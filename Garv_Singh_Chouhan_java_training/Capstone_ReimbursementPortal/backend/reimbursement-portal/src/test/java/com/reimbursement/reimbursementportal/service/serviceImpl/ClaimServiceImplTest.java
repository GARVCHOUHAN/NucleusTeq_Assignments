package com.reimbursement.reimbursementportal.service.serviceImpl;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.reimbursement.reimbursementportal.dto.request.ClaimActionRequestDTO;
import com.reimbursement.reimbursementportal.dto.request.ClaimRequestDTO;
import com.reimbursement.reimbursementportal.dto.response.ClaimResponseDTO;
import com.reimbursement.reimbursementportal.dto.response.PageResponseDTO;
import com.reimbursement.reimbursementportal.entity.Claim;
import com.reimbursement.reimbursementportal.entity.User;
import com.reimbursement.reimbursementportal.enums.ClaimStatus;
import com.reimbursement.reimbursementportal.enums.Role;
import com.reimbursement.reimbursementportal.exception.BadRequestException;
import com.reimbursement.reimbursementportal.repository.ClaimRepository;
import com.reimbursement.reimbursementportal.repository.UserRepository;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;

@ExtendWith(MockitoExtension.class)
class ClaimServiceImplTest {

    @Mock
    private ClaimRepository claimRepository;

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private ClaimServiceImpl claimService;

    private User employee;
    private User manager;
    private User admin;

    @BeforeEach
    void setUp() {
        manager = User.builder().id(2L).name("Manager").role(Role.MANAGER).build();
        admin = User.builder().id(3L).name("Admin").role(Role.ADMIN).build();
        employee = User.builder().id(1L).name("Employee").role(Role.EMPLOYEE).manager(manager).build();
    }

    @Test
    void submitClaimAssignsEmployeeManagerAsReviewer() {
        ClaimRequestDTO request = claimRequest(2500.0);
        when(userRepository.findById(1L)).thenReturn(Optional.of(employee));
        when(claimRepository.save(any(Claim.class))).thenAnswer(invocation -> {
            Claim claim = invocation.getArgument(0);
            claim.setId(10L);
            return claim;
        });

        ClaimResponseDTO response = claimService.submitClaim(request);

        assertEquals(10L, response.getId());
        assertEquals(manager.getId(), response.getReviewerId());
        assertEquals(LocalDate.of(2026, 5, 1), response.getDate());
        ArgumentCaptor<Claim> claimCaptor = ArgumentCaptor.forClass(Claim.class);
        verify(claimRepository).save(claimCaptor.capture());
        assertEquals(ClaimStatus.SUBMITTED, claimCaptor.getValue().getStatus());
    }

    @Test
    void submitClaimFallsBackToAdminWhenEmployeeHasNoManager() {
        employee.setManager(null);
        when(userRepository.findById(1L)).thenReturn(Optional.of(employee));
        when(userRepository.findByRole(Role.ADMIN)).thenReturn(List.of(admin));
        when(claimRepository.save(any(Claim.class))).thenAnswer(invocation -> invocation.getArgument(0));

        ClaimResponseDTO response = claimService.submitClaim(claimRequest(1200.0));

        assertEquals(admin.getId(), response.getReviewerId());
    }

    @Test
    void submitClaimRejectsAmountAboveLimit() {
        ClaimRequestDTO request = claimRequest(100001.0);

        BadRequestException ex = assertThrows(BadRequestException.class, () -> claimService.submitClaim(request));

        assertEquals("Amount must not exceed 100000", ex.getMessage());
    }

    @Test
    void takeActionApprovesSubmittedClaimByAssignedReviewer() {
        Claim claim = claim(ClaimStatus.SUBMITTED, manager);
        ClaimActionRequestDTO request = actionRequest(ClaimStatus.APPROVED, "Approved");
        when(claimRepository.findById(20L)).thenReturn(Optional.of(claim));
        when(userRepository.findById(2L)).thenReturn(Optional.of(manager));
        when(claimRepository.save(any(Claim.class))).thenAnswer(invocation -> invocation.getArgument(0));

        ClaimResponseDTO response = claimService.takeAction(20L, 2L, request);

        assertEquals(ClaimStatus.APPROVED, response.getStatus());
        assertEquals("Approved", response.getComment());
    }

    @Test
    void takeActionRejectsUnauthorizedReviewer() {
        Claim claim = claim(ClaimStatus.SUBMITTED, manager);
        User anotherManager = User.builder().id(5L).role(Role.MANAGER).build();
        when(claimRepository.findById(20L)).thenReturn(Optional.of(claim));
        when(userRepository.findById(5L)).thenReturn(Optional.of(anotherManager));

        BadRequestException ex = assertThrows(BadRequestException.class,
                () -> claimService.takeAction(20L, 5L, actionRequest(ClaimStatus.APPROVED, "")));

        assertEquals("You are not authorized to take action on this claim", ex.getMessage());
    }

    @Test
    void takeActionRejectsAlreadyProcessedClaim() {
        Claim claim = claim(ClaimStatus.APPROVED, manager);
        when(claimRepository.findById(20L)).thenReturn(Optional.of(claim));
        when(userRepository.findById(2L)).thenReturn(Optional.of(manager));

        BadRequestException ex = assertThrows(BadRequestException.class,
                () -> claimService.takeAction(20L, 2L, actionRequest(ClaimStatus.REJECTED, "Late")));

        assertEquals("Claim has already been processed", ex.getMessage());
    }

    @Test
    void takeActionRequiresCommentForRejection() {
        Claim claim = claim(ClaimStatus.SUBMITTED, manager);
        when(claimRepository.findById(20L)).thenReturn(Optional.of(claim));
        when(userRepository.findById(2L)).thenReturn(Optional.of(manager));

        BadRequestException ex = assertThrows(BadRequestException.class,
                () -> claimService.takeAction(20L, 2L, actionRequest(ClaimStatus.REJECTED, "")));

        assertEquals("A comment is required when rejecting a claim", ex.getMessage());
    }

    @Test
    void takeActionRejectsSubmittedAsTargetStatus() {
        Claim claim = claim(ClaimStatus.SUBMITTED, manager);
        when(claimRepository.findById(20L)).thenReturn(Optional.of(claim));
        when(userRepository.findById(2L)).thenReturn(Optional.of(manager));

        BadRequestException ex = assertThrows(BadRequestException.class,
                () -> claimService.takeAction(20L, 2L, actionRequest(ClaimStatus.SUBMITTED, "")));

        assertEquals("Invalid action - cannot set status to SUBMITTED", ex.getMessage());
    }

    @Test
    void adminCanActOnAdminFallbackClaim() {
        Claim claim = claim(ClaimStatus.SUBMITTED, admin);
        when(claimRepository.findById(20L)).thenReturn(Optional.of(claim));
        when(userRepository.findById(3L)).thenReturn(Optional.of(admin));
        when(claimRepository.save(any(Claim.class))).thenAnswer(invocation -> invocation.getArgument(0));

        ClaimResponseDTO response = claimService.takeAction(20L, 3L, actionRequest(ClaimStatus.APPROVED, ""));

        assertEquals(ClaimStatus.APPROVED, response.getStatus());
    }

    @Test
    void getClaimsByReviewerReturnsPaginatedPayload() {
        Claim claim = claim(ClaimStatus.SUBMITTED, manager);
        when(userRepository.existsById(2L)).thenReturn(true);
        when(claimRepository.findByReviewerId(any(Long.class), any(Pageable.class)))
                .thenReturn(new PageImpl<>(List.of(claim)));

        PageResponseDTO<ClaimResponseDTO> response = claimService.getClaimsByReviewer(2L, 0, 10);

        assertEquals(1, response.getContent().size());
        assertEquals(0, response.getPage());
    }

    @Test
    void getAllClaimsReturnsPaginatedPayload() {
        when(claimRepository.findAll(any(Pageable.class))).thenReturn(new PageImpl<>(List.of(claim(ClaimStatus.SUBMITTED, manager))));

        PageResponseDTO<ClaimResponseDTO> response = claimService.getAllClaims(0, 10);

        assertEquals(1, response.getTotalElements());
    }

    @Test
    void getClaimsByEmployeeRejectsMissingEmployee() {
        when(userRepository.existsById(99L)).thenReturn(false);

        BadRequestException ex = assertThrows(BadRequestException.class,
                () -> claimService.getClaimsByEmployee(99L, 0, 10));

        assertEquals("Employee not found", ex.getMessage());
    }

    @Test
    void getClaimsByStatusReturnsPaginatedPayload() {
        when(claimRepository.findByStatus(any(ClaimStatus.class), any(Pageable.class)))
                .thenReturn(new PageImpl<>(List.of(claim(ClaimStatus.REJECTED, manager))));

        PageResponseDTO<ClaimResponseDTO> response = claimService.getClaimsByStatus(ClaimStatus.REJECTED, 0, 10);

        assertEquals(ClaimStatus.REJECTED, response.getContent().get(0).getStatus());
    }

    private ClaimRequestDTO claimRequest(Double amount) {
        ClaimRequestDTO request = new ClaimRequestDTO();
        request.setAmount(amount);
        request.setClaimDate(LocalDate.of(2026, 5, 1));
        request.setDescription("Taxi fare");
        request.setEmployeeId(1L);
        return request;
    }

    private ClaimActionRequestDTO actionRequest(ClaimStatus status, String comment) {
        ClaimActionRequestDTO request = new ClaimActionRequestDTO();
        request.setStatus(status);
        request.setComment(comment);
        return request;
    }

    private Claim claim(ClaimStatus status, User reviewer) {
        return Claim.builder()
                .id(20L)
                .amount(BigDecimal.valueOf(500))
                .claimDate(LocalDate.of(2026, 5, 1))
                .description("Lunch")
                .status(status)
                .employee(employee)
                .reviewer(reviewer)
                .build();
    }
}

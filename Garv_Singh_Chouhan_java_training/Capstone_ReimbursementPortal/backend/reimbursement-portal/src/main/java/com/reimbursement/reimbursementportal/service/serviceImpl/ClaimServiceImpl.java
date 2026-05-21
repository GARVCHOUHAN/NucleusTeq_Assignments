package com.reimbursement.reimbursementportal.service.serviceImpl;
import com.reimbursement.reimbursementportal.dto.request.ClaimActionRequestDTO;
import com.reimbursement.reimbursementportal.dto.request.ClaimRequestDTO;
import com.reimbursement.reimbursementportal.dto.response.ClaimResponseDTO;
import com.reimbursement.reimbursementportal.entity.Claim;
import com.reimbursement.reimbursementportal.entity.User;
import com.reimbursement.reimbursementportal.enums.ClaimStatus;
import com.reimbursement.reimbursementportal.enums.Role;
import com.reimbursement.reimbursementportal.exception.BadRequestException;
import com.reimbursement.reimbursementportal.exception.ResourceNotFoundException;
import com.reimbursement.reimbursementportal.mapper.ClaimMapper;
import com.reimbursement.reimbursementportal.repository.ClaimRepository;
import com.reimbursement.reimbursementportal.repository.UserRepository;
import com.reimbursement.reimbursementportal.service.ClaimService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

@Service
@RequiredArgsConstructor
public class ClaimServiceImpl implements ClaimService {

    private final ClaimRepository claimRepository;
    private final UserRepository userRepository;
    private static final Logger log = LoggerFactory.getLogger(ClaimServiceImpl.class);

    // ========================= SUBMIT CLAIM =========================
    @Override
    public ClaimResponseDTO submitClaim(ClaimRequestDTO request) {

        if (request.getAmount() == null || request.getAmount() <= 0) {
            throw new BadRequestException("Amount must be greater than 0");
        }

        if (request.getDescription() == null || request.getDescription().isBlank()) {
            throw new BadRequestException("Description is required");
        }

        User employee = userRepository.findById(request.getEmployeeId())
                .orElseThrow(() ->
                        new BadRequestException("Employee not found with id: " + request.getEmployeeId()));

        // Assign reviewer: manager if assigned, else fallback to Admin
        User reviewer = resolveReviewer(employee);

        Claim claim = new Claim();
        claim.setAmount(BigDecimal.valueOf(request.getAmount()));
        claim.setDescription(request.getDescription());
        claim.setDate(LocalDate.now());
        claim.setStatus(ClaimStatus.SUBMITTED);
        claim.setEmployee(employee);
        claim.setReviewer(reviewer);

        log.info("Claim submitted for employeeId: {}", request.getEmployeeId());
        return ClaimMapper.toResponse(claimRepository.save(claim));

    }

    // ========================= GET ALL CLAIMS =========================
    @Override
    public List<ClaimResponseDTO> getAllClaims() {
        return claimRepository.findAll()
                .stream()
                .map(ClaimMapper::toResponse)
                .toList();
    }

    // ========================= GET CLAIMS BY EMPLOYEE =========================
    @Override
    public List<ClaimResponseDTO> getClaimsByEmployee(Long employeeId) {

        if (!userRepository.existsById(employeeId)) {
            throw new BadRequestException("Employee not found");
        }

        return claimRepository.findByEmployeeId(employeeId)
                .stream()
                .map(ClaimMapper::toResponse)
                .toList();
    }

    // ========================= GET CLAIMS BY REVIEWER =========================
    @Override
    public List<ClaimResponseDTO> getClaimsByReviewer(Long reviewerId) {

        if (!userRepository.existsById(reviewerId)) {
            throw new BadRequestException("Reviewer not found");
        }

        return claimRepository.findByReviewerId(reviewerId)
                .stream()
                .map(ClaimMapper::toResponse)
                .toList();
    }

    // ========================= GET CLAIMS BY STATUS =========================
    @Override
    public List<ClaimResponseDTO> getClaimsByStatus(ClaimStatus status) {
        return claimRepository.findByStatus(status)
                .stream()
                .map(ClaimMapper::toResponse)
                .toList();
    }

    // ========================= TAKE ACTION =========================
    @Override
    public ClaimResponseDTO takeAction(Long claimId, Long reviewerId, ClaimActionRequestDTO request) {

        log.info("Processing claim: claimId={}, reviewerId={}, status={}",
                claimId, reviewerId, request.getStatus());
        Claim claim = claimRepository.findById(claimId)
                .orElseThrow(() -> new ResourceNotFoundException("Claim not found"));

        User reviewer = userRepository.findById(reviewerId)
                .orElseThrow(() -> new ResourceNotFoundException("Reviewer not found"));

        // Claim must still be SUBMITTED to be actioned
        if (claim.getStatus() != ClaimStatus.SUBMITTED) {
            throw new BadRequestException("Claim has already been processed");
        }

        // AUTHORIZATION:
        // Allow action if:
        //   (a) the acting user is an ADMIN — admin can approve/reject ANY claim, OR
        //   (b) the acting user is the assigned reviewer on this specific claim
        boolean isAssignedReviewer = claim.getReviewer() != null &&
                claim.getReviewer().getId().equals(reviewerId);

        if (!isAssignedReviewer) {
            throw new BadRequestException("You are not authorized to take action on this claim");
        }

        // Cannot set status back to SUBMITTED
        if (request.getStatus() == ClaimStatus.SUBMITTED) {
            throw new BadRequestException("Invalid action — cannot set status to SUBMITTED");
        }

        // Comment is mandatory for rejection
        if (request.getStatus() == ClaimStatus.REJECTED &&
                (request.getComment() == null || request.getComment().isBlank())) {
            throw new BadRequestException("A comment is required when rejecting a claim");
        }

        claim.setStatus(request.getStatus());
        if (request.getStatus() == ClaimStatus.APPROVED) {
            log.info("Claim APPROVED: {}", claimId);
        }

        if (request.getStatus() == ClaimStatus.REJECTED) {
            log.warn("Claim REJECTED: {} reason={}", claimId, request.getComment());
        }
        claim.setComment(request.getComment());

        // Update reviewer to the person who actually took the action
        // This correctly records that an Admin actioned it, not the original assigned reviewer
        claim.setReviewer(reviewer);


        return ClaimMapper.toResponse(claimRepository.save(claim));
    }

    // ========================= RESOLVE REVIEWER =========================
    // If employee has a manager → manager is reviewer
    // If no manager assigned → first Admin acts as fallback reviewer
    private User resolveReviewer(User employee) {

        if (employee.getManager() != null) {
            return employee.getManager();
        }

        return userRepository.findByRole(Role.ADMIN)
                .stream()
                .findFirst()
                .orElseThrow(() ->
                        new BadRequestException("No admin available to act as reviewer"));
    }
}

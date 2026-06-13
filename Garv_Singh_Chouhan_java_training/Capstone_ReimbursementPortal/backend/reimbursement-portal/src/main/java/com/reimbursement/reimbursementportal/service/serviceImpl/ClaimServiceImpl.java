package com.reimbursement.reimbursementportal.service.serviceImpl;
import com.reimbursement.reimbursementportal.dto.request.ClaimActionRequestDTO;
import com.reimbursement.reimbursementportal.dto.request.ClaimRequestDTO;
import com.reimbursement.reimbursementportal.dto.response.ClaimResponseDTO;
import com.reimbursement.reimbursementportal.dto.response.PageResponseDTO;
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
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;

@Service
@RequiredArgsConstructor
public class ClaimServiceImpl implements ClaimService {

    private final ClaimRepository claimRepository;
    private final UserRepository userRepository;
    private static final Logger log = LoggerFactory.getLogger(ClaimServiceImpl.class);
    private static final BigDecimal MAX_CLAIM_AMOUNT = BigDecimal.valueOf(100000);
    private static final int MAX_PAGE_SIZE = 100;

    // ========================= SUBMIT CLAIM =========================
    @Override
    public ClaimResponseDTO submitClaim(ClaimRequestDTO request) {

        log.info("Claim submission started: employeeId={}, amount={}",
                request.getEmployeeId(), request.getAmount());

        if (request.getAmount() == null || request.getAmount() <= 0) {
            log.warn("Invalid claim request by employee {}: amount={}",
                    request.getEmployeeId(), request.getAmount());
            throw new BadRequestException("Amount must be greater than 0");
        }

        BigDecimal amount = BigDecimal.valueOf(request.getAmount());
        if (amount.compareTo(MAX_CLAIM_AMOUNT) > 0) {
            log.warn("Invalid claim request by employee {}: amount exceeds limit",
                    request.getEmployeeId());
            throw new BadRequestException("Amount must not exceed 100000");
        }

        if (request.getClaimDate() == null) {
            log.warn("Invalid claim request by employee {}: missing claim date",
                    request.getEmployeeId());
            throw new BadRequestException("Claim date is required");
        }

        if (request.getDescription() == null || request.getDescription().isBlank()) {
            log.warn("Invalid claim request by employee {}: missing description",
                    request.getEmployeeId());
            throw new BadRequestException("Description is required");
        }

        log.info("Fetching employee for claim submission: {}", request.getEmployeeId());
        User employee = userRepository.findById(request.getEmployeeId())
                .orElseThrow(() -> {
                    log.warn("Invalid claim request by employee {}: employee not found",
                            request.getEmployeeId());
                    return new BadRequestException("Employee not found with id: " + request.getEmployeeId());
                });

        // Assign reviewer: manager if assigned, else fallback to Admin
        User reviewer = resolveReviewer(employee);

        Claim claim = new Claim();
        claim.setAmount(amount);
        claim.setDescription(request.getDescription());
        claim.setDate(request.getClaimDate());
        claim.setStatus(ClaimStatus.SUBMITTED);
        claim.setEmployee(employee);
        claim.setReviewer(reviewer);

        log.info("Saving claim for employee {} amount {}", request.getEmployeeId(), amount);
        Claim savedClaim = claimRepository.save(claim);
        log.info("Claim submitted by employee {} amount {}", request.getEmployeeId(), amount);
        return ClaimMapper.toResponse(savedClaim);

    }

    // ========================= GET ALL CLAIMS =========================
    @Override
    public PageResponseDTO<ClaimResponseDTO> getAllClaims(int page, int size) {
        log.info("Fetching all claims: page={}, size={}", page, size);
        return toPageResponse(claimRepository.findAll(pageable(page, size)));
    }

    // ========================= GET CLAIMS BY EMPLOYEE =========================
    @Override
    public PageResponseDTO<ClaimResponseDTO> getClaimsByEmployee(Long employeeId, int page, int size) {

        log.info("Fetching claims for employee {}", employeeId);
        if (!userRepository.existsById(employeeId)) {
            log.warn("Invalid claim retrieval: employee not found {}", employeeId);
            throw new BadRequestException("Employee not found");
        }

        return toPageResponse(claimRepository.findByEmployeeId(employeeId, pageable(page, size)));
    }

    // ========================= GET CLAIMS BY REVIEWER =========================
    @Override
    public PageResponseDTO<ClaimResponseDTO> getClaimsByReviewer(Long reviewerId, int page, int size) {

        log.info("Fetching claims for reviewer {}", reviewerId);
        if (!userRepository.existsById(reviewerId)) {
            log.warn("Invalid claim retrieval: reviewer not found {}", reviewerId);
            throw new BadRequestException("Reviewer not found");
        }

        return toPageResponse(claimRepository.findByReviewerId(reviewerId, pageable(page, size)));
    }

    // ========================= GET CLAIMS BY STATUS =========================
    @Override
    public PageResponseDTO<ClaimResponseDTO> getClaimsByStatus(ClaimStatus status, int page, int size) {
        log.info("Fetching claims by status {}", status);
        return toPageResponse(claimRepository.findByStatus(status, pageable(page, size)));
    }

    // ========================= TAKE ACTION =========================
    @Override
    public ClaimResponseDTO takeAction(Long claimId, Long reviewerId, ClaimActionRequestDTO request) {

        log.info("Processing claim: claimId={}, reviewerId={}, status={}",
                claimId, reviewerId, request.getStatus());
        Claim claim = claimRepository.findById(claimId)
                .orElseThrow(() -> {
                    log.warn("Invalid claim action: claim not found {}", claimId);
                    return new ResourceNotFoundException("Claim not found");
                });

        User reviewer = userRepository.findById(reviewerId)
                .orElseThrow(() -> {
                    log.warn("Invalid claim action: reviewer not found {}", reviewerId);
                    return new ResourceNotFoundException("Reviewer not found");
                });

        // Claim must still be SUBMITTED to be actioned
        if (claim.getStatus() != ClaimStatus.SUBMITTED) {
            log.warn("Invalid claim action: claimId={} already status={}", claimId, claim.getStatus());
            throw new BadRequestException("Claim has already been processed");
        }

        // Only the assigned reviewer can approve or reject a claim.
        // For admin fallback claims, any admin can complete the review.
        boolean isAssignedReviewer = claim.getReviewer() != null &&
                claim.getReviewer().getId().equals(reviewerId);
        boolean isAdminFallbackClaim = reviewer.getRole() == Role.ADMIN &&
                claim.getReviewer() != null &&
                claim.getReviewer().getRole() == Role.ADMIN;

        if (!isAssignedReviewer && !isAdminFallbackClaim) {
            log.warn("Unauthorized claim action: claimId={}, reviewerId={}", claimId, reviewerId);
            throw new BadRequestException("You are not authorized to take action on this claim");
        }

        // Cannot set status back to SUBMITTED
        if (request.getStatus() == ClaimStatus.SUBMITTED) {
            log.warn("Invalid claim status update: claimId={} requested SUBMITTED", claimId);
            throw new BadRequestException("Invalid action - cannot set status to SUBMITTED");
        }

        // Comment is mandatory for rejection
        if (request.getStatus() == ClaimStatus.REJECTED &&
                (request.getComment() == null || request.getComment().isBlank())) {
            log.warn("Invalid claim rejection: claimId={} missing comment", claimId);
            throw new BadRequestException("A comment is required when rejecting a claim");
        }

        claim.setStatus(request.getStatus());
        if (request.getStatus() == ClaimStatus.APPROVED) {
            log.info("Claim {} approved by reviewer {}", claimId, reviewerId);
        }

        if (request.getStatus() == ClaimStatus.REJECTED) {
            log.info("Claim {} rejected by reviewer {}", claimId, reviewerId);
        }
        claim.setComment(request.getComment());

        // Keep reviewer aligned with the person who completed the assigned review.
        claim.setReviewer(reviewer);


        log.info("Saving claim status update: claimId={}, status={}", claimId, request.getStatus());
        return ClaimMapper.toResponse(claimRepository.save(claim));
    }

    // ========================= RESOLVE REVIEWER =========================
    // If employee has a manager → manager is reviewer
    // If no manager assigned → first Admin acts as fallback reviewer
    private User resolveReviewer(User employee) {

        if (employee.getManager() != null) {
            log.info("Resolved reviewer from manager: employeeId={}, reviewerId={}",
                    employee.getId(), employee.getManager().getId());
            return employee.getManager();
        }

        return userRepository.findByRole(Role.ADMIN)
                .stream()
                .findFirst()
                .orElseThrow(() -> {
                    log.error("Database operation failed: no admin available to act as reviewer");
                    return new BadRequestException("No admin available to act as reviewer");
                });
    }

    private Pageable pageable(int page, int size) {
        int safePage = Math.max(page, 0);
        int safeSize = Math.min(Math.max(size, 1), MAX_PAGE_SIZE);
        return PageRequest.of(safePage, safeSize, Sort.by(Sort.Direction.DESC, "createdAt"));
    }

    private PageResponseDTO<ClaimResponseDTO> toPageResponse(Page<Claim> claimPage) {
        Page<ClaimResponseDTO> dtoPage = claimPage.map(ClaimMapper::toResponse);
        return PageResponseDTO.<ClaimResponseDTO>builder()
                .content(dtoPage.getContent())
                .page(dtoPage.getNumber())
                .size(dtoPage.getSize())
                .totalElements(dtoPage.getTotalElements())
                .totalPages(dtoPage.getTotalPages())
                .first(dtoPage.isFirst())
                .last(dtoPage.isLast())
                .build();
    }
}

package com.reimbursement.reimbursementportal.controller;

import com.reimbursement.reimbursementportal.dto.request.ClaimActionRequestDTO;
import com.reimbursement.reimbursementportal.dto.request.ClaimRequestDTO;
import com.reimbursement.reimbursementportal.dto.response.ClaimResponseDTO;
import com.reimbursement.reimbursementportal.dto.response.PageResponseDTO;
import com.reimbursement.reimbursementportal.dto.StandardAPIResponse;
import com.reimbursement.reimbursementportal.enums.ClaimStatus;
import com.reimbursement.reimbursementportal.service.ClaimService;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/claims")
@RequiredArgsConstructor
public class ClaimController {

    private static final Logger log = LoggerFactory.getLogger(ClaimController.class);

    private final ClaimService claimService;

    // ======================= SUBMIT CLAIM =======================
    @PostMapping
    public ResponseEntity<StandardAPIResponse<ClaimResponseDTO>> submitClaim(
            @Valid @RequestBody ClaimRequestDTO request) {

        log.info("Submit claim request received: employeeId={}, amount={}",
                request.getEmployeeId(), request.getAmount());
        ClaimResponseDTO response = claimService.submitClaim(request);
        log.info("Submit claim request completed: claimId={}", response.getId());

        StandardAPIResponse<ClaimResponseDTO> apiResponse =
                StandardAPIResponse.<ClaimResponseDTO>builder()
                        .success(true)
                        .message("Claim submitted successfully")
                        .data(response)
                        .build();

        return ResponseEntity.ok(apiResponse);
    }

    // ========================= GET ALL CLAIMS =========================
    @GetMapping
    public ResponseEntity<StandardAPIResponse<PageResponseDTO<ClaimResponseDTO>>> getAllClaims(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {

        log.info("Fetch all claims request received: page={}, size={}", page, size);
        PageResponseDTO<ClaimResponseDTO> response = claimService.getAllClaims(page, size);
        log.info("Fetch all claims request completed: total={}", response.getTotalElements());

        StandardAPIResponse<PageResponseDTO<ClaimResponseDTO>> apiResponse =
                StandardAPIResponse.<PageResponseDTO<ClaimResponseDTO>>builder()
                        .success(true)
                        .message("Claims fetched successfully")
                        .data(response)
                        .build();

        return ResponseEntity.ok(apiResponse);
    }

    // ========================= GET CLAIMS BY EMPLOYEE =========================
    @GetMapping("/employee/{employeeId}")
    public ResponseEntity<StandardAPIResponse<PageResponseDTO<ClaimResponseDTO>>> getClaimsByEmployee(
            @PathVariable Long employeeId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {

        log.info("Fetch claims by employee request received: employeeId={}", employeeId);
        PageResponseDTO<ClaimResponseDTO> response = claimService.getClaimsByEmployee(employeeId, page, size);
        log.info("Fetch claims by employee request completed: employeeId={}, total={}",
                employeeId, response.getTotalElements());

        StandardAPIResponse<PageResponseDTO<ClaimResponseDTO>> apiResponse =
                StandardAPIResponse.<PageResponseDTO<ClaimResponseDTO>>builder()
                        .success(true)
                        .message("Employee claims fetched successfully")
                        .data(response)
                        .build();

        return ResponseEntity.ok(apiResponse);
    }

    // ========================= GET CLAIMS BY REVIEWER =========================
    @GetMapping("/reviewer/{reviewerId}")
    public ResponseEntity<StandardAPIResponse<PageResponseDTO<ClaimResponseDTO>>> getClaimsByReviewer(
            @PathVariable Long reviewerId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {

        log.info("Fetch claims by reviewer request received: reviewerId={}", reviewerId);
        PageResponseDTO<ClaimResponseDTO> response = claimService.getClaimsByReviewer(reviewerId, page, size);
        log.info("Fetch claims by reviewer request completed: reviewerId={}, total={}",
                reviewerId, response.getTotalElements());

        StandardAPIResponse<PageResponseDTO<ClaimResponseDTO>> apiResponse =
                StandardAPIResponse.<PageResponseDTO<ClaimResponseDTO>>builder()
                        .success(true)
                        .message("Reviewer claims fetched successfully")
                        .data(response)
                        .build();

        return ResponseEntity.ok(apiResponse);
    }

    // ========================= GET CLAIMS BY STATUS =========================
    @GetMapping("/status/{status}")
    public ResponseEntity<StandardAPIResponse<PageResponseDTO<ClaimResponseDTO>>> getClaimsByStatus(
            @PathVariable ClaimStatus status,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {

        log.info("Fetch claims by status request received: status={}", status);
        PageResponseDTO<ClaimResponseDTO> response = claimService.getClaimsByStatus(status, page, size);
        log.info("Fetch claims by status request completed: status={}, total={}",
                status, response.getTotalElements());

        StandardAPIResponse<PageResponseDTO<ClaimResponseDTO>> apiResponse =
                StandardAPIResponse.<PageResponseDTO<ClaimResponseDTO>>builder()
                        .success(true)
                        .message("Claims fetched by status successfully")
                        .data(response)
                        .build();

        return ResponseEntity.ok(apiResponse);
    }

    // ========================= TAKE ACTION =========================
    @PutMapping("/{claimId}/action/{reviewerId}")
    public ResponseEntity<StandardAPIResponse<ClaimResponseDTO>> takeAction(
            @PathVariable Long claimId,
            @PathVariable Long reviewerId,
            @Valid @RequestBody ClaimActionRequestDTO request) {

        log.info("Claim status update request received: claimId={}, reviewerId={}, status={}",
                claimId, reviewerId, request.getStatus());
        ClaimResponseDTO response = claimService.takeAction(claimId, reviewerId, request);
        log.info("Claim status update request completed: claimId={}, status={}",
                claimId, response.getStatus());

        StandardAPIResponse<ClaimResponseDTO> apiResponse =
                StandardAPIResponse.<ClaimResponseDTO>builder()
                        .success(true)
                        .message("Claim updated successfully")
                        .data(response)
                        .build();

        return ResponseEntity.ok(apiResponse);
    }
}

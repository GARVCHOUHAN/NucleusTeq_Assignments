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

    private final ClaimService claimService;

    // ======================= SUBMIT CLAIM =======================
    @PostMapping
    public ResponseEntity<StandardAPIResponse<ClaimResponseDTO>> submitClaim(
            @Valid @RequestBody ClaimRequestDTO request) {

        ClaimResponseDTO response = claimService.submitClaim(request);

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

        PageResponseDTO<ClaimResponseDTO> response = claimService.getAllClaims(page, size);

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

        PageResponseDTO<ClaimResponseDTO> response = claimService.getClaimsByEmployee(employeeId, page, size);

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

        PageResponseDTO<ClaimResponseDTO> response = claimService.getClaimsByReviewer(reviewerId, page, size);

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

        PageResponseDTO<ClaimResponseDTO> response = claimService.getClaimsByStatus(status, page, size);

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

        ClaimResponseDTO response = claimService.takeAction(claimId, reviewerId, request);

        StandardAPIResponse<ClaimResponseDTO> apiResponse =
                StandardAPIResponse.<ClaimResponseDTO>builder()
                        .success(true)
                        .message("Claim updated successfully")
                        .data(response)
                        .build();

        return ResponseEntity.ok(apiResponse);
    }
}

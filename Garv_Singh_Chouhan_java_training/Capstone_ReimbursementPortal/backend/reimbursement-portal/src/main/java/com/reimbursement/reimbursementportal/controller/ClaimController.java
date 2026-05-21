package com.reimbursement.reimbursementportal.controller;

import com.reimbursement.reimbursementportal.dto.request.ClaimActionRequestDTO;
import com.reimbursement.reimbursementportal.dto.request.ClaimRequestDTO;
import com.reimbursement.reimbursementportal.dto.response.ClaimResponseDTO;
import com.reimbursement.reimbursementportal.dto.StandardAPIResponse;
import com.reimbursement.reimbursementportal.enums.ClaimStatus;
import com.reimbursement.reimbursementportal.service.ClaimService;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/claims")
@RequiredArgsConstructor
public class ClaimController {

    private final ClaimService claimService;

    // ======================= SUBMIT CLAIM =======================
    @PostMapping
    public ResponseEntity<StandardAPIResponse<ClaimResponseDTO>> submitClaim(
            @RequestBody ClaimRequestDTO request) {

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
    public ResponseEntity<StandardAPIResponse<List<ClaimResponseDTO>>> getAllClaims() {

        List<ClaimResponseDTO> response = claimService.getAllClaims();

        StandardAPIResponse<List<ClaimResponseDTO>> apiResponse =
                StandardAPIResponse.<List<ClaimResponseDTO>>builder()
                        .success(true)
                        .message("Claims fetched successfully")
                        .data(response)
                        .build();

        return ResponseEntity.ok(apiResponse);
    }

    // ========================= GET CLAIMS BY EMPLOYEE =========================
    @GetMapping("/employee/{employeeId}")
    public ResponseEntity<StandardAPIResponse<List<ClaimResponseDTO>>> getClaimsByEmployee(
            @PathVariable Long employeeId) {

        List<ClaimResponseDTO> response = claimService.getClaimsByEmployee(employeeId);

        StandardAPIResponse<List<ClaimResponseDTO>> apiResponse =
                StandardAPIResponse.<List<ClaimResponseDTO>>builder()
                        .success(true)
                        .message("Employee claims fetched successfully")
                        .data(response)
                        .build();

        return ResponseEntity.ok(apiResponse);
    }

    // ========================= GET CLAIMS BY REVIEWER =========================
    @GetMapping("/reviewer/{reviewerId}")
    public ResponseEntity<StandardAPIResponse<List<ClaimResponseDTO>>> getClaimsByReviewer(
            @PathVariable Long reviewerId) {

        List<ClaimResponseDTO> response = claimService.getClaimsByReviewer(reviewerId);

        StandardAPIResponse<List<ClaimResponseDTO>> apiResponse =
                StandardAPIResponse.<List<ClaimResponseDTO>>builder()
                        .success(true)
                        .message("Reviewer claims fetched successfully")
                        .data(response)
                        .build();

        return ResponseEntity.ok(apiResponse);
    }

    // ========================= GET CLAIMS BY STATUS =========================
    @GetMapping("/status/{status}")
    public ResponseEntity<StandardAPIResponse<List<ClaimResponseDTO>>> getClaimsByStatus(
            @PathVariable ClaimStatus status) {

        List<ClaimResponseDTO> response = claimService.getClaimsByStatus(status);

        StandardAPIResponse<List<ClaimResponseDTO>> apiResponse =
                StandardAPIResponse.<List<ClaimResponseDTO>>builder()
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
            @RequestBody ClaimActionRequestDTO request) {

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

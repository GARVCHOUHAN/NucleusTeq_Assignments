package com.reimbursement.reimbursementportal.service;
import com.reimbursement.reimbursementportal.dto.request.ClaimActionRequestDTO;

import com.reimbursement.reimbursementportal.dto.request.ClaimRequestDTO;

import com.reimbursement.reimbursementportal.dto.response.ClaimResponseDTO;
import com.reimbursement.reimbursementportal.dto.response.PageResponseDTO;

import com.reimbursement.reimbursementportal.enums.ClaimStatus;

/**
 * Service interface for claim operations.
 */
public interface ClaimService {

    /**
     * Submits a new claim.
     *
     * @param request the claim request
     * @return the created claim
     */
    ClaimResponseDTO submitClaim(ClaimRequestDTO request);

    /**
     * Retrieves all claims.
     *
     * @return list of claims
     */
    PageResponseDTO<ClaimResponseDTO> getAllClaims(int page, int size);

    /**
     * Retrieves claims by employee ID.
     *
     * @param employeeId the employee ID
     * @return list of claims
     */
    PageResponseDTO<ClaimResponseDTO> getClaimsByEmployee(Long employeeId, int page, int size);

    /**
     * Retrieves claims by reviewer ID.
     *
     * @param reviewerId the reviewer ID
     * @return list of claims
     */
    PageResponseDTO<ClaimResponseDTO> getClaimsByReviewer(Long reviewerId, int page, int size);

    /**
     * Retrieves claims by status.
     *
     * @param status the claim status
     * @return list of claims
     */
    PageResponseDTO<ClaimResponseDTO> getClaimsByStatus(ClaimStatus status, int page, int size);

    /**
     * Takes action on a claim.
     *
     * @param claimId the claim ID
     * @param reviewerId the reviewer ID
     * @param request the action request
     * @return the updated claim
     */
    ClaimResponseDTO takeAction(Long claimId, Long reviewerId, ClaimActionRequestDTO request);
}

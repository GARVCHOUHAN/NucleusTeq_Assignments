package com.reimbursement.reimbursementportal.repository;

import com.reimbursement.reimbursementportal.entity.Claim;
import com.reimbursement.reimbursementportal.enums.ClaimStatus;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

/**
 * Repository for Claim entity.
 */
public interface ClaimRepository extends JpaRepository<Claim, Long> {

    /**
     * Finds claims by employee ID.
     *
     * @param employeeId the employee ID
     * @return list of claims
     */
    List<Claim> findByEmployeeId(Long employeeId);

    /**
     * Finds claims by employee ID and status.
     *
     * @param employeeId the employee ID
     * @param status the claim status
     * @return list of claims
     */
    List<Claim> findByEmployeeIdAndStatus(Long employeeId, ClaimStatus status);

    /**
     * Finds claims by reviewer ID.
     *
     * @param reviewerId the reviewer ID
     * @return list of claims
     */
    List<Claim> findByReviewerId(Long reviewerId);

    /**
     * Finds claims by status.
     *
     * @param status the claim status
     * @return list of claims
     */
    List<Claim> findByStatus(ClaimStatus status);

    /**
     * Finds claims by reviewer ID and status.
     *
     * @param reviewerId the reviewer ID
     * @param status the claim status
     * @return list of claims
     */
    List<Claim> findByReviewerIdAndStatus(Long reviewerId, ClaimStatus status);
}

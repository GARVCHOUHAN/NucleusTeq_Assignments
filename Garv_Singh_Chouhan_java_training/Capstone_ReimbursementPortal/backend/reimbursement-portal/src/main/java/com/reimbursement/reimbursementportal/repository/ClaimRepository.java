package com.reimbursement.reimbursementportal.repository;

import com.reimbursement.reimbursementportal.entity.Claim;
import com.reimbursement.reimbursementportal.enums.ClaimStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * Data access layer for Claim entities.
 */
@Repository
public interface ClaimRepository extends JpaRepository<Claim, Long> {

    Page<Claim> findByEmployeeId(Long employeeId, Pageable pageable);

    Page<Claim> findByReviewerId(Long reviewerId, Pageable pageable);

    Page<Claim> findByReviewerIdAndStatus(Long reviewerId, ClaimStatus status, Pageable pageable);

    Page<Claim> findAll(Pageable pageable);

    long countByEmployeeId(Long employeeId);

    long countByReviewerIdAndStatus(Long reviewerId, ClaimStatus status);
}
package com.reimbursement.reimbursementportal.repository;

import com.reimbursement.reimbursementportal.entity.Claim;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ClaimRepository extends JpaRepository<Claim, Long> {
}
package com.reimbursement.reimbursementportal.mapper;


import com.reimbursement.reimbursementportal.dto.request.ClaimRequestDTO;
import com.reimbursement.reimbursementportal.dto.response.ClaimResponseDTO;
import com.reimbursement.reimbursementportal.entity.Claim;
import com.reimbursement.reimbursementportal.entity.User;
import com.reimbursement.reimbursementportal.enums.ClaimStatus;

import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * Mapper for Claim entity.
 */
public class ClaimMapper {

    /**
     * Converts Claim entity to ClaimResponseDTO.
     *
     * @param claim the claim entity
     * @return the claim response DTO
     */
    public static ClaimResponseDTO toResponse(Claim claim) {

        return ClaimResponseDTO.builder()
                .id(claim.getId())
                .amount(claim.getAmount() != null ? claim.getAmount().doubleValue() : 0.0)
                .description(claim.getDescription())
                .date(claim.getDate())
                .status(claim.getStatus())
                .employeeId(claim.getEmployee() != null ? claim.getEmployee().getId() : null)
                .employeeName(claim.getEmployee() != null ? claim.getEmployee().getName() : null)
                .reviewerId(claim.getReviewer() != null ? claim.getReviewer().getId() : null)
                .reviewerName(claim.getReviewer() != null ? claim.getReviewer().getName() : null)
                .comment(claim.getComment())
                .build();
    }

    /**
     * Converts ClaimRequestDTO to Claim entity.
     *
     * @param request the claim request
     * @param employee the employee
     * @param reviewer the reviewer
     * @return the claim entity
     */
    public static Claim toEntity(ClaimRequestDTO request, User employee, User reviewer) {

        Claim claim = new Claim();
        claim.setAmount(BigDecimal.valueOf(request.getAmount()));
        claim.setDescription(request.getDescription());
        claim.setDate(LocalDate.now());
        claim.setStatus(ClaimStatus.SUBMITTED);
        claim.setEmployee(employee);
        claim.setReviewer(reviewer);

        return claim;
    }
}

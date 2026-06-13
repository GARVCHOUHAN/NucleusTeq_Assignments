package com.reimbursement.reimbursementportal.dto.response;

import com.reimbursement.reimbursementportal.enums.ClaimStatus;
import com.reimbursement.reimbursementportal.enums.Role;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDate;

/**
 * Response DTO for claim details.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ClaimResponseDTO {

    private Long id;
    private Double amount;
    private String description;
    private LocalDate date;
    private ClaimStatus status;

    private Long employeeId;
    private String employeeName;

    private Long reviewerId;
    private String reviewerName;
    private Role reviewerRole;

    private String comment;
}

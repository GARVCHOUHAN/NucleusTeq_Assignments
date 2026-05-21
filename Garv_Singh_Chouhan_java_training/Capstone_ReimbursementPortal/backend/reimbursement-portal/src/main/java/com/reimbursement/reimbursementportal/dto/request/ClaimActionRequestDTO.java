package com.reimbursement.reimbursementportal.dto.request;

import com.reimbursement.reimbursementportal.enums.ClaimStatus;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Data;

/**
 * Request DTO for claim approval or rejection.
 */
@Data
public class ClaimActionRequestDTO {

    /**
     * Claim status to be applied.
     */
    @NotNull(message = "Status is required")
    private ClaimStatus status;

    /**
     * Optional comment for the action.
     */
    @Size(max = 500, message = "Comment must not exceed 500 characters")
    private String comment;
}

package com.reimbursement.reimbursementportal.dto.request;

import jakarta.validation.constraints.*;
import lombok.Data;

/**
 * Request DTO for claim submission.
 */
@Data
public class ClaimRequestDTO {

    /**
     * Claim amount.
     */
    @NotNull(message = "Amount is required")
    @Positive(message = "Amount must be greater than 0")
    private Double amount;

    /**
     * Claim description.
     */
    @NotBlank(message = "Description is required")
    @Size(max = 255, message = "Description must not exceed 255 characters")
    private String description;

    /**
     * Employee ID submitting the claim.
     */
    @NotNull(message = "Employee ID is required")
    @Positive(message = "Employee ID must be a positive number")
    private Long employeeId;
}

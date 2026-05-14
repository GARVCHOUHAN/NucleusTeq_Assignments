package com.reimbursement.reimbursementportal.dto;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import java.math.BigDecimal;
import java.time.LocalDate;
import lombok.Data;

/**
 * DTO for user login requests.
 */
@Data
class LoginRequest {

    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;

    @NotBlank(message = "Password is required")
    private String password;
}

/**
 * DTO for creating a new user (Admin only).
 */
@Data
class CreateUserRequest {

    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100, message = "Name must be 2–100 characters")
    private String name;

    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    @Pattern(
            regexp = "^[a-zA-Z0-9._%+\\-]+@company\\.com$",
            message = "Email must be a valid @company.com address"
    )
    private String email;

    @NotBlank(message = "Password is required")
    @Size(min = 8, message = "Password must be at least 8 characters")
    private String password;

    @NotBlank(message = "Role is required")
    @Pattern(regexp = "ADMIN|MANAGER|EMPLOYEE", message = "Role must be ADMIN, MANAGER, or EMPLOYEE")
    private String role;
}

/**
 * DTO for submitting a reimbursement claim.
 */
@Data
class SubmitClaimRequest {

    @NotNull(message = "Amount is required")
    @DecimalMin(value = "0.01", message = "Amount must be greater than zero")
    private BigDecimal amount;

    @NotNull(message = "Claim date is required")
    private LocalDate claimDate;

    @NotBlank(message = "Description is required")
    @Size(min = 10, max = 500, message = "Description must be 10–500 characters")
    private String description;
}

/**
 * DTO for approving or rejecting a claim.
 */
@Data
class ReviewClaimRequest {

    @Size(max = 500, message = "Comment must not exceed 500 characters")
    private String comment;
}

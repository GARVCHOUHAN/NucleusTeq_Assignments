package com.reimbursement.reimbursementportal.dto.request;

import com.reimbursement.reimbursementportal.enums.Role;
import jakarta.validation.constraints.*;
import lombok.Data;

/**
 * Request DTO for user creation.
 */
@Data
public class UserRequestDTO {

    /**
     * User name.
     */
    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 30, message = "Name must be between 2 and 30 characters")
    @Pattern(regexp = "^[A-Za-z\\s]+$", message = "Name must contain only letters and spaces")
    private String name;

    /**
     * User email.
     */
    @Email(message = "Invalid email format")
    @NotBlank(message = "Email is required")
    @Size(max = 30, message = "Email must not exceed 30 characters")
    private String email;

    /**
     * User password.
     */
    @NotBlank(message = "Password is required")
    @Size(min = 6, message = "Password must be at least 6 characters")
    private String password;

    /**
     * User role.
     */
    @NotNull(message = "Role is required")
    private Role role;

    /**
     * Manager ID for employee users.
     */
    @Positive(message = "Manager ID must be a positive number")
    private Long managerId;
}

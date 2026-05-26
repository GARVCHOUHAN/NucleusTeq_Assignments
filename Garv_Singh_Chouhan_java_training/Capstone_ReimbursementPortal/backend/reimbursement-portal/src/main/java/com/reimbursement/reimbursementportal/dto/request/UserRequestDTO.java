package com.reimbursement.reimbursementportal.dto.request;

import com.reimbursement.reimbursementportal.enums.Role;
import lombok.Data;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Size;

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

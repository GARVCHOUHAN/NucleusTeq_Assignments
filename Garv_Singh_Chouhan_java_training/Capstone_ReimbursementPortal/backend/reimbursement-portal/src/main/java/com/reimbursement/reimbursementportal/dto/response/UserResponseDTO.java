package com.reimbursement.reimbursementportal.dto.response;

import com.reimbursement.reimbursementportal.enums.Role;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;


/**
 * Response DTO for user details.
 */
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class UserResponseDTO {

    private Long id;
    private String name;
    private String email;
    private Role role;

    // Include manager info so the frontend can show "Reports to X"
    private Long managerId;
    private String managerName;
}

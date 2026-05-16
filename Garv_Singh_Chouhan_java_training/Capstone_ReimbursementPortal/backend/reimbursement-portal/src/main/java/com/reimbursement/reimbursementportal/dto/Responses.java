package com.reimbursement.reimbursementportal.dto;


import com.reimbursement.reimbursementportal.enums.ClaimStatus;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import lombok.Builder;
import lombok.Data;

/**
 * Response DTO for authentication token.
 */
@Data
@Builder
class AuthResponse {

    private String token;
    private String type;
    private Long userId;
    private String name;
    private String email;
    private String role;
}

/**
 * Response DTO for user details.
 */
@Data
@Builder
class UserResponse {

    private Long id;
    private String name;
    private String email;
    private String role;
    private Long managerId;
    private String managerName;
    private LocalDateTime createdAt;
}

/**
 * Response DTO for claim details.
 */
@Data
@Builder
class ClaimResponse {

    private Long id;
    private BigDecimal amount;
    private LocalDate claimDate;
    private String description;
    private ClaimStatus status;
    private String reviewerComment;
    private Long employeeId;
    private String employeeName;
    private Long reviewerId;
    private String reviewerName;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}

/**
 * Standard API error response envelope.
 */
@Data
@Builder
public class ErrorResponse {

    private int status;
    private String error;
    private String message;
    private String path;
    private LocalDateTime timestamp;
}

package com.reimbursement.reimbursementportal.exception;

import com.reimbursement.reimbursementportal.dto.StandardAPIResponse;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.stream.Collectors;

@RestControllerAdvice
public class GlobalExceptionHandler {
    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(BadRequestException.class)
    public ResponseEntity<StandardAPIResponse<Object>> handleBadRequest(BadRequestException ex) {
        log.error("Exception occurred: {}", ex.getMessage(), ex);
        return ResponseEntity.badRequest().body(
                StandardAPIResponse.builder()
                        .success(false)
                        .message(ex.getMessage())
                        .data(null)
                        .build()
        );
    }

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<StandardAPIResponse<Object>> handleNotFound(ResourceNotFoundException ex) {
        log.error("Exception occurred: {}", ex.getMessage(), ex);
        return ResponseEntity.status(404).body(
                StandardAPIResponse.builder()
                        .success(false)
                        .message(ex.getMessage())
                        .data(null)
                        .build()
        );
    }

    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<StandardAPIResponse<Object>> handleUserNotFound(UserNotFoundException ex) {
        log.error("Exception occurred: {}", ex.getMessage(), ex);
        return ResponseEntity.status(404).body(
                StandardAPIResponse.builder()
                        .success(false)
                        .message(ex.getMessage())
                        .data(null)
                        .build()
        );
    }

    @ExceptionHandler(ClaimNotFoundException.class)
    public ResponseEntity<StandardAPIResponse<Object>> handleClaimNotFound(ClaimNotFoundException ex) {
        log.error("Exception occurred: {}", ex.getMessage(), ex);
        return ResponseEntity.status(404).body(
                StandardAPIResponse.builder()
                        .success(false)
                        .message(ex.getMessage())
                        .data(null)
                        .build()
        );
    }

    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<StandardAPIResponse<Object>> handleBusinessValidation(ValidationException ex) {
        log.error("Exception occurred: {}", ex.getMessage(), ex);
        return ResponseEntity.badRequest().body(
                StandardAPIResponse.builder()
                        .success(false)
                        .message(ex.getMessage())
                        .data(null)
                        .build()
        );
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    public ResponseEntity<StandardAPIResponse<Object>> handleDataIntegrity(DataIntegrityViolationException ex) {
        log.error("Database operation failed {}", ex.getMessage(), ex);
        return ResponseEntity.badRequest().body(
                StandardAPIResponse.builder()
                        .success(false)
                        .message("Cannot delete this user because they have existing claims in the system. Please delete their claims first.")
                        .data(null)
                        .build()
        );
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<StandardAPIResponse<Object>> handleValidation(MethodArgumentNotValidException ex) {
        String message = ex.getBindingResult().getFieldErrors().stream()
                .map(FieldError::getDefaultMessage)
                .collect(Collectors.joining(", "));

        log.error("Exception occurred: {}", message, ex);
        return ResponseEntity.badRequest().body(
                StandardAPIResponse.builder()
                        .success(false)
                        .message(message)
                        .data(null)
                        .build()
        );
    }

    @ExceptionHandler(BadCredentialsException.class)
    public ResponseEntity<StandardAPIResponse<Object>> handleBadCredentials(BadCredentialsException ex) {
        log.warn("Invalid credentials: {}", ex.getMessage());
        return ResponseEntity.status(401).body(
                StandardAPIResponse.builder()
                        .success(false)
                        .message("Invalid email or password")
                        .data(null)
                        .build()
        );
    }

    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<StandardAPIResponse<Object>> handleAccessDenied(AccessDeniedException ex) {
        log.warn("Unauthorized access detected: {}", ex.getMessage());
        return ResponseEntity.status(403).body(
                StandardAPIResponse.builder()
                        .success(false)
                        .message("You do not have permission to perform this action")
                        .data(null)
                        .build()
        );
    }

    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<StandardAPIResponse<Object>> handleRuntime(RuntimeException ex) {
        log.error("Exception occurred: {}", ex.getMessage(), ex);
        return ResponseEntity.internalServerError().body(
                StandardAPIResponse.builder()
                        .success(false)
                        .message("Something went wrong: " + ex.getMessage())
                        .data(null)
                        .build()
        );
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<StandardAPIResponse<Object>> handleGeneric(Exception ex) {
        log.error("Exception occurred: {}", ex.getMessage(), ex);
        return ResponseEntity.internalServerError().body(
                StandardAPIResponse.builder()
                        .success(false)
                        .message("Something went wrong: " + ex.getMessage())
                        .data(null)
                        .build()
        );
    }

}

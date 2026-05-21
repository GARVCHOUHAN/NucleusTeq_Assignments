package com.reimbursement.reimbursementportal.exception;

//import com.reimbursement.reimbursementportal.dto.*;
//import jakarta.servlet.http.HttpServletRequest;
//import java.time.LocalDateTime;
//import java.util.stream.Collectors;
//import org.springframework.http.HttpStatus;
//import org.springframework.http.ResponseEntity;
//import org.springframework.security.access.AccessDeniedException;
//import org.springframework.security.authentication.BadCredentialsException;
//import org.springframework.validation.FieldError;
//import org.springframework.web.bind.MethodArgumentNotValidException;
//import org.springframework.web.bind.annotation.ExceptionHandler;
//import org.springframework.web.bind.annotation.RestControllerAdvice;
//
///**
// * Centralized exception handling for all controllers.
// */
//@RestControllerAdvice
//public class GlobalExceptionHandler {
//
//    @ExceptionHandler(ResourceNotFoundException.class)
//    public ResponseEntity<ErrorResponse> handleNotFound(
//            ResourceNotFoundException ex, HttpServletRequest req) {
//        return buildResponse(HttpStatus.NOT_FOUND, "Not Found", ex.getMessage(), req);
//    }
//
//    @ExceptionHandler(BusinessException.class)
//    public ResponseEntity<ErrorResponse> handleBusiness(
//            BusinessException ex, HttpServletRequest req) {
//        return buildResponse(HttpStatus.BAD_REQUEST, "Bad Request", ex.getMessage(), req);
//    }
//
//    @ExceptionHandler(MethodArgumentNotValidException.class)
//    public ResponseEntity<ErrorResponse> handleValidation(
//            MethodArgumentNotValidException ex, HttpServletRequest req) {
//        String message = ex.getBindingResult().getFieldErrors().stream()
//                .map(FieldError::getDefaultMessage)
//                .collect(Collectors.joining(", "));
//        return buildResponse(HttpStatus.BAD_REQUEST, "Validation Failed", message, req);
//    }
//
//    @ExceptionHandler(AccessDeniedException.class)
//    public ResponseEntity<ErrorResponse> handleAccessDenied(
//            AccessDeniedException ex, HttpServletRequest req) {
//        return buildResponse(HttpStatus.FORBIDDEN, "Forbidden",
//                "You do not have permission to perform this action", req);
//    }
//
//    @ExceptionHandler(BadCredentialsException.class)
//    public ResponseEntity<ErrorResponse> handleBadCredentials(
//            BadCredentialsException ex, HttpServletRequest req) {
//        return buildResponse(HttpStatus.UNAUTHORIZED, "Unauthorized", "Invalid email or password", req);
//    }
//
//    @ExceptionHandler(Exception.class)
//    public ResponseEntity<ErrorResponse> handleGeneric(Exception ex, HttpServletRequest req) {
//        return buildResponse(HttpStatus.INTERNAL_SERVER_ERROR, "Internal Server Error",
//                "An unexpected error occurred", req);
//    }
//
//    private ResponseEntity<ErrorResponse> buildResponse(
//            HttpStatus status, String error, String message, HttpServletRequest req) {
//        ErrorResponse body = ErrorResponse.builder()
//                .status(status.value())
//                .error(error)
//                .message(message)
//                .path(req.getRequestURI())
//                .timestamp(LocalDateTime.now())
//                .build();
//        return ResponseEntity.status(status).body(body);
//    }
//}


import com.reimbursement.reimbursementportal.dto.StandardAPIResponse;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.stream.Collectors;

@ControllerAdvice
public class GlobalExceptionHandler {
    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(BadRequestException.class)
    public ResponseEntity<StandardAPIResponse<Object>> handleBadRequest(BadRequestException ex) {
        log.error("Bad Request Error: {}", ex.getMessage());
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
        return ResponseEntity.status(404).body(
                StandardAPIResponse.builder()
                        .success(false)
                        .message(ex.getMessage())
                        .data(null)
                        .build()
        );
    }

    @ExceptionHandler(DataIntegrityViolationException.class)
    public ResponseEntity<StandardAPIResponse<Object>> handleDataIntegrity(DataIntegrityViolationException ex) {
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
        return ResponseEntity.status(403).body(
                StandardAPIResponse.builder()
                        .success(false)
                        .message("You do not have permission to perform this action")
                        .data(null)
                        .build()
        );
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<StandardAPIResponse<Object>> handleGeneric(Exception ex) {
        log.error("Something went wrong", ex);
        return ResponseEntity.internalServerError().body(
                StandardAPIResponse.builder()
                        .success(false)
                        .message("Something went wrong: " + ex.getMessage())
                        .data(null)
                        .build()
        );
    }

}

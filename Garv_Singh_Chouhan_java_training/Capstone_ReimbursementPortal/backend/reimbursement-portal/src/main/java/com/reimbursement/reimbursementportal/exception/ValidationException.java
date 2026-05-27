package com.reimbursement.reimbursementportal.exception;

/**
 * Raised for business validation failures that are not tied to a DTO field.
 */
public class ValidationException extends RuntimeException {

    public ValidationException(String message) {
        super(message);
    }
}

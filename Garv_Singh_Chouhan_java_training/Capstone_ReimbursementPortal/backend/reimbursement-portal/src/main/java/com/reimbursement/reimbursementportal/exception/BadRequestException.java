package com.reimbursement.reimbursementportal.exception;

/**
 * Exception for invalid client requests.
 */
public class BadRequestException extends RuntimeException {

    /**
     * Constructs a new BadRequestException.
     *
     * @param message the error message
     */
    public BadRequestException(String message) {
        super(message);
    }
}

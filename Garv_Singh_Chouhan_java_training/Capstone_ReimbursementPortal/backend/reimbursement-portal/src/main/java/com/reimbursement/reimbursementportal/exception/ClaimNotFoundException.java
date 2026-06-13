package com.reimbursement.reimbursementportal.exception;

/**
 * Raised when a requested reimbursement claim cannot be found.
 */
public class ClaimNotFoundException extends ResourceNotFoundException {

    public ClaimNotFoundException(String message) {
        super(message);
    }
}

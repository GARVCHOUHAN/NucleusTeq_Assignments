package com.reimbursement.reimbursementportal.exception;

/**
 * Raised when a requested user record cannot be found.
 */
public class UserNotFoundException extends ResourceNotFoundException {

    public UserNotFoundException(String message) {
        super(message);
    }
}

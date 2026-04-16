package com.session2.usermanagement.exception;
// Custom exception for better error handling

public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String message) {
        super(message);
    }
}

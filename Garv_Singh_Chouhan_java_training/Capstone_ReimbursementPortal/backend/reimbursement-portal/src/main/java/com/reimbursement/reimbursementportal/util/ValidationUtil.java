package com.reimbursement.reimbursementportal.util;
/**
 * this is a utility class for validation methods.
 */
public class ValidationUtil {

    /**
     * Validates if the email belongs to the company domain.
     *
     * @param email the email address
     * @return true if valid, otherwise false
     */
    public static boolean isValidCompanyEmail(String email) {
        if (email == null) return false;

        return email.trim().toLowerCase().endsWith("@company.com");
    }
}
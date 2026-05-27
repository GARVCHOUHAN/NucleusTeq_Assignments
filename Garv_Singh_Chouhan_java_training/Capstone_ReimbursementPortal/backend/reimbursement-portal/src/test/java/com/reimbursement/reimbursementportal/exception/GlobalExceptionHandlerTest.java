package com.reimbursement.reimbursementportal.exception;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;

import com.reimbursement.reimbursementportal.dto.StandardAPIResponse;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.boot.test.system.CapturedOutput;
import org.springframework.boot.test.system.OutputCaptureExtension;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.authentication.BadCredentialsException;

@ExtendWith(OutputCaptureExtension.class)
class GlobalExceptionHandlerTest {

    private final GlobalExceptionHandler handler = new GlobalExceptionHandler();

    @Test
    void handlesUserNotFound(CapturedOutput output) {
        ResponseEntity<StandardAPIResponse<Object>> response =
                handler.handleUserNotFound(new UserNotFoundException("User missing"));

        assertEquals(404, response.getStatusCode().value());
        assertEquals("User missing", response.getBody().getMessage());
        assertThat(output).contains("Exception occurred: User missing");
    }

    @Test
    void handlesClaimNotFound() {
        ResponseEntity<StandardAPIResponse<Object>> response =
                handler.handleClaimNotFound(new ClaimNotFoundException("Claim missing"));

        assertEquals(404, response.getStatusCode().value());
        assertEquals("Claim missing", response.getBody().getMessage());
    }

    @Test
    void handlesValidationException() {
        ResponseEntity<StandardAPIResponse<Object>> response =
                handler.handleBusinessValidation(new ValidationException("Invalid data"));

        assertEquals(400, response.getStatusCode().value());
        assertEquals("Invalid data", response.getBody().getMessage());
    }

    @Test
    void handlesBadCredentialsAndAccessDenied() {
        ResponseEntity<StandardAPIResponse<Object>> unauthorized =
                handler.handleBadCredentials(new BadCredentialsException("bad"));
        ResponseEntity<StandardAPIResponse<Object>> forbidden =
                handler.handleAccessDenied(new AccessDeniedException("denied"));

        assertEquals(401, unauthorized.getStatusCode().value());
        assertEquals("Invalid email or password", unauthorized.getBody().getMessage());
        assertEquals(403, forbidden.getStatusCode().value());
    }

    @Test
    void handlesRuntimeAndGenericExceptions() {
        ResponseEntity<StandardAPIResponse<Object>> runtime =
                handler.handleRuntime(new RuntimeException("runtime"));
        ResponseEntity<StandardAPIResponse<Object>> generic =
                handler.handleGeneric(new Exception("generic"));

        assertEquals(500, runtime.getStatusCode().value());
        assertEquals("Something went wrong: runtime", runtime.getBody().getMessage());
        assertEquals(500, generic.getStatusCode().value());
    }
}

package com.reimbursement.reimbursementportal.config;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.boot.test.system.CapturedOutput;
import org.springframework.boot.test.system.OutputCaptureExtension;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.TestingAuthenticationToken;
import org.springframework.security.authentication.event.AuthenticationFailureBadCredentialsEvent;
import org.springframework.security.authentication.event.AuthenticationSuccessEvent;

@ExtendWith(OutputCaptureExtension.class)
class AuthServiceTest {

    private final SecurityEventListener listener = new SecurityEventListener();

    @Test
    void logsAuthenticationSuccess(CapturedOutput output) {
        listener.onAuthenticationSuccess(new AuthenticationSuccessEvent(
                new TestingAuthenticationToken("employee@company.com", "secret1", List.of())));

        assertThat(output).contains("User logged in successfully: employee@company.com");
    }

    @Test
    void logsAuthenticationFailure(CapturedOutput output) {
        listener.onAuthenticationFailure(new AuthenticationFailureBadCredentialsEvent(
                new TestingAuthenticationToken("employee@company.com", "bad", List.of()),
                new BadCredentialsException("bad")));

        assertThat(output).contains("Failed login attempt: employee@company.com");
    }
}

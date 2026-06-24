package com.reimbursement.reimbursementportal.config;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.when;

import com.reimbursement.reimbursementportal.entity.User;
import com.reimbursement.reimbursementportal.enums.Role;
import com.reimbursement.reimbursementportal.repository.UserRepository;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.boot.test.system.CapturedOutput;
import org.springframework.boot.test.system.OutputCaptureExtension;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;

@ExtendWith({MockitoExtension.class, OutputCaptureExtension.class})
class CustomUserDetailsServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private CustomUserDetailsService customUserDetailsService;

    @Test
    void loadUserByUsernameReturnsUserDetails(CapturedOutput output) {
        User user = User.builder()
                .email("manager@company.com")
                .password("encoded")
                .role(Role.MANAGER)
                .build();
        when(userRepository.findByEmail("manager@company.com")).thenReturn(Optional.of(user));

        UserDetails details = customUserDetailsService.loadUserByUsername("manager@company.com");

        assertEquals("manager@company.com", details.getUsername());
        assertEquals("encoded", details.getPassword());
        assertEquals("ROLE_MANAGER", details.getAuthorities().iterator().next().getAuthority());
        org.assertj.core.api.Assertions.assertThat(output).contains("User login attempt: manager@company.com");
    }

    @Test
    void loadUserByUsernameThrowsWhenMissing(CapturedOutput output) {
        when(userRepository.findByEmail("missing@company.com")).thenReturn(Optional.empty());

        assertThrows(UsernameNotFoundException.class,
                () -> customUserDetailsService.loadUserByUsername("missing@company.com"));
        org.assertj.core.api.Assertions.assertThat(output).contains("Invalid credentials for email");
    }
}

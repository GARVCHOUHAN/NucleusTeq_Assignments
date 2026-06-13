package com.reimbursement.reimbursementportal.config;

import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.httpBasic;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.reimbursement.reimbursementportal.entity.User;
import com.reimbursement.reimbursementportal.dto.response.ClaimResponseDTO;
import com.reimbursement.reimbursementportal.dto.response.PageResponseDTO;
import com.reimbursement.reimbursementportal.enums.Role;
import com.reimbursement.reimbursementportal.repository.ClaimRepository;
import com.reimbursement.reimbursementportal.repository.UserRepository;
import com.reimbursement.reimbursementportal.service.ClaimService;
import com.reimbursement.reimbursementportal.service.UserService;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class SecurityConfigTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private BCryptPasswordEncoder passwordEncoder;

    @MockitoBean
    private UserRepository userRepository;

    @MockitoBean
    private ClaimRepository claimRepository;

    @MockitoBean
    private UserService userService;

    @MockitoBean
    private ClaimService claimService;

    @MockitoBean
    private PasswordMigrationRunner passwordMigrationRunner;

    @Test
    void unauthenticatedProtectedRequestIsUnauthorized() throws Exception {
        mockMvc.perform(get("/api/users"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    void invalidCredentialsAreUnauthorized() throws Exception {
        when(userRepository.findByEmail("admin@company.com"))
                .thenReturn(Optional.of(user(Role.ADMIN, "secret1")));

        mockMvc.perform(get("/api/users")
                        .with(httpBasic("admin@company.com", "wrong")))
                .andExpect(status().isUnauthorized());
    }

    @Test
    void adminCanAccessUserEndpoints() throws Exception {
        when(userRepository.findByEmail("admin@company.com"))
                .thenReturn(Optional.of(user(Role.ADMIN, "secret1")));
        when(userService.getAllUsers()).thenReturn(List.of());

        mockMvc.perform(get("/api/users")
                        .with(httpBasic("admin@company.com", "secret1")))
                .andExpect(status().isOk());
    }

    @Test
    void managerIsForbiddenFromAdminUserEndpoints() throws Exception {
        when(userRepository.findByEmail("manager@company.com"))
                .thenReturn(Optional.of(user(Role.MANAGER, "secret1")));

        mockMvc.perform(get("/api/users")
                        .with(httpBasic("manager@company.com", "secret1")))
                .andExpect(status().isForbidden());
    }

    @Test
    void employeeCanAccessClaimEndpoints() throws Exception {
        when(userRepository.findByEmail("employee@company.com"))
                .thenReturn(Optional.of(user(Role.EMPLOYEE, "secret1")));
        when(claimService.getAllClaims(0, 10)).thenReturn(emptyClaimPage());

        mockMvc.perform(get("/api/claims")
                        .with(httpBasic("employee@company.com", "secret1")))
                .andExpect(status().isOk());
    }

    private User user(Role role, String password) {
        return User.builder()
                .id(1L)
                .name(role.name())
                .email(role.name().toLowerCase() + "@company.com")
                .password(passwordEncoder.encode(password))
                .role(role)
                .build();
    }

    private PageResponseDTO<ClaimResponseDTO> emptyClaimPage() {
        return PageResponseDTO.<ClaimResponseDTO>builder()
                .content(List.of())
                .page(0)
                .size(10)
                .totalElements(0L)
                .totalPages(0)
                .first(true)
                .last(true)
                .build();
    }
}

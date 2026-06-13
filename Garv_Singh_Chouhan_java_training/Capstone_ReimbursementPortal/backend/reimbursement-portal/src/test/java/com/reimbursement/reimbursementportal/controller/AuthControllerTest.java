package com.reimbursement.reimbursementportal.controller;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.user;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.reimbursement.reimbursementportal.config.PasswordMigrationRunner;
import com.reimbursement.reimbursementportal.dto.request.UserRequestDTO;
import com.reimbursement.reimbursementportal.dto.response.UserResponseDTO;
import com.reimbursement.reimbursementportal.entity.User;
import com.reimbursement.reimbursementportal.enums.Role;
import com.reimbursement.reimbursementportal.repository.ClaimRepository;
import com.reimbursement.reimbursementportal.repository.UserRepository;
import com.reimbursement.reimbursementportal.service.UserService;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class AuthControllerTest {

    @Autowired
    private MockMvc mockMvc;

    private final ObjectMapper objectMapper = new ObjectMapper();

    @MockitoBean
    private UserService userService;

    @MockitoBean
    private UserRepository userRepository;

    @MockitoBean
    private ClaimRepository claimRepository;

    @MockitoBean
    private PasswordMigrationRunner passwordMigrationRunner;

    @Test
    void publicEmployeeSignupSucceeds() throws Exception {
        UserRequestDTO request = userRequest(Role.EMPLOYEE);
        when(userService.createUser(any(UserRequestDTO.class))).thenReturn(userResponse());

        mockMvc.perform(post("/api/auth/signup")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message").value("User registered successfully"));
    }

    @Test
    void publicSignupRejectsAdminRole() throws Exception {
        mockMvc.perform(post("/api/auth/signup")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(userRequest(Role.ADMIN))))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.success").value(false));
    }

    @Test
    void authenticatedUserCanFetchProfile() throws Exception {
        User user = User.builder()
                .id(1L)
                .name("Employee")
                .email("employee@company.com")
                .role(Role.EMPLOYEE)
                .build();
        when(userRepository.findByEmail("employee@company.com")).thenReturn(Optional.of(user));

        mockMvc.perform(get("/api/auth/me").with(user("employee@company.com").roles("EMPLOYEE")))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.data.email").value("employee@company.com"));
    }

    @Test
    void unauthenticatedProfileRequestIsUnauthorized() throws Exception {
        mockMvc.perform(get("/api/auth/me"))
                .andExpect(status().isUnauthorized());
    }

    private UserRequestDTO userRequest(Role role) {
        UserRequestDTO request = new UserRequestDTO();
        request.setName("Employee");
        request.setEmail("employee@company.com");
        request.setPassword("secret1");
        request.setRole(role);
        return request;
    }

    private UserResponseDTO userResponse() {
        return UserResponseDTO.builder()
                .id(1L)
                .name("Employee")
                .email("employee@company.com")
                .role(Role.EMPLOYEE)
                .build();
    }
}

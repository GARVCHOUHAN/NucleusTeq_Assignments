package com.reimbursement.reimbursementportal.controller;

import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.user;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.reimbursement.reimbursementportal.config.PasswordMigrationRunner;
import com.reimbursement.reimbursementportal.dto.request.UserRequestDTO;
import com.reimbursement.reimbursementportal.dto.response.UserResponseDTO;
import com.reimbursement.reimbursementportal.enums.Role;
import com.reimbursement.reimbursementportal.repository.ClaimRepository;
import com.reimbursement.reimbursementportal.repository.UserRepository;
import com.reimbursement.reimbursementportal.service.UserService;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class UserControllerTest {

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
    void adminCanCreateUser() throws Exception {
        UserRequestDTO request = userRequest();
        when(userService.createUser(request)).thenReturn(userResponse(1L, Role.EMPLOYEE));

        mockMvc.perform(post("/api/users")
                        .with(user("admin@company.com").roles("ADMIN"))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.success").value(true))
                .andExpect(jsonPath("$.data.email").value("employee@company.com"));
    }

    @Test
    void employeeCannotFetchUsers() throws Exception {
        mockMvc.perform(get("/api/users").with(user("employee@company.com").roles("EMPLOYEE")))
                .andExpect(status().isForbidden());
    }

    @Test
    void unauthenticatedUserListIsUnauthorized() throws Exception {
        mockMvc.perform(get("/api/users"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    void adminCanFetchAndAssignAndDeleteUsers() throws Exception {
        when(userService.getAllUsers()).thenReturn(List.of(userResponse(1L, Role.EMPLOYEE)));
        when(userService.getUserById(1L)).thenReturn(userResponse(1L, Role.EMPLOYEE));
        when(userService.assignManager(1L, 2L)).thenReturn(userResponse(1L, Role.EMPLOYEE));
        doNothing().when(userService).deleteUser(1L);

        mockMvc.perform(get("/api/users").with(user("admin@company.com").roles("ADMIN")))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.data[0].id").value(1L));

        mockMvc.perform(get("/api/users/1").with(user("admin@company.com").roles("ADMIN")))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.data.id").value(1L));

        mockMvc.perform(put("/api/users/1/manager")
                        .param("managerId", "2")
                        .with(user("admin@company.com").roles("ADMIN")))
                .andExpect(status().isOk());

        mockMvc.perform(delete("/api/users/1").with(user("admin@company.com").roles("ADMIN")))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.data").value("User deleted with id: 1"));
    }

    private UserRequestDTO userRequest() {
        UserRequestDTO request = new UserRequestDTO();
        request.setName("Employee");
        request.setEmail("employee@company.com");
        request.setPassword("secret1");
        request.setRole(Role.EMPLOYEE);
        return request;
    }

    private UserResponseDTO userResponse(Long id, Role role) {
        return UserResponseDTO.builder()
                .id(id)
                .name("Employee")
                .email("employee@company.com")
                .role(role)
                .managerId(2L)
                .managerName("Manager")
                .build();
    }
}

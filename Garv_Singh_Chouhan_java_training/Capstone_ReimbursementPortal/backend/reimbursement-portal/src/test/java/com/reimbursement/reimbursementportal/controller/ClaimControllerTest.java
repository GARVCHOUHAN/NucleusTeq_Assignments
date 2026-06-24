package com.reimbursement.reimbursementportal.controller;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.user;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.reimbursement.reimbursementportal.config.PasswordMigrationRunner;
import com.reimbursement.reimbursementportal.dto.request.ClaimActionRequestDTO;
import com.reimbursement.reimbursementportal.dto.request.ClaimRequestDTO;
import com.reimbursement.reimbursementportal.dto.response.ClaimResponseDTO;
import com.reimbursement.reimbursementportal.dto.response.PageResponseDTO;
import com.reimbursement.reimbursementportal.enums.ClaimStatus;
import com.reimbursement.reimbursementportal.repository.ClaimRepository;
import com.reimbursement.reimbursementportal.repository.UserRepository;
import com.reimbursement.reimbursementportal.service.ClaimService;
import java.time.LocalDate;
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
class ClaimControllerTest {

    @Autowired
    private MockMvc mockMvc;

    private final ObjectMapper objectMapper = new ObjectMapper();

    @MockitoBean
    private ClaimService claimService;

    @MockitoBean
    private UserRepository userRepository;

    @MockitoBean
    private ClaimRepository claimRepository;

    @MockitoBean
    private PasswordMigrationRunner passwordMigrationRunner;

    @Test
    void employeeCanSubmitClaim() throws Exception {
        ClaimRequestDTO request = claimRequest();
        when(claimService.submitClaim(any(ClaimRequestDTO.class))).thenReturn(claimResponse());

        mockMvc.perform(post("/api/claims")
                        .with(user("employee@company.com").roles("EMPLOYEE"))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(claimRequestJson(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message").value("Claim submitted successfully"))
                .andExpect(jsonPath("$.data.status").value("SUBMITTED"));
    }

    @Test
    void invalidClaimRequestReturnsBadRequest() throws Exception {
        ClaimRequestDTO request = claimRequest();
        request.setAmount(-1.0);

        mockMvc.perform(post("/api/claims")
                        .with(user("employee@company.com").roles("EMPLOYEE"))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(claimRequestJson(request)))
                .andExpect(status().isBadRequest());
    }

    @Test
    void managerCanFetchReviewerClaimsAndTakeAction() throws Exception {
        when(claimService.getClaimsByReviewer(eq(2L), eq(0), eq(10))).thenReturn(pageResponse());
        when(claimService.takeAction(eq(10L), eq(2L), any(ClaimActionRequestDTO.class)))
                .thenReturn(claimResponse(ClaimStatus.APPROVED));

        mockMvc.perform(get("/api/claims/reviewer/2")
                        .with(user("manager@company.com").roles("MANAGER")))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.data.totalElements").value(1L));

        mockMvc.perform(put("/api/claims/10/action/2")
                        .with(user("manager@company.com").roles("MANAGER"))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(actionRequest())))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.data.status").value("APPROVED"));
    }

    @Test
    void unauthenticatedClaimRequestIsUnauthorized() throws Exception {
        mockMvc.perform(get("/api/claims"))
                .andExpect(status().isUnauthorized());
    }

    private ClaimRequestDTO claimRequest() {
        ClaimRequestDTO request = new ClaimRequestDTO();
        request.setAmount(200.0);
        request.setClaimDate(LocalDate.of(2026, 5, 1));
        request.setDescription("Taxi");
        request.setEmployeeId(1L);
        return request;
    }

    private ClaimActionRequestDTO actionRequest() {
        ClaimActionRequestDTO request = new ClaimActionRequestDTO();
        request.setStatus(ClaimStatus.APPROVED);
        request.setComment("Approved");
        return request;
    }

    private ClaimResponseDTO claimResponse() {
        return claimResponse(ClaimStatus.SUBMITTED);
    }

    private ClaimResponseDTO claimResponse(ClaimStatus status) {
        return ClaimResponseDTO.builder()
                .id(10L)
                .amount(200.0)
                .description("Taxi")
                .date(LocalDate.of(2026, 5, 1))
                .status(status)
                .employeeId(1L)
                .reviewerId(2L)
                .comment("Approved")
                .build();
    }

    private PageResponseDTO<ClaimResponseDTO> pageResponse() {
        return PageResponseDTO.<ClaimResponseDTO>builder()
                .content(List.of(claimResponse()))
                .page(0)
                .size(10)
                .totalElements(1L)
                .totalPages(1)
                .first(true)
                .last(true)
                .build();
    }

    private String claimRequestJson(ClaimRequestDTO request) {
        return """
                {
                  "amount": %s,
                  "claimDate": "%s",
                  "description": "%s",
                  "employeeId": %s
                }
                """.formatted(request.getAmount(), request.getClaimDate(),
                request.getDescription(), request.getEmployeeId());
    }
}

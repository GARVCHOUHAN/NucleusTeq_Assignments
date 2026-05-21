package com.reimbursement.reimbursementportal.controller;

import com.reimbursement.reimbursementportal.dto.request.UserRequestDTO;
import com.reimbursement.reimbursementportal.dto.response.UserResponseDTO;
import com.reimbursement.reimbursementportal.entity.User;
import com.reimbursement.reimbursementportal.mapper.UserMapper;
import com.reimbursement.reimbursementportal.repository.UserRepository;
import com.reimbursement.reimbursementportal.dto.StandardAPIResponse;
import com.reimbursement.reimbursementportal.service.UserService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;

import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

/**
 * Controller for authentication-related endpoints.
 */
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final UserRepository userRepository;
    private final UserService userService;

    /**
     * Registers a user from the public signup page.
     *
     * @param request user details including role and optional manager
     * @return the created user response DTO
     */
    @PostMapping("/signup")
    public ResponseEntity<StandardAPIResponse<UserResponseDTO>> signup(
            @Valid @RequestBody UserRequestDTO request) {

        UserResponseDTO response = userService.createUser(request);

        StandardAPIResponse<UserResponseDTO> apiResponse =
                StandardAPIResponse.<UserResponseDTO>builder()
                        .success(true)
                        .message("User registered successfully")
                        .data(response)
                        .build();

        return ResponseEntity.ok(apiResponse);
    }

    /**
     * Retrieves details of the currently authenticated user.
     *
     * @param authentication the authentication object containing user details
     * @return the authenticated user's response DTO
     */

    @GetMapping("/me")
    public ResponseEntity<StandardAPIResponse<UserResponseDTO>> me(Authentication authentication) {

        String email = authentication.getName();

        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("Logged-in user not found"));

        UserResponseDTO response = UserMapper.toResponse(user);

        StandardAPIResponse<UserResponseDTO> apiResponse =
                StandardAPIResponse.<UserResponseDTO>builder()
                        .success(true)
                        .message("User fetched successfully")
                        .data(response)
                        .build();

        return ResponseEntity.ok(apiResponse);
    }
}

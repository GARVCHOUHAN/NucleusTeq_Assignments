package com.reimbursement.reimbursementportal.mapper;

import com.reimbursement.reimbursementportal.dto.request.UserRequestDTO;
import com.reimbursement.reimbursementportal.dto.response.UserResponseDTO;
import com.reimbursement.reimbursementportal.entity.User;

/**
 * Mapper for User entity.
 */
public class UserMapper {

    /**
     * Converts User entity to UserResponseDTO.
     *
     * @param user the user entity
     * @return the user response DTO
     */
    public static UserResponseDTO toResponse(User user) {
        return UserResponseDTO.builder()
                .id(user.getId())
                .name(user.getName())
                .email(user.getEmail())
                .role(user.getRole())
                .managerId(user.getManager() != null ? user.getManager().getId() : null)
                .managerName(user.getManager() != null ? user.getManager().getName() : null)
                .build();
    }

    /**
     * Converts UserRequestDTO to User entity.
     *
     * @param request the user request DTO
     * @param encryptedPassword the encrypted password
     * @return the user entity
     */
    public static User toEntity(UserRequestDTO request, String encryptedPassword) {
        if (request == null) {
            return null;
        }

        User user = new User();
        user.setName(request.getName());
        user.setEmail(request.getEmail());
        user.setPassword(encryptedPassword);
        user.setRole(request.getRole());

        return user;
    }
}

package com.reimbursement.reimbursementportal.service;

import com.reimbursement.reimbursementportal.dto.request.UserRequestDTO;
import com.reimbursement.reimbursementportal.dto.response.UserResponseDTO;

import java.util.List;

/**
 * Service interface for user operations.
 */
public interface UserService {

    /**
     * Creates a new user.
     *
     * @param request the user request
     * @return the created user
     */
    UserResponseDTO createUser(UserRequestDTO request);

    /**
     * Retrieves all users.
     *
     * @return list of users
     */
    List<UserResponseDTO> getAllUsers();

    /**
     * Retrieves a user by ID.
     *
     * @param id the user ID
     * @return the user
     */
    UserResponseDTO getUserById(Long id);

    /**
     * Assigns or clears a manager for an employee.
     *
     * @param employeeId the employee user ID
     * @param managerId the manager user ID, or null to route claims to admin
     * @return the updated employee
     */
    UserResponseDTO assignManager(Long employeeId, Long managerId);

    /**
     * Retrieves employees by manager ID.
     *
     * @param managerId the manager ID
     * @return list of employees
     */
    List<UserResponseDTO> getEmployeesByManager(Long managerId);

    /**
     * Deletes a user by ID.
     *
     * @param id the user ID
     */
    void deleteUser(Long id);
}

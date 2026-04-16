package com.session2.usermanagement.service;

import com.session2.usermanagement.dto.UserRequestDTO;
import com.session2.usermanagement.model.User;
import com.session2.usermanagement.repository.UserRepository;
import com.session2.usermanagement.exception.UserNotFoundException;
import org.springframework.stereotype.Service;

import java.util.List;

// Service layer contains business logic
// No logic should be inside controller

@Service
public class UserService {

    private final UserRepository userRepository;

    // Constructor Injection (MANDATORY)
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    // Create user
    public User createUser(UserRequestDTO dto) {

        // Basic validation
        if (dto.getName() == null || dto.getEmail() == null) {
            throw new IllegalArgumentException("Name or Email cannot be null");
        }

        Long id = userRepository.generateId();

        User user = new User(id, dto.getName(), dto.getEmail());

        return userRepository.save(user);
    }

    // Get all users
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    // Get user by ID
    public User getUserById(Long id) {
        return userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException("User not found"));
    }
}
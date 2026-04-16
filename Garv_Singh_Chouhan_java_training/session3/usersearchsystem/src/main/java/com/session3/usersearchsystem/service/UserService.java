package com.session3.usersearchsystem.service;

import com.session3.usersearchsystem.dto.UserRequestDTO;
import com.session3.usersearchsystem.model.User;
import com.session3.usersearchsystem.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

// Business logic layer

@Service
public class UserService {

    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    // Search API logic
    public List<User> searchUsers(String name, Integer age, String role) {

        return userRepository.findAll().stream()
                .filter(u -> name == null || u.getName().equalsIgnoreCase(name))
                .filter(u -> age == null || u.getAge() == age)
                .filter(u -> role == null || u.getRole().equalsIgnoreCase(role))
                .collect(Collectors.toList());
    }

    // Submit API logic
    public User submitUser(UserRequestDTO dto) {

        if (dto.getName() == null || dto.getName().isEmpty() ||
                dto.getAge() == null ||
                dto.getRole() == null || dto.getRole().isEmpty()) {

            throw new IllegalArgumentException("Invalid input");
        }

        Long id = System.currentTimeMillis();

        User user = new User(id, dto.getName(), dto.getAge(), dto.getRole());

        userRepository.save(user);

        return user;
    }

    // Delete API logic
    public String deleteUser(Long id, Boolean confirm) {

        if (confirm == null || !confirm) {
            return "Confirmation required";
        }

        User user = userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("User not found"));

        userRepository.delete(user);

        return "User deleted successfully";
    }
}

package com.session2.usermanagement.controller;

import com.session2.usermanagement.dto.UserRequestDTO;
import com.session2.usermanagement.model.User;
import com.session2.usermanagement.service.UserService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

// Controller handles API requests
// No business logic should be written here

@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    // Constructor Injection
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // GET /users
    @GetMapping
    public List<User> getAllUsers() {
        return userService.getAllUsers();
    }

    // POST /users
    @PostMapping
    public User createUser(@RequestBody UserRequestDTO dto) {
        return userService.createUser(dto);
    }

    // GET /users/{id}
    @GetMapping("/{id}")
    public User getUserById(@PathVariable Long id) {
        return userService.getUserById(id);
    }
}
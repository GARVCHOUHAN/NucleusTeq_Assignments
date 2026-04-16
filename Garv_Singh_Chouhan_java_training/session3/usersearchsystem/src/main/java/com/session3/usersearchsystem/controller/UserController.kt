package com.session3.usersearchsystem.controller

import com.session3.usersearchsystem.dto.UserRequestDTO;
import com.session3.usersearchsystem.model.User;
import com.session3.usersearchsystem.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

// Controller layer handles API requests
// No business logic should be written here

@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    // Constructor injection (MANDATORY as per assignment)
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // SEARCH API
    // If params are null → returns all users
    @GetMapping("/search")
    public List<User> searchUsers(
    @RequestParam(required = false) String name,
    @RequestParam(required = false) Integer age,
    @RequestParam(required = false) String role) {

        return userService.searchUsers(name, age, role);
    }

    // SUBMIT API
    @PostMapping("/submit")
    public ResponseEntity<?> submitUser(@RequestBody UserRequestDTO dto) {

        try {
            User user = userService.submitUser(dto);

            // returning 201 CREATED
            return ResponseEntity.status(201).body(user);

        } catch (IllegalArgumentException e) {

            // returning 400 BAD REQUEST
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

    // DELETE API with confirmation
    @DeleteMapping("/{id}")
    public String deleteUser(
    @PathVariable Long id,
    @RequestParam(required = false) Boolean confirm) {

        return userService.deleteUser(id, confirm);
    }
}
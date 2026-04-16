package com.session3.usersearchsystem.controller

import com.session3.usersearchsystem.dto.UserRequestDTO
import com.session3.usersearchsystem.service.UserService
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import com.session3.usersearchsystem.model.User

// Controller layer handles API requests
// No business logic should be written here
@RestController
@RequestMapping("/users")
class UserController // Constructor injection (MANDATORY as per assignment)
    (private val userService: UserService) {
    // SEARCH API
    // If params are null → returns all users
    @GetMapping("/search")
    fun searchUsers(
        @RequestParam(required = false) name: String?,
        @RequestParam(required = false) age: Int?,
        @RequestParam(required = false) role: String?
    ): MutableList<User?> {
        return userService.searchUsers(name, age, role)
    }

    // SUBMIT API
    @PostMapping("/submit")
    fun submitUser(@RequestBody dto: UserRequestDTO?): ResponseEntity<*> {
        try {
            val user: User? = userService.submitUser(dto)

            // returning 201 CREATED
            return ResponseEntity.status(201).body<Any?>(user)
        } catch (e: IllegalArgumentException) {
            // returning 400 BAD REQUEST

            return ResponseEntity.badRequest().body<String?>(e.message)
        }
    }

    // DELETE API with confirmation
    @DeleteMapping("/{id}")
    fun deleteUser(
        @PathVariable id: Long?,
        @RequestParam(required = false) confirm: Boolean?
    ): String {
        return userService.deleteUser(id, confirm)
    }
}
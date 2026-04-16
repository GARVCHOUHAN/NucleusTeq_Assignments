package com.session2.usermanagement.dto;

// DTO is used to transfer data safely
// We do not expose internal model directly

public class UserRequestDTO {

    private String name;
    private String email;

    public String getName() { return name; }
    public String getEmail() { return email; }
}

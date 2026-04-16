package com.session3.usersearchsystem.model;

// Represents user data

public class User {

    private Long id;
    private String name;
    private int age;
    private String role;

    public User(Long id, String name, int age, String role) {
        this.id = id;
        this.name = name;
        this.age = age;
        this.role = role;
    }

    public Long getId() { return id; }
    public String getName() { return name; }
    public int getAge() { return age; }
    public String getRole() { return role; }
}
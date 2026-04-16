package com.session3.usersearchsystem.repository;
import com.session3.usersearchsystem.model.User;
import org.springframework.stereotype.Repository;

import java.util.*;

// Handles in-memory data
// not using any db here

@Repository
public class UserRepository {

    private final List<User> users = new ArrayList<>();

    public UserRepository() {
        users.add(new User(1L, "Priya", 25, "USER"));
        users.add(new User(2L, "Rahul", 30, "ADMIN"));
        users.add(new User(3L, "Amit", 30, "USER"));
        users.add(new User(4L, "Sneha", 28, "USER"));
        users.add(new User(5L, "Rohit", 35, "ADMIN"));
    }

    public List<User> findAll() {
        return users;
    }

    public Optional<User> findById(Long id) {
        return users.stream().filter(u -> u.getId().equals(id)).findFirst();
    }

    public void save(User user) {
        users.add(user);
    }

    public void delete(User user) {
        users.remove(user);
    }
}

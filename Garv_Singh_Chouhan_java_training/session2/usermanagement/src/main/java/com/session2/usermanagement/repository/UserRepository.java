package com.session2.usermanagement.repository;


import com.session2.usermanagement.model.User;
import org.springframework.stereotype.Repository;

import java.util.*;

// Repository layer handles data storage (dummy in-memory)

@Repository
public class UserRepository {

    private final Map<Long, User> userMap = new HashMap<>();
    private Long idCounter = 1L;

    // Save user
    public User save(User user) {
        userMap.put(user.getId(), user);
        return user;
    }

    // Get all users
    public List<User> findAll() {
        return new ArrayList<>(userMap.values());
    }

    // Find by ID
    public Optional<User> findById(Long id) {
        return Optional.ofNullable(userMap.get(id));
    }

    // Generate ID
    public Long generateId() {
        return idCounter++;
    }
}

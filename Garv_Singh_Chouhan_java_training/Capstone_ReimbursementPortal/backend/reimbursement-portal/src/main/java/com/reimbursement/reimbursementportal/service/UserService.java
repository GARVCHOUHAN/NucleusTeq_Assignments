package com.reimbursement.reimbursementportal.service;

import com.reimbursement.reimbursementportal.entity.User;
import com.reimbursement.reimbursementportal.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    public User registerUser(User user) {

        if (!user.getEmail().endsWith("@company.com")) {
            throw new RuntimeException("Invalid company email");
        }

        user.setPassword(passwordEncoder.encode(user.getPassword()));

        return userRepository.save(user);
    }
}
package com.reimbursement.reimbursementportal.repository;


import com.reimbursement.reimbursementportal.enums.Role;
import com.reimbursement.reimbursementportal.entity.User;
//import java.util.List;
//import java.util.Optional;
//import org.springframework.data.domain.Page;
//import org.springframework.data.domain.Pageable;
//import org.springframework.data.jpa.repository.JpaRepository;
//import org.springframework.stereotype.Repository;
//
///**
// * Data access layer for User entities.
// */
//@Repository
//public interface UserRepository extends JpaRepository<User, Long> {
//
//    Optional<User> findByEmail(String email);
//
//    boolean existsByEmail(String email);
//
//    Page<User> findAll(Pageable pageable);
//
//    List<User> findByRole(Role role);
//
//    List<User> findByManagerId(Long managerId);
//}

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

/**
 * Repository for User entity.
 */
public interface UserRepository extends JpaRepository<User, Long> {

    /**
     * Finds user by email.
     *
     * @param email the email
     * @return optional user
     */
    Optional<User> findByEmail(String email);

    /**
     * Checks if email exists.
     *
     * @param email the email
     * @return true if exists
     */
    boolean existsByEmail(String email);

    /**
     * Finds users by manager ID.
     *
     * @param managerId the manager ID
     * @return list of users
     */
    List<User> findByManagerId(Long managerId);

    /**
     * Checks if users exist for a manager ID.
     *
     * @param managerId the manager ID
     * @return true if exists
     */
    boolean existsByManagerId(Long managerId);

    /**
     * Finds users by role.
     *
     * @param role the user role
     * @return list of users
     */
    List<User> findByRole(Role role);
}
package com.reimbursement.reimbursementportal.repository;


import com.reimbursement.reimbursementportal.enums.Role;
import com.reimbursement.reimbursementportal.entity.User;
import java.util.List;
import java.util.Optional;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * Data access layer for User entities.
 */
@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByEmail(String email);

    boolean existsByEmail(String email);

    Page<User> findAll(Pageable pageable);

    List<User> findByRole(Role role);

    List<User> findByManagerId(Long managerId);
}
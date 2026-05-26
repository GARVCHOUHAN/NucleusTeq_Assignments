package com.reimbursement.reimbursementportal.entity;

import com.reimbursement.reimbursementportal.enums.Role;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * Represents a system user (Admin, Manager, or Employee).
 */
@Entity
@Table(name = "users")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class User {

    /**
     * User ID.
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * User name.
     */
    private String name;

    /**
     * User email.
     */
    @Column(unique = true)
    private String email;

    /**
     * User password.
     */
    private String password;

    /**
     * User role.
     */
    @Enumerated(EnumType.STRING)
    private Role role;

    /**
     * Manager of the user.
     */
    @ManyToOne
    @JoinColumn(name = "manager_id")
    private User manager;
}

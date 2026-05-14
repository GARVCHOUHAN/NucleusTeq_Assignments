package com.reimbursement.reimbursementportal.entity;

import com.reimbursement.reimbursementportal.enums.ClaimStatus;
import jakarta.persistence.*;

@Entity
@Table(name = "claims")
public class Claim {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Double amount;

    private String description;

    @Enumerated(EnumType.STRING)
    private ClaimStatus status;

    private String reviewerComment;

    @ManyToOne
    @JoinColumn(name = "employee_id")
    private User employee;

    public Claim() {
    }

    public Long getId() {
        return id;
    }

    public Double getAmount() {
        return amount;
    }

    public void setAmount(Double amount) {
        this.amount = amount;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public ClaimStatus getStatus() {
        return status;
    }

    public void setStatus(ClaimStatus status) {
        this.status = status;
    }

    public String getReviewerComment() {
        return reviewerComment;
    }

    public void setReviewerComment(String reviewerComment) {
        this.reviewerComment = reviewerComment;
    }

    public User getEmployee() {
        return employee;
    }

    public void setEmployee(User employee) {
        this.employee = employee;
    }
}
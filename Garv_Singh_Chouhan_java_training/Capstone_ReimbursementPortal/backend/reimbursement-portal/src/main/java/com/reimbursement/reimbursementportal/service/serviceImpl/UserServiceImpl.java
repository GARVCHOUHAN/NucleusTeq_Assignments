package com.reimbursement.reimbursementportal.service.serviceImpl;

import com.reimbursement.reimbursementportal.dto.request.UserRequestDTO;
import com.reimbursement.reimbursementportal.dto.response.UserResponseDTO;
import com.reimbursement.reimbursementportal.entity.Claim;
import com.reimbursement.reimbursementportal.enums.Role;
import com.reimbursement.reimbursementportal.entity.User;
import com.reimbursement.reimbursementportal.enums.ClaimStatus;
import com.reimbursement.reimbursementportal.exception.BadRequestException;
import com.reimbursement.reimbursementportal.repository.ClaimRepository;
import com.reimbursement.reimbursementportal.repository.UserRepository;
import com.reimbursement.reimbursementportal.service.UserService;
import com.reimbursement.reimbursementportal.util.ValidationUtil;
import com.reimbursement.reimbursementportal.mapper.UserMapper;

import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;

import org.slf4j.LoggerFactory;

import java.util.List;

@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final ClaimRepository claimRepository;
    private final BCryptPasswordEncoder passwordEncoder;
    private static final Logger log = LoggerFactory.getLogger(UserServiceImpl.class);

    // ========================= CREATE USER =========================
    @Override
    public UserResponseDTO createUser(UserRequestDTO request) {

        log.info("Creating user: {}", request.getEmail());

        // 1. Validate email domain
        if (!ValidationUtil.isValidCompanyEmail(request.getEmail())) {
            log.warn("Failed to create user {}: invalid company email", request.getEmail());
            throw new BadRequestException("Email must be @company.com");
        }

        // 2. Check duplicate email
        log.info("Checking duplicate email before save: {}", request.getEmail());
        if (userRepository.existsByEmail(request.getEmail())) {
            log.warn("Failed to create user {}: duplicate email", request.getEmail());
            throw new BadRequestException("Email already exists");
        }

        // 3. Encrypt password
        String encryptedPassword = passwordEncoder.encode(request.getPassword());

        // 4. Create user entity FIRST
        User user = UserMapper.toEntity(request, encryptedPassword);

        // 5. Assign manager ONLY if provided (optional for EMPLOYEE)
        if (request.getRole() == Role.EMPLOYEE && request.getManagerId() != null) {

            User manager = userRepository.findById(request.getManagerId())
                    .orElseThrow(() -> {
                        log.warn("Failed to assign manager during create: managerId={}", request.getManagerId());
                        return new BadRequestException("Manager not found");
                    });

            if (manager.getRole() != Role.MANAGER) {
                log.warn("Invalid manager role during user create: managerId={}", request.getManagerId());
                throw new BadRequestException("Assigned manager must have MANAGER role");
            }

            user.setManager(manager);
        }

        // 6. Save user
        log.info("Saving user: {}", request.getEmail());
        User savedUser = userRepository.save(user);

        log.info("User created: {}", savedUser.getEmail());
        return UserMapper.toResponse(savedUser);
    }

    // ========================= GET ALL USERS =========================
    @Override
    public List<UserResponseDTO> getAllUsers() {
        log.info("Fetching all users");
        return userRepository.findAll()
                .stream()
                .map(UserMapper::toResponse)
                .toList();
    }

    // ========================= GET USER BY ID =========================
    @Override
    public UserResponseDTO getUserById(Long id) {
        log.info("Fetching user by ID: {}", id);
        User user = userRepository.findById(id)
                .orElseThrow(() -> {
                    log.warn("User not found with ID: {}", id);
                    return new BadRequestException("User not found with ID: " + id);
                });

        return UserMapper.toResponse(user);
    }

    // ========================= ASSIGN MANAGER =========================
    @Override
    public UserResponseDTO assignManager(Long employeeId, Long managerId) {
        log.info("Assigning manager: employeeId={}, managerId={}", employeeId, managerId);
        User employee = userRepository.findById(employeeId)
                .orElseThrow(() -> {
                    log.warn("Employee not found for manager assignment: employeeId={}", employeeId);
                    return new BadRequestException("Employee not found with ID: " + employeeId);
                });

        if (employee.getRole() != Role.EMPLOYEE) {
            log.warn("Invalid manager assignment target role: employeeId={}, role={}", employeeId, employee.getRole());
            throw new BadRequestException("Manager can be assigned only to EMPLOYEE users");
        }

        if (managerId == null) {
            employee.setManager(null);
            User savedEmployee = userRepository.save(employee);
            reassignSubmittedClaims(savedEmployee, resolveFallbackAdmin());
            log.info("Manager cleared for employeeId: {}", employeeId);
            return UserMapper.toResponse(savedEmployee);
        }

        User manager = userRepository.findById(managerId)
                .orElseThrow(() -> {
                    log.warn("Manager not found for assignment: managerId={}", managerId);
                    return new BadRequestException("Manager not found with ID: " + managerId);
                });

        if (manager.getRole() != Role.MANAGER) {
            log.warn("Invalid role for assigned manager: managerId={}, role={}", managerId, manager.getRole());
            throw new BadRequestException("Assigned manager must have MANAGER role");
        }

        employee.setManager(manager);
        User savedEmployee = userRepository.save(employee);
        reassignSubmittedClaims(savedEmployee, manager);
        log.info("Manager assigned: employeeId={}, managerId={}", employeeId, managerId);
        return UserMapper.toResponse(savedEmployee);
    }

    // ========================= GET EMPLOYEES UNDER MANAGER =========================
    @Override
    public List<UserResponseDTO> getEmployeesByManager(Long managerId) {

        log.info("Fetching employees for manager: {}", managerId);
        if (!userRepository.existsById(managerId)) {
            log.warn("Manager not found while fetching employees: {}", managerId);
            throw new BadRequestException("Manager not found with ID: " + managerId);
        }

        return userRepository.findByManagerId(managerId)
                .stream()
                .map(UserMapper::toResponse)
                .toList();


    }

    // ========================= DELETE USER =========================
    @Override
    public void deleteUser(Long id) {

        log.warn("Deleting user: {}", id);
        User user = userRepository.findById(id)
                .orElseThrow(() -> {
                    log.warn("User not found for delete: {}", id);
                    return new BadRequestException("User not found with ID: " + id);
                });

        if (userRepository.existsByManagerId(id)) {
            log.warn("Cannot delete manager with assigned employees: {}", id);
            throw new BadRequestException("Cannot delete manager with assigned employees");
        }

        if (user.getRole() == Role.MANAGER) {
            reassignClaimsForDeletedReviewer(user, resolveFallbackAdmin());
        }

        log.warn("User deleted with id: {}", id);
        userRepository.delete(user);
    }

    private void reassignSubmittedClaims(User employee, User reviewer) {
        List<Claim> submittedClaims = claimRepository.findByEmployeeIdAndStatus(
                employee.getId(), ClaimStatus.SUBMITTED);

        submittedClaims.forEach(claim -> claim.setReviewer(reviewer));
        claimRepository.saveAll(submittedClaims);

        if (!submittedClaims.isEmpty()) {
            log.info("Reassigned {} submitted claim(s) for employeeId={} to reviewerId={}",
                    submittedClaims.size(), employee.getId(), reviewer.getId());
        }
    }

    private void reassignClaimsForDeletedReviewer(User deletedReviewer, User fallbackReviewer) {
        List<Claim> assignedClaims = claimRepository.findByReviewerId(deletedReviewer.getId());

        assignedClaims.forEach(claim -> claim.setReviewer(fallbackReviewer));
        claimRepository.saveAll(assignedClaims);

        if (!assignedClaims.isEmpty()) {
            log.info("Reassigned {} claim(s) from deleted reviewerId={} to admin reviewerId={}",
                    assignedClaims.size(), deletedReviewer.getId(), fallbackReviewer.getId());
        }
    }

    private User resolveFallbackAdmin() {
        return userRepository.findByRole(Role.ADMIN)
                .stream()
                .findFirst()
                .orElseThrow(() -> {
                    log.error("Database operation failed: no admin available for fallback reviewer");
                    return new BadRequestException("No admin available to act as fallback reviewer");
                });
    }
}


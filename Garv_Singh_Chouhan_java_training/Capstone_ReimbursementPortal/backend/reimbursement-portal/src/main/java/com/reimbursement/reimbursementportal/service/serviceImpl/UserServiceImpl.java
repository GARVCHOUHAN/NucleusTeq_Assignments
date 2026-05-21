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

        // 1. Validate email domain
        if (!ValidationUtil.isValidCompanyEmail(request.getEmail())) {
            throw new BadRequestException("Email must be @company.com");
        }

        // 2. Check duplicate email
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new BadRequestException("Email already exists");
        }

        // 3. Encrypt password
        String encryptedPassword = passwordEncoder.encode(request.getPassword());

        // 4. Create user entity FIRST
        User user = UserMapper.toEntity(request, encryptedPassword);

        // 5. Assign manager ONLY if provided (optional for EMPLOYEE)
        if (request.getRole() == Role.EMPLOYEE && request.getManagerId() != null) {

            User manager = userRepository.findById(request.getManagerId())
                    .orElseThrow(() -> new BadRequestException("Manager not found"));

            if (manager.getRole() != Role.MANAGER) {
                throw new BadRequestException("Assigned manager must have MANAGER role");
            }

            user.setManager(manager);
        }

        // 6. Save user
        User savedUser = userRepository.save(user);

        log.info("User created: {}", request.getEmail());
        return UserMapper.toResponse(savedUser);
    }

    // ========================= GET ALL USERS =========================
    @Override
    public List<UserResponseDTO> getAllUsers() {
        return userRepository.findAll()
                .stream()
                .map(UserMapper::toResponse)
                .toList();
    }

    // ========================= GET USER BY ID =========================
    @Override
    public UserResponseDTO getUserById(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new BadRequestException("User not found with ID: " + id));

        return UserMapper.toResponse(user);
    }

    // ========================= ASSIGN MANAGER =========================
    @Override
    public UserResponseDTO assignManager(Long employeeId, Long managerId) {
        User employee = userRepository.findById(employeeId)
                .orElseThrow(() -> new BadRequestException("Employee not found with ID: " + employeeId));

        if (employee.getRole() != Role.EMPLOYEE) {
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
                .orElseThrow(() -> new BadRequestException("Manager not found with ID: " + managerId));

        if (manager.getRole() != Role.MANAGER) {
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

        if (!userRepository.existsById(managerId)) {
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

        User user = userRepository.findById(id)
                .orElseThrow(() -> new BadRequestException("User not found with ID: " + id));

        if (userRepository.existsByManagerId(id)) {
            throw new BadRequestException("Cannot delete manager with assigned employees");
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

    private User resolveFallbackAdmin() {
        return userRepository.findByRole(Role.ADMIN)
                .stream()
                .findFirst()
                .orElseThrow(() -> new BadRequestException("No admin available to act as fallback reviewer"));
    }
}

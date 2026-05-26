package com.reimbursement.reimbursementportal.service.serviceImpl;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.reimbursement.reimbursementportal.dto.request.UserRequestDTO;
import com.reimbursement.reimbursementportal.dto.response.UserResponseDTO;
import com.reimbursement.reimbursementportal.entity.Claim;
import com.reimbursement.reimbursementportal.entity.User;
import com.reimbursement.reimbursementportal.enums.ClaimStatus;
import com.reimbursement.reimbursementportal.enums.Role;
import com.reimbursement.reimbursementportal.exception.BadRequestException;
import com.reimbursement.reimbursementportal.repository.ClaimRepository;
import com.reimbursement.reimbursementportal.repository.UserRepository;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

@ExtendWith(MockitoExtension.class)
class UserServiceImplTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private ClaimRepository claimRepository;

    @Mock
    private BCryptPasswordEncoder passwordEncoder;

    @InjectMocks
    private UserServiceImpl userService;

    @Test
    void createUserEncryptsPasswordAndAssignsManager() {
        User manager = User.builder().id(2L).name("Manager").role(Role.MANAGER).build();
        when(userRepository.existsByEmail("employee@company.com")).thenReturn(false);
        when(passwordEncoder.encode("secret1")).thenReturn("encoded");
        when(userRepository.findById(2L)).thenReturn(Optional.of(manager));
        when(userRepository.save(any(User.class))).thenAnswer(invocation -> {
            User user = invocation.getArgument(0);
            user.setId(1L);
            return user;
        });

        UserResponseDTO response = userService.createUser(userRequest(Role.EMPLOYEE, 2L));

        assertEquals("employee@company.com", response.getEmail());
        assertEquals(2L, response.getManagerId());
        ArgumentCaptor<User> userCaptor = ArgumentCaptor.forClass(User.class);
        verify(userRepository).save(userCaptor.capture());
        assertEquals("encoded", userCaptor.getValue().getPassword());
    }

    @Test
    void createUserRejectsNonCompanyEmail() {
        UserRequestDTO request = userRequest(Role.EMPLOYEE, null);
        request.setEmail("employee@gmail.com");

        BadRequestException ex = assertThrows(BadRequestException.class, () -> userService.createUser(request));

        assertEquals("Email must be @company.com", ex.getMessage());
    }

    @Test
    void assignManagerClearsManagerAndRoutesSubmittedClaimsToAdmin() {
        User employee = User.builder().id(1L).role(Role.EMPLOYEE).build();
        User admin = User.builder().id(3L).role(Role.ADMIN).build();
        Claim claim = Claim.builder().id(8L).status(ClaimStatus.SUBMITTED).employee(employee).build();
        when(userRepository.findById(1L)).thenReturn(Optional.of(employee));
        when(userRepository.findByRole(Role.ADMIN)).thenReturn(List.of(admin));
        when(userRepository.save(employee)).thenReturn(employee);
        when(claimRepository.findByEmployeeIdAndStatus(1L, ClaimStatus.SUBMITTED)).thenReturn(List.of(claim));

        UserResponseDTO response = userService.assignManager(1L, null);

        assertNull(response.getManagerId());
        assertEquals(admin, claim.getReviewer());
        verify(claimRepository).saveAll(List.of(claim));
    }

    @Test
    void assignManagerSetsManagerAndReassignsSubmittedClaims() {
        User employee = User.builder().id(1L).role(Role.EMPLOYEE).build();
        User manager = User.builder().id(2L).role(Role.MANAGER).build();
        Claim claim = Claim.builder().id(8L).status(ClaimStatus.SUBMITTED).employee(employee).build();
        when(userRepository.findById(1L)).thenReturn(Optional.of(employee));
        when(userRepository.findById(2L)).thenReturn(Optional.of(manager));
        when(userRepository.save(employee)).thenReturn(employee);
        when(claimRepository.findByEmployeeIdAndStatus(1L, ClaimStatus.SUBMITTED)).thenReturn(List.of(claim));

        UserResponseDTO response = userService.assignManager(1L, 2L);

        assertEquals(2L, response.getManagerId());
        assertEquals(manager, claim.getReviewer());
    }

    @Test
    void getUserByIdReturnsMappedUser() {
        User user = User.builder().id(1L).name("Employee").email("employee@company.com").role(Role.EMPLOYEE).build();
        when(userRepository.findById(1L)).thenReturn(Optional.of(user));

        UserResponseDTO response = userService.getUserById(1L);

        assertEquals("Employee", response.getName());
    }

    @Test
    void getEmployeesByManagerReturnsMappedUsers() {
        User employee = User.builder().id(1L).name("Employee").email("employee@company.com").role(Role.EMPLOYEE).build();
        when(userRepository.existsById(2L)).thenReturn(true);
        when(userRepository.findByManagerId(2L)).thenReturn(List.of(employee));

        List<UserResponseDTO> response = userService.getEmployeesByManager(2L);

        assertEquals(1, response.size());
    }

    @Test
    void getAllUsersReturnsMappedUsers() {
        User user = User.builder().id(1L).name("Admin").email("admin@company.com").role(Role.ADMIN).build();
        when(userRepository.findAll()).thenReturn(List.of(user));

        List<UserResponseDTO> response = userService.getAllUsers();

        assertEquals(Role.ADMIN, response.get(0).getRole());
    }

    @Test
    void deleteManagerReassignsClaimsToFallbackAdmin() {
        User manager = User.builder().id(2L).role(Role.MANAGER).build();
        User admin = User.builder().id(3L).role(Role.ADMIN).build();
        Claim claim = Claim.builder().id(9L).reviewer(manager).build();
        when(userRepository.findById(2L)).thenReturn(Optional.of(manager));
        when(userRepository.existsByManagerId(2L)).thenReturn(false);
        when(userRepository.findByRole(Role.ADMIN)).thenReturn(List.of(admin));
        when(claimRepository.findByReviewerId(2L)).thenReturn(List.of(claim));

        userService.deleteUser(2L);

        assertEquals(admin, claim.getReviewer());
        verify(userRepository).delete(manager);
    }

    @Test
    void deleteUserRejectsManagerWithAssignedEmployees() {
        User manager = User.builder().id(2L).role(Role.MANAGER).build();
        when(userRepository.findById(2L)).thenReturn(Optional.of(manager));
        when(userRepository.existsByManagerId(2L)).thenReturn(true);

        BadRequestException ex = assertThrows(BadRequestException.class, () -> userService.deleteUser(2L));

        assertEquals("Cannot delete manager with assigned employees", ex.getMessage());
    }

    private UserRequestDTO userRequest(Role role, Long managerId) {
        UserRequestDTO request = new UserRequestDTO();
        request.setName("Employee");
        request.setEmail("employee@company.com");
        request.setPassword("secret1");
        request.setRole(role);
        request.setManagerId(managerId);
        return request;
    }
}

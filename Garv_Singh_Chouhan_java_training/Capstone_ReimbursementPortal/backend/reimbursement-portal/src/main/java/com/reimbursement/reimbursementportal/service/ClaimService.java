package com.reimbursement.reimbursementportal.service;
import com.reimbursement.reimbursementportal.dto.*;

public interface ClaimService {

    ClaimResponseDto createClaim(Long employeeId, ClaimRequestDto requestDto);
}

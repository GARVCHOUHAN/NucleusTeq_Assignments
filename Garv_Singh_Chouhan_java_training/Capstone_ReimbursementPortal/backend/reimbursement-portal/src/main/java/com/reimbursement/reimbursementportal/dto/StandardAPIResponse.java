package com.reimbursement.reimbursementportal.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class StandardAPIResponse<T> {

    private boolean success;
    private String message;
    private T data;
}

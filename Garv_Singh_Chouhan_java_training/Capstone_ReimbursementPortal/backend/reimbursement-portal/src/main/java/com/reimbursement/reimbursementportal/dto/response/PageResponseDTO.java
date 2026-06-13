package com.reimbursement.reimbursementportal.dto.response;

import java.util.List;
import lombok.Builder;
import lombok.Data;

/**
 * Standard paginated response payload for listing APIs.
 *
 * @param <T> response item type
 */
@Data
@Builder
public class PageResponseDTO<T> {

    private List<T> content;
    private int page;
    private int size;
    private long totalElements;
    private int totalPages;
    private boolean first;
    private boolean last;
}

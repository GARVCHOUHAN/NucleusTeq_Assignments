package com.garv.todo.dto;

import com.garv.todo.entity.Todo;
import com.garv.todo.entity.TodoStatus;
import com.garv.todo.service.NotificationServiceClient;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

class DtoAndEntityTest {

    @Test
    void todoResponseDtoSettersUpdateAllFields() {
        LocalDateTime createdAt = LocalDateTime.of(2026, 6, 2, 18, 0);
        TodoResponseDTO responseDTO = new TodoResponseDTO();

        responseDTO.setId(22L);
        responseDTO.setTitle("Response title");
        responseDTO.setDescription("Response description");
        responseDTO.setStatus(TodoStatus.COMPLETED);
        responseDTO.setCreatedAt(createdAt);

        assertThat(responseDTO.getId()).isEqualTo(22L);
        assertThat(responseDTO.getTitle()).isEqualTo("Response title");
        assertThat(responseDTO.getDescription()).isEqualTo("Response description");
        assertThat(responseDTO.getStatus()).isEqualTo(TodoStatus.COMPLETED);
        assertThat(responseDTO.getCreatedAt()).isEqualTo(createdAt);
    }

    @Test
    void errorResponseSettersUpdateAllFields() {
        LocalDateTime timestamp = LocalDateTime.of(2026, 6, 2, 18, 5);
        Map<String, String> validationErrors = Map.of("title", "Title is required");
        ErrorResponse errorResponse = new ErrorResponse();

        errorResponse.setTimestamp(timestamp);
        errorResponse.setStatus(400);
        errorResponse.setError("Bad Request");
        errorResponse.setMessage("Request validation failed");
        errorResponse.setPath("/todos");
        errorResponse.setValidationErrors(validationErrors);

        assertThat(errorResponse.getTimestamp()).isEqualTo(timestamp);
        assertThat(errorResponse.getStatus()).isEqualTo(400);
        assertThat(errorResponse.getError()).isEqualTo("Bad Request");
        assertThat(errorResponse.getMessage()).isEqualTo("Request validation failed");
        assertThat(errorResponse.getPath()).isEqualTo("/todos");
        assertThat(errorResponse.getValidationErrors()).containsEntry("title", "Title is required");
    }

    @Test
    void errorResponseConstructorSetsAllFields() {
        LocalDateTime timestamp = LocalDateTime.of(2026, 6, 2, 18, 10);

        ErrorResponse errorResponse = new ErrorResponse(
                timestamp,
                404,
                "Not Found",
                "Todo not found",
                "/todos/99",
                null
        );

        assertThat(errorResponse.getTimestamp()).isEqualTo(timestamp);
        assertThat(errorResponse.getStatus()).isEqualTo(404);
        assertThat(errorResponse.getError()).isEqualTo("Not Found");
        assertThat(errorResponse.getMessage()).isEqualTo("Todo not found");
        assertThat(errorResponse.getPath()).isEqualTo("/todos/99");
        assertThat(errorResponse.getValidationErrors()).isNull();
    }

    @Test
    void todoPrePersistDefaultsCreatedAtAndStatus() {
        Todo todo = new Todo();
        todo.setTitle("Persist task");
        todo.setDescription("Default fields");

        todo.prePersist();

        assertThat(todo.getCreatedAt()).isNotNull();
        assertThat(todo.getStatus()).isEqualTo(TodoStatus.PENDING);
    }

    @Test
    void todoPrePersistKeepsExistingCreatedAtAndStatus() {
        LocalDateTime createdAt = LocalDateTime.of(2026, 6, 2, 18, 15);
        Todo todo = new Todo("Existing task", "Keep values", TodoStatus.COMPLETED);
        todo.setId(8L);
        todo.setCreatedAt(createdAt);

        todo.prePersist();

        assertThat(todo.getId()).isEqualTo(8L);
        assertThat(todo.getTitle()).isEqualTo("Existing task");
        assertThat(todo.getDescription()).isEqualTo("Keep values");
        assertThat(todo.getCreatedAt()).isEqualTo(createdAt);
        assertThat(todo.getStatus()).isEqualTo(TodoStatus.COMPLETED);
    }

    @Test
    void notificationServiceClientLogsCreatedTodoNotification() {
        NotificationServiceClient notificationServiceClient = new NotificationServiceClient();
        Todo todo = new Todo("Notify task", "Call dummy service", TodoStatus.PENDING);
        todo.setId(31L);

        notificationServiceClient.sendTodoCreatedNotification(todo);

        assertThat(todo.getId()).isEqualTo(31L);
    }
}

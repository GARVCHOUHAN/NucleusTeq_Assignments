package com.garv.todo.mapper;

import com.garv.todo.dto.TodoDTO;
import com.garv.todo.dto.TodoResponseDTO;
import com.garv.todo.entity.Todo;
import com.garv.todo.entity.TodoStatus;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.assertj.core.api.Assertions.assertThat;

class TodoMapperTest {

    private final TodoMapper todoMapper = new TodoMapper();

    @Test
    void toEntityDefaultsStatusToPending() {
        TodoDTO todoDTO = new TodoDTO("Create mapper test", "Verify default status", null);

        Todo todo = todoMapper.toEntity(todoDTO);

        assertThat(todo.getTitle()).isEqualTo("Create mapper test");
        assertThat(todo.getDescription()).isEqualTo("Verify default status");
        assertThat(todo.getStatus()).isEqualTo(TodoStatus.PENDING);
    }

    @Test
    void toEntityUsesProvidedStatus() {
        TodoDTO todoDTO = new TodoDTO("Completed task", "Already finished", TodoStatus.COMPLETED);

        Todo todo = todoMapper.toEntity(todoDTO);

        assertThat(todo.getStatus()).isEqualTo(TodoStatus.COMPLETED);
    }

    @Test
    void toResponseDtoCopiesAllPublicFields() {
        LocalDateTime createdAt = LocalDateTime.of(2026, 6, 2, 17, 30);
        Todo todo = new Todo("Map response", "Return DTO", TodoStatus.PENDING);
        todo.setId(12L);
        todo.setCreatedAt(createdAt);

        TodoResponseDTO responseDTO = todoMapper.toResponseDTO(todo);

        assertThat(responseDTO.getId()).isEqualTo(12L);
        assertThat(responseDTO.getTitle()).isEqualTo("Map response");
        assertThat(responseDTO.getDescription()).isEqualTo("Return DTO");
        assertThat(responseDTO.getStatus()).isEqualTo(TodoStatus.PENDING);
        assertThat(responseDTO.getCreatedAt()).isEqualTo(createdAt);
    }
}

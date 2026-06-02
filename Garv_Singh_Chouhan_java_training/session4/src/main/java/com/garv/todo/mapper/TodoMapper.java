package com.garv.todo.mapper;

import com.garv.todo.dto.TodoDTO;
import com.garv.todo.dto.TodoResponseDTO;
import com.garv.todo.entity.Todo;
import com.garv.todo.entity.TodoStatus;
import org.springframework.stereotype.Component;

@Component
public class TodoMapper {

    public Todo toEntity(TodoDTO todoDTO) {
        TodoStatus status = todoDTO.getStatus() == null ? TodoStatus.PENDING : todoDTO.getStatus();
        return new Todo(todoDTO.getTitle(), todoDTO.getDescription(), status);
    }

    public TodoResponseDTO toResponseDTO(Todo todo) {
        return new TodoResponseDTO(
                todo.getId(),
                todo.getTitle(),
                todo.getDescription(),
                todo.getStatus(),
                todo.getCreatedAt()
        );
    }
}

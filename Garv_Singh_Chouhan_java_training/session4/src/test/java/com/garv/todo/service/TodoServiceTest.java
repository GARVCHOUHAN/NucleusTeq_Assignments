package com.garv.todo.service;

import com.garv.todo.dto.TodoDTO;
import com.garv.todo.dto.TodoResponseDTO;
import com.garv.todo.entity.Todo;
import com.garv.todo.entity.TodoStatus;
import com.garv.todo.exception.InvalidStatusTransitionException;
import com.garv.todo.exception.ResourceNotFoundException;
import com.garv.todo.mapper.TodoMapper;
import com.garv.todo.repository.TodoRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class TodoServiceTest {

    @Mock
    private TodoRepository todoRepository;

    @Mock
    private NotificationServiceClient notificationServiceClient;

    private TodoService todoService;

    @BeforeEach
    void setUp() {
        todoService = new TodoService(todoRepository, new TodoMapper(), notificationServiceClient);
    }

    @Test
    void createTodoDefaultsStatusToPendingWhenStatusIsMissing() {
        TodoDTO todoDTO = new TodoDTO("Read docs", "Study Spring Data JPA", null);
        Todo savedTodo = todoWithId(1L, "Read docs", "Study Spring Data JPA", TodoStatus.PENDING);

        when(todoRepository.save(any(Todo.class))).thenReturn(savedTodo);

        TodoResponseDTO response = todoService.createTodo(todoDTO);

        ArgumentCaptor<Todo> todoCaptor = ArgumentCaptor.forClass(Todo.class);
        verify(todoRepository).save(todoCaptor.capture());

        assertThat(todoCaptor.getValue().getStatus()).isEqualTo(TodoStatus.PENDING);
        assertThat(response.getId()).isEqualTo(1L);
        assertThat(response.getStatus()).isEqualTo(TodoStatus.PENDING);
        verify(notificationServiceClient).sendTodoCreatedNotification(savedTodo);
    }

    @Test
    void getAllTodosReturnsMappedDtos() {
        when(todoRepository.findAll()).thenReturn(List.of(
                todoWithId(1L, "First task", "Description one", TodoStatus.PENDING),
                todoWithId(2L, "Second task", "Description two", TodoStatus.COMPLETED)
        ));

        List<TodoResponseDTO> todos = todoService.getAllTodos();

        assertThat(todos).hasSize(2);
        assertThat(todos).extracting(TodoResponseDTO::getTitle)
                .containsExactly("First task", "Second task");
    }

    @Test
    void getTodoByIdThrowsExceptionWhenTodoDoesNotExist() {
        when(todoRepository.findById(99L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> todoService.getTodoById(99L))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessage("Todo not found with id: 99");
    }

    @Test
    void getTodoByIdReturnsTodoWhenTodoExists() {
        Todo todo = todoWithId(10L, "Write tests", "Cover service logic", TodoStatus.PENDING);
        when(todoRepository.findById(10L)).thenReturn(Optional.of(todo));

        TodoResponseDTO response = todoService.getTodoById(10L);

        assertThat(response.getId()).isEqualTo(10L);
        assertThat(response.getTitle()).isEqualTo("Write tests");
    }

    @Test
    void updateTodoAllowsPendingToCompletedTransition() {
        Todo existingTodo = todoWithId(1L, "Old title", "Old description", TodoStatus.PENDING);
        TodoDTO todoDTO = new TodoDTO("New title", "New description", TodoStatus.COMPLETED);

        when(todoRepository.findById(1L)).thenReturn(Optional.of(existingTodo));
        when(todoRepository.save(existingTodo)).thenReturn(existingTodo);

        TodoResponseDTO response = todoService.updateTodo(1L, todoDTO);

        assertThat(response.getTitle()).isEqualTo("New title");
        assertThat(response.getDescription()).isEqualTo("New description");
        assertThat(response.getStatus()).isEqualTo(TodoStatus.COMPLETED);
    }

    @Test
    void updateTodoAllowsCompletedToPendingTransition() {
        Todo existingTodo = todoWithId(2L, "Review task", "Already completed", TodoStatus.COMPLETED);
        TodoDTO todoDTO = new TodoDTO("Review task again", "Reopened task", TodoStatus.PENDING);

        when(todoRepository.findById(2L)).thenReturn(Optional.of(existingTodo));
        when(todoRepository.save(existingTodo)).thenReturn(existingTodo);

        TodoResponseDTO response = todoService.updateTodo(2L, todoDTO);

        assertThat(response.getStatus()).isEqualTo(TodoStatus.PENDING);
        assertThat(response.getTitle()).isEqualTo("Review task again");
    }

    @Test
    void updateTodoKeepsExistingStatusWhenStatusIsMissing() {
        Todo existingTodo = todoWithId(3L, "Keep status", "Do not send status", TodoStatus.PENDING);
        TodoDTO todoDTO = new TodoDTO("Keep status updated", "Status remains pending", null);

        when(todoRepository.findById(3L)).thenReturn(Optional.of(existingTodo));
        when(todoRepository.save(existingTodo)).thenReturn(existingTodo);

        TodoResponseDTO response = todoService.updateTodo(3L, todoDTO);

        assertThat(response.getStatus()).isEqualTo(TodoStatus.PENDING);
        assertThat(response.getDescription()).isEqualTo("Status remains pending");
    }

    @Test
    void updateTodoThrowsExceptionWhenTodoDoesNotExist() {
        TodoDTO todoDTO = new TodoDTO("Missing task", "Cannot update", TodoStatus.COMPLETED);
        when(todoRepository.findById(404L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> todoService.updateTodo(404L, todoDTO))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessage("Todo not found with id: 404");

        verify(todoRepository, never()).save(any(Todo.class));
    }

    @Test
    void updateTodoThrowsExceptionForUnsupportedNullCurrentStatusTransition() {
        Todo existingTodo = todoWithId(5L, "Broken state", "Missing current status", null);
        TodoDTO todoDTO = new TodoDTO("Broken state", "Should fail", TodoStatus.COMPLETED);

        when(todoRepository.findById(5L)).thenReturn(Optional.of(existingTodo));

        assertThatThrownBy(() -> todoService.updateTodo(5L, todoDTO))
                .isInstanceOf(InvalidStatusTransitionException.class)
                .hasMessage("Invalid status transition from null to COMPLETED");

        verify(todoRepository, never()).save(any(Todo.class));
    }

    @Test
    void deleteTodoDeletesTodoWhenTodoExists() {
        when(todoRepository.existsById(7L)).thenReturn(true);

        todoService.deleteTodo(7L);

        verify(todoRepository).deleteById(7L);
    }

    @Test
    void deleteTodoThrowsExceptionWhenTodoDoesNotExist() {
        when(todoRepository.existsById(42L)).thenReturn(false);

        assertThatThrownBy(() -> todoService.deleteTodo(42L))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessage("Todo not found with id: 42");

        verify(todoRepository, never()).deleteById(42L);
    }

    private Todo todoWithId(Long id, String title, String description, TodoStatus status) {
        Todo todo = new Todo(title, description, status);
        todo.setId(id);
        todo.setCreatedAt(LocalDateTime.of(2026, 6, 2, 10, 30));
        return todo;
    }
}

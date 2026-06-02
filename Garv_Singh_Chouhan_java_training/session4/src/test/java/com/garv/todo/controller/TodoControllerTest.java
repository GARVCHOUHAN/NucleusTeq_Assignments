package com.garv.todo.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.garv.todo.dto.TodoDTO;
import com.garv.todo.dto.TodoResponseDTO;
import com.garv.todo.entity.TodoStatus;
import com.garv.todo.exception.GlobalExceptionHandler;
import com.garv.todo.exception.InvalidStatusTransitionException;
import com.garv.todo.exception.ResourceNotFoundException;
import com.garv.todo.service.TodoService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.validation.beanvalidation.LocalValidatorFactoryBean;

import java.time.LocalDateTime;
import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

class TodoControllerTest {

    private final ObjectMapper objectMapper = new ObjectMapper().findAndRegisterModules();

    private TodoService todoService;
    private MockMvc mockMvc;

    @BeforeEach
    void setUp() {
        todoService = mock(TodoService.class);
        LocalValidatorFactoryBean validator = new LocalValidatorFactoryBean();
        validator.afterPropertiesSet();
        mockMvc = MockMvcBuilders
                .standaloneSetup(new TodoController(todoService))
                .setControllerAdvice(new GlobalExceptionHandler())
                .setValidator(validator)
                .build();
    }

    @Test
    void createTodoReturnsCreatedTodo() throws Exception {
        TodoResponseDTO responseDTO = responseDto(1L, "Create todo", "Controller test", TodoStatus.PENDING);
        when(todoService.createTodo(any(TodoDTO.class))).thenReturn(responseDTO);

        mockMvc.perform(post("/todos")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(new TodoDTO("Create todo", "Controller test", null))))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1L))
                .andExpect(jsonPath("$.status").value("PENDING"));
    }

    @Test
    void createTodoReturnsBadRequestForInvalidTitle() throws Exception {
        mockMvc.perform(post("/todos")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(new TodoDTO("Hi", "Too short", null))))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value("Request validation failed"))
                .andExpect(jsonPath("$.validationErrors.title").value("Title must contain at least 3 characters"));
    }

    @Test
    void getAllTodosReturnsTodos() throws Exception {
        when(todoService.getAllTodos()).thenReturn(List.of(
                responseDto(1L, "First todo", "One", TodoStatus.PENDING),
                responseDto(2L, "Second todo", "Two", TodoStatus.COMPLETED)
        ));

        mockMvc.perform(get("/todos"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].title").value("First todo"))
                .andExpect(jsonPath("$[1].status").value("COMPLETED"));
    }

    @Test
    void getTodoByIdReturnsTodo() throws Exception {
        when(todoService.getTodoById(1L)).thenReturn(responseDto(1L, "Find todo", "By id", TodoStatus.PENDING));

        mockMvc.perform(get("/todos/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("Find todo"));
    }

    @Test
    void getTodoByIdReturnsNotFoundWhenMissing() throws Exception {
        when(todoService.getTodoById(99L)).thenThrow(new ResourceNotFoundException("Todo not found with id: 99"));

        mockMvc.perform(get("/todos/99"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.message").value("Todo not found with id: 99"));
    }

    @Test
    void updateTodoReturnsUpdatedTodo() throws Exception {
        TodoResponseDTO responseDTO = responseDto(1L, "Updated todo", "Done", TodoStatus.COMPLETED);
        when(todoService.updateTodo(eq(1L), any(TodoDTO.class))).thenReturn(responseDTO);

        mockMvc.perform(put("/todos/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(new TodoDTO("Updated todo", "Done", TodoStatus.COMPLETED))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("COMPLETED"));
    }

    @Test
    void updateTodoReturnsBadRequestForInvalidStatusTransition() throws Exception {
        when(todoService.updateTodo(eq(1L), any(TodoDTO.class)))
                .thenThrow(new InvalidStatusTransitionException("Invalid status transition from PENDING to null"));

        mockMvc.perform(put("/todos/1")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(new TodoDTO("Updated todo", "Done", TodoStatus.COMPLETED))))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value("Invalid status transition from PENDING to null"));
    }

    @Test
    void deleteTodoReturnsNoContent() throws Exception {
        mockMvc.perform(delete("/todos/1"))
                .andExpect(status().isNoContent());

        verify(todoService).deleteTodo(1L);
    }

    @Test
    void malformedRequestReturnsBadRequest() throws Exception {
        mockMvc.perform(post("/todos")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"title\":\"Bad enum\",\"status\":\"IN_PROGRESS\"}"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value("Request body is missing or contains invalid JSON values"));
    }

    private TodoResponseDTO responseDto(Long id, String title, String description, TodoStatus status) {
        return new TodoResponseDTO(id, title, description, status, LocalDateTime.of(2026, 6, 2, 17, 30));
    }
}

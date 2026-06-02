package com.garv.todo.controller;

import com.garv.todo.dto.TodoDTO;
import com.garv.todo.dto.TodoResponseDTO;
import com.garv.todo.service.TodoService;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/todos")
public class TodoController {

    private static final Logger LOGGER = LoggerFactory.getLogger(TodoController.class);

    private final TodoService todoService;

    public TodoController(TodoService todoService) {
        this.todoService = todoService;
    }

    @PostMapping
    public ResponseEntity<TodoResponseDTO> createTodo(@Valid @RequestBody TodoDTO todoDTO) {
        LOGGER.info("Received request to create todo with title: {}", todoDTO.getTitle());
        TodoResponseDTO createdTodo = todoService.createTodo(todoDTO);
        LOGGER.info("Todo created successfully with id: {}", createdTodo.getId());
        return ResponseEntity.status(HttpStatus.CREATED).body(createdTodo);
    }

    @GetMapping
    public ResponseEntity<List<TodoResponseDTO>> getAllTodos() {
        LOGGER.info("Received request to fetch all todos");
        List<TodoResponseDTO> todos = todoService.getAllTodos();
        LOGGER.info("Returning {} todos", todos.size());
        return ResponseEntity.ok(todos);
    }

    @GetMapping("/{id}")
    public ResponseEntity<TodoResponseDTO> getTodoById(@PathVariable Long id) {
        LOGGER.info("Received request to fetch todo with id: {}", id);
        return ResponseEntity.ok(todoService.getTodoById(id));
    }

    @PutMapping("/{id}")
    public ResponseEntity<TodoResponseDTO> updateTodo(@PathVariable Long id, @Valid @RequestBody TodoDTO todoDTO) {
        LOGGER.info("Received request to update todo with id: {}", id);
        return ResponseEntity.ok(todoService.updateTodo(id, todoDTO));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteTodo(@PathVariable Long id) {
        LOGGER.info("Received request to delete todo with id: {}", id);
        todoService.deleteTodo(id);
        LOGGER.info("Todo deleted successfully with id: {}", id);
        return ResponseEntity.noContent().build();
    }
}

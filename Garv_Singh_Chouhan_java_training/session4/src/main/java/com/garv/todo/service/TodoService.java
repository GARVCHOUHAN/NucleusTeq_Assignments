package com.garv.todo.service;

import com.garv.todo.dto.TodoDTO;
import com.garv.todo.dto.TodoResponseDTO;
import com.garv.todo.entity.Todo;
import com.garv.todo.entity.TodoStatus;
import com.garv.todo.exception.InvalidStatusTransitionException;
import com.garv.todo.exception.ResourceNotFoundException;
import com.garv.todo.mapper.TodoMapper;
import com.garv.todo.repository.TodoRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class TodoService {

    private static final Logger LOGGER = LoggerFactory.getLogger(TodoService.class);

    private final TodoRepository todoRepository;
    private final TodoMapper todoMapper;
    private final NotificationServiceClient notificationServiceClient;

    public TodoService(TodoRepository todoRepository, TodoMapper todoMapper,
                       NotificationServiceClient notificationServiceClient) {
        this.todoRepository = todoRepository;
        this.todoMapper = todoMapper;
        this.notificationServiceClient = notificationServiceClient;
    }

    @Transactional
    public TodoResponseDTO createTodo(TodoDTO todoDTO) {
        LOGGER.info("Creating todo with title: {}", todoDTO.getTitle());
        Todo todo = todoMapper.toEntity(todoDTO);
        Todo savedTodo = todoRepository.save(todo);
        notificationServiceClient.sendTodoCreatedNotification(savedTodo);
        LOGGER.info("Todo created with id: {}", savedTodo.getId());
        return todoMapper.toResponseDTO(savedTodo);
    }

    @Transactional(readOnly = true)
    public List<TodoResponseDTO> getAllTodos() {
        LOGGER.info("Fetching all todos");
        return todoRepository.findAll()
                .stream()
                .map(todoMapper::toResponseDTO)
                .toList();
    }

    @Transactional(readOnly = true)
    public TodoResponseDTO getTodoById(Long id) {
        LOGGER.info("Fetching todo with id: {}", id);
        Todo todo = findTodoById(id);
        return todoMapper.toResponseDTO(todo);
    }

    @Transactional
    public TodoResponseDTO updateTodo(Long id, TodoDTO todoDTO) {
        LOGGER.info("Updating todo with id: {}", id);
        Todo todo = findTodoById(id);

        todo.setTitle(todoDTO.getTitle());
        todo.setDescription(todoDTO.getDescription());

        if (todoDTO.getStatus() != null) {
            validateStatusTransition(todo.getStatus(), todoDTO.getStatus());
            todo.setStatus(todoDTO.getStatus());
        }

        Todo updatedTodo = todoRepository.save(todo);
        LOGGER.info("Todo updated with id: {}", updatedTodo.getId());
        return todoMapper.toResponseDTO(updatedTodo);
    }

    @Transactional
    public void deleteTodo(Long id) {
        LOGGER.info("Deleting todo with id: {}", id);
        if (!todoRepository.existsById(id)) {
            throw new ResourceNotFoundException("Todo not found with id: " + id);
        }
        todoRepository.deleteById(id);
        LOGGER.info("Todo deleted with id: {}", id);
    }

    private Todo findTodoById(Long id) {
        return todoRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found with id: " + id));
    }

    private void validateStatusTransition(TodoStatus currentStatus, TodoStatus requestedStatus) {
        if (currentStatus == requestedStatus) {
            return;
        }

        boolean isAllowedTransition = (currentStatus == TodoStatus.PENDING && requestedStatus == TodoStatus.COMPLETED)
                || (currentStatus == TodoStatus.COMPLETED && requestedStatus == TodoStatus.PENDING);

        if (!isAllowedTransition) {
            LOGGER.warn("Invalid todo status transition from {} to {}", currentStatus, requestedStatus);
            throw new InvalidStatusTransitionException(
                    "Invalid status transition from " + currentStatus + " to " + requestedStatus
            );
        }
    }
}

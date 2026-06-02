package com.garv.todo.service;

import com.garv.todo.entity.Todo;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Service
public class NotificationServiceClient {

    private static final Logger LOGGER = LoggerFactory.getLogger(NotificationServiceClient.class);

    public void sendTodoCreatedNotification(Todo todo) {
        LOGGER.info("Notification sent for new TODO with id: {} and title: {}", todo.getId(), todo.getTitle());
    }
}

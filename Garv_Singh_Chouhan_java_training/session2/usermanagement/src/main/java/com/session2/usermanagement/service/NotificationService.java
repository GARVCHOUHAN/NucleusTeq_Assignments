package com.session2.usermanagement.service;

import com.session2.usermanagement.component.NotificationComponent;
import org.springframework.stereotype.Service;

// Service calls component (DI in action)

@Service
public class NotificationService {

    private final NotificationComponent notificationComponent;

    public NotificationService(NotificationComponent notificationComponent) {
        this.notificationComponent = notificationComponent;
    }

    public String triggerNotification() {
        return notificationComponent.sendNotification();
    }
}

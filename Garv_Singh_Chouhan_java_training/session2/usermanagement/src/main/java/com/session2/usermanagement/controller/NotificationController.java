package com.session2.usermanagement.controller;

import com.session2.usermanagement.service.NotificationService;
import org.springframework.web.bind.annotation.*;

// API to trigger notification

@RestController
@RequestMapping("/notify")
public class NotificationController {

    private final NotificationService notificationService;

    public NotificationController(NotificationService notificationService) {
        this.notificationService = notificationService;
    }

    @GetMapping
    public String sendNotification() {
        return notificationService.triggerNotification();
    }
}

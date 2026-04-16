package com.session2.usermanagement.component;

import org.springframework.stereotype.Component;

// This component handles reusable notification logic

@Component
public class NotificationComponent {

    public String sendNotification() {
        return "Notification sent successfully!";
    }
}

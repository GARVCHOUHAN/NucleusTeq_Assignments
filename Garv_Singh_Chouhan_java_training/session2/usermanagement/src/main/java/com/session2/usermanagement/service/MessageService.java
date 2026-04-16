package com.session2.usermanagement.service;

import com.session2.usermanagement.component.MessageFormatter;
import org.springframework.stereotype.Service;

import java.util.Map;

// Decision logic should be inside service, not controller

@Service
public class MessageService {

    private final Map<String, MessageFormatter> formatterMap;

    // Spring injects all implementations automatically
    public MessageService(Map<String, MessageFormatter> formatterMap) {
        this.formatterMap = formatterMap;
    }

    public String getMessage(String type) {

        MessageFormatter formatter = formatterMap.get(type.toUpperCase());

        if (formatter == null) {
            throw new IllegalArgumentException("Invalid message type");
        }

        return formatter.format();
    }
}

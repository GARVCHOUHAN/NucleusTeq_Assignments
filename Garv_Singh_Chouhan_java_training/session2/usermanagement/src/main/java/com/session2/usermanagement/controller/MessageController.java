package com.session2.usermanagement.controller;

import com.session2.usermanagement.service.MessageService;
import org.springframework.web.bind.annotation.*;

// Controller only forwards request

@RestController
@RequestMapping("/message")
public class MessageController {

    private final MessageService messageService;

    public MessageController(MessageService messageService) {
        this.messageService = messageService;
    }

    @GetMapping
    public String getMessage(@RequestParam String type) {
        return messageService.getMessage(type);
    }
}

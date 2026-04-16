package com.session2.usermanagement.component;

import org.springframework.stereotype.Component;

@Component("SHORT")
public class ShortMessageFormatter implements MessageFormatter {

    public String format() {
        return "Short Message";
    }
}

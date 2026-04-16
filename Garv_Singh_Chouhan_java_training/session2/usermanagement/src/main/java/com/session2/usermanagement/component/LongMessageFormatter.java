package com.session2.usermanagement.component;
import org.springframework.stereotype.Component;

@Component("LONG")
public class LongMessageFormatter implements MessageFormatter {

    public String format() {
        return "This is a detailed long message format.";
    }
}

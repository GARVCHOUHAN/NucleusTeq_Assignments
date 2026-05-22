package com.reimbursement.reimbursementportal.config;

import com.reimbursement.reimbursementportal.entity.User;
import com.reimbursement.reimbursementportal.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Component;

/**
 * Encrypts legacy plaintext passwords once when the application starts.
 */
@Component
@RequiredArgsConstructor
public class PasswordMigrationRunner implements ApplicationRunner {

    private static final Logger log = LoggerFactory.getLogger(PasswordMigrationRunner.class);
    private static final String BCRYPT_PREFIX = "$2";

    private final UserRepository userRepository;
    private final BCryptPasswordEncoder passwordEncoder;

    @Override
    public void run(ApplicationArguments args) {
        int migrated = 0;

        for (User user : userRepository.findAll()) {
            String password = user.getPassword();
            if (password != null && !password.startsWith(BCRYPT_PREFIX)) {
                user.setPassword(passwordEncoder.encode(password));
                userRepository.save(user);
                migrated++;
            }
        }

        if (migrated > 0) {
            log.info("Encrypted {} legacy plaintext user password(s)", migrated);
        }
    }
}

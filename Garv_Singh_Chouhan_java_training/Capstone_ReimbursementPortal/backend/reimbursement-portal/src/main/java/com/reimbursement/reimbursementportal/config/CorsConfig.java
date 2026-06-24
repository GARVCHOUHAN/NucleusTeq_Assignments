package com.reimbursement.reimbursementportal.config;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;

/**
 * Configuration class for CORS settings.
 */
@Configuration
public class CorsConfig {

    /**
     * Creates a CorsFilter bean to handle CORS configuration.
     *
     * @return CorsFilter configured with allowed origins, headers, and methods
     */
    @Bean
    public CorsFilter corsFilter() {
        CorsConfiguration config = new CorsConfiguration();

        // Allow requests from any origin (your HTML files opened from disk)
        // In production, replace "*" with your actual domain
        config.addAllowedOriginPattern("*");

        // Allow Basic Auth header and Content-Type
        config.addAllowedHeader("*");

        // Allow all HTTP methods: GET, POST, PUT, DELETE, OPTIONS
        config.addAllowedMethod("*");

        // Allow credentials (needed for Basic Auth)
        config.setAllowCredentials(false);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();

        // Apply this CORS config to ALL endpoints
        source.registerCorsConfiguration("/api/**", config);

        return new CorsFilter(source);
    }
}

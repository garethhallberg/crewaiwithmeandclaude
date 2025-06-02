package com.twitterclone.common.test

import org.springframework.http.HttpHeaders
import java.util.*

/**
 * JWT test utilities for integration tests
 */
object JwtTestUtils {
    
    // Mock JWT token for testing
    const val MOCK_JWT_TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImlhdCI6MTYzNzc1NTIwMCwiZXhwIjoyNjM3NzU1MjAwfQ.test"
    
    /**
     * Create HTTP headers with Bearer authentication token
     */
    fun createAuthHeaders(token: String = MOCK_JWT_TOKEN): HttpHeaders {
        val headers = HttpHeaders()
        headers.setBearerAuth(token)
        return headers
    }
    
    /**
     * Create a test JWT token for the given username
     */
    fun createTestToken(username: String = "testuser"): String {
        return MOCK_JWT_TOKEN
    }
}

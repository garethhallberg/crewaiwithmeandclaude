package com.twitterclone.user.integration

import com.twitterclone.user.UserServiceApplication
import com.twitterclone.user.dto.AuthResponse
import com.twitterclone.user.dto.RegisterRequest
import com.twitterclone.user.dto.LoginRequest
import org.junit.jupiter.api.*
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.boot.test.web.client.TestRestTemplate
import org.springframework.boot.test.web.server.LocalServerPort
import org.springframework.http.*
import org.springframework.test.context.ActiveProfiles
import java.util.*

/**
 * Integration tests for User Service (using H2 in-memory database)
 */
@SpringBootTest(
    classes = [UserServiceApplication::class],
    webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT
)
@ActiveProfiles("test")
@TestMethodOrder(MethodOrderer.OrderAnnotation::class)
class UserServiceIntegrationTest {

    @Autowired
    private lateinit var restTemplate: TestRestTemplate

    @LocalServerPort
    private var port: Int = 0

    private fun getBaseUrl(): String = "http://localhost:$port"
    
    private fun createRegisterRequest(): RegisterRequest {
        return RegisterRequest(
            username = "testuser_${UUID.randomUUID().toString().substring(0, 8)}",
            email = "test_${UUID.randomUUID().toString().substring(0, 8)}@example.com",
            password = "password123",
            displayName = "Test User"
        )
    }
    
    private fun createLoginRequest(usernameOrEmail: String, password: String): LoginRequest {
        return LoginRequest(
            usernameOrEmail = usernameOrEmail,
            password = password
        )
    }

    @Test
    @Order(1)
    fun `should register user successfully`() {
        // Given
        val request = createRegisterRequest()

        // When
        val response = restTemplate.postForEntity(
            "${getBaseUrl()}/api/auth/register",
            request,
            AuthResponse::class.java
        )

        // Then
        Assertions.assertEquals(HttpStatus.CREATED, response.statusCode)
        Assertions.assertNotNull(response.body)
        Assertions.assertNotNull(response.body?.token)
        Assertions.assertEquals(request.username, response.body?.user?.username)
    }

    @Test
    @Order(2)
    fun `should login user successfully`() {
        // Given - First register a user
        val registerRequest = createRegisterRequest()
        restTemplate.postForEntity(
            "${getBaseUrl()}/api/auth/register",
            registerRequest,
            AuthResponse::class.java
        )
        
        val loginRequest = createLoginRequest(
            usernameOrEmail = registerRequest.username,
            password = registerRequest.password
        )

        // When
        val response = restTemplate.postForEntity(
            "${getBaseUrl()}/api/auth/login",
            loginRequest,
            AuthResponse::class.java
        )

        // Then
        Assertions.assertEquals(HttpStatus.OK, response.statusCode)
        Assertions.assertNotNull(response.body)
        Assertions.assertNotNull(response.body?.token)
        Assertions.assertEquals(registerRequest.username, response.body?.user?.username)
    }

    @Test
    @Order(3)  
    fun `should access protected endpoint with valid token`() {
        // Given - Register and login to get token  
        val registerRequest = createRegisterRequest()
        restTemplate.postForEntity(
            "${getBaseUrl()}/api/auth/register",
            registerRequest,
            AuthResponse::class.java
        )
        
        val loginRequest = createLoginRequest(
            usernameOrEmail = registerRequest.username,
            password = registerRequest.password
        )
        val loginResponse = restTemplate.postForEntity(
            "${getBaseUrl()}/api/auth/login",
            loginRequest,
            AuthResponse::class.java
        )
        val token = loginResponse.body?.token!!

        // When - Access protected endpoint
        val headers = HttpHeaders()
        headers.setBearerAuth(token)
        val entity = HttpEntity<String>(headers)

        val response = restTemplate.exchange(
            "${getBaseUrl()}/api/users/search?q=test",
            HttpMethod.GET,
            entity,
            String::class.java
        )

        // Then
        Assertions.assertEquals(HttpStatus.OK, response.statusCode)
    }

    @Test
    @Order(4)
    fun `should return 401 for protected endpoint without token`() {
        // When
        val response = restTemplate.getForEntity(
            "${getBaseUrl()}/api/users/search?q=test",
            String::class.java
        )

        // Then
        Assertions.assertEquals(HttpStatus.UNAUTHORIZED, response.statusCode)
    }
}

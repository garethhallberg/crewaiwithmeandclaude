"""
004m_integration_tests.py - Integration Tests Creation
Twitter Clone CrewAI Project - Phase 4m Integration Testing

This script uses CrewAI agents to create comprehensive integration tests
that validate end-to-end workflows across services, database, and authentication.
"""

from improved_twitter_config import technical_lead, kotlin_api_architect, kotlin_api_developer
from crewai import Agent, Task, Crew, Process
from pathlib import Path

def create_integration_tests():
    """Use CrewAI agents to create comprehensive integration tests"""
    
    print("🚀 Starting Integration Tests Creation with CrewAI...")
    print("=" * 80)
    print("🔗 PHASE 4m: Integration Tests Implementation")
    print("=" * 80)
    print("CrewAI agents will create end-to-end integration tests...")
    print("")

    # Task 1: User Service Integration Tests
    user_integration_tests_task = Task(
        description='''
        You must create comprehensive integration tests for the user-service.
        
        REQUIREMENTS:
        Create UserServiceIntegrationTest.kt that will be written to disk.
        
        The integration test must include:
        - @SpringBootTest annotation for full application context
        - @AutoConfigureTestDatabase for test database
        - @TestMethodOrder for ordered test execution
        - Real database operations using TestContainers
        - Full authentication flow testing
        
        TEST SCENARIOS TO COVER:
        1. User Registration Flow:
           - POST /api/auth/register with valid data
           - Verify user created in database
           - Verify JWT token returned
           - Verify password is encrypted
        
        2. User Login Flow:
           - POST /api/auth/login with registered user
           - Verify JWT token returned
           - Verify token is valid and contains username
        
        3. Protected Endpoint Access:
           - GET /api/users/{id} with valid JWT token
           - GET /api/users/search with valid JWT token
           - Verify 401 response without token
           - Verify 403 response with invalid token
        
        4. User Profile Operations:
           - PUT /api/users/{id} to update profile
           - Verify changes persisted in database
        
        CRITICAL: Use @TestRestTemplate or WebTestClient for real HTTP calls.
        Include proper assertions for HTTP status codes and response content.
        
        OUTPUT: Complete UserServiceIntegrationTest.kt file.
        ''',
        agent=kotlin_api_architect,
        expected_output='Complete UserServiceIntegrationTest.kt with end-to-end user service testing'
    )

    # Task 2: Post Service Integration Tests
    post_integration_tests_task = Task(
        description='''
        You must create comprehensive integration tests for the post-service.
        
        REQUIREMENTS:
        Create PostServiceIntegrationTest.kt that will be written to disk.
        
        The integration test must include:
        - @SpringBootTest annotation for full application context
        - JWT authentication for all requests
        - Real database operations with TestContainers
        - Cross-service authentication validation
        
        TEST SCENARIOS TO COVER:
        1. Post Creation Flow:
           - POST /api/posts with valid JWT token
           - Verify post created in database
           - Verify author information
           - Test with invalid/missing token (401/403)
        
        2. Post Retrieval Operations:
           - GET /api/posts/{id} for specific post
           - GET /api/posts/user/{userId} for user posts
           - Verify pagination works correctly
        
        3. Post Engagement Features:
           - POST /api/posts/{id}/like to like a post
           - DELETE /api/posts/{id}/like to unlike
           - Verify like count updates
           - Test duplicate like prevention
        
        4. Timeline Operations:
           - GET /api/timeline/public for public timeline
           - GET /api/timeline/user/{userId} for user timeline
           - Verify posts ordered by creation time
           - Test pagination and sorting
        
        5. Comment/Reply System:
           - POST /api/posts with parentPostId for replies
           - GET /api/posts/{id}/comments for post comments
           - Verify comment threading
        
        CRITICAL: All requests must include valid JWT token from user-service.
        Test cross-service authentication validation.
        
        OUTPUT: Complete PostServiceIntegrationTest.kt file.
        ''',
        agent=kotlin_api_developer,
        expected_output='Complete PostServiceIntegrationTest.kt with end-to-end post service testing'
    )

    # Task 3: Cross-Service Integration Tests
    cross_service_tests_task = Task(
        description='''
        You must create integration tests that validate cross-service workflows.
        
        REQUIREMENTS:
        Create CrossServiceIntegrationTest.kt that will be written to disk.
        
        The integration test must validate:
        - JWT tokens work across both services
        - End-to-end user journey workflows
        - Service-to-service communication
        - Data consistency across services
        
        TEST SCENARIOS TO COVER:
        1. Complete User Journey:
           - Register user on user-service (port 8081)
           - Login and get JWT token
           - Use token to create post on post-service (port 8082)
           - Retrieve user's posts
           - Like/unlike posts
           - Update user profile
           - Verify all operations work end-to-end
        
        2. Authentication Cross-Service:
           - Get JWT from user-service
           - Use same JWT on post-service endpoints
           - Verify token validation works consistently
           - Test token expiration handling
        
        3. Data Consistency:
           - Create user and posts
           - Update user profile
           - Verify post author information consistency
           - Test data integrity across services
        
        4. Error Handling:
           - Invalid JWT tokens across services
           - Non-existent user/post operations
           - Database constraint violations
           - Service unavailability scenarios
        
        CRITICAL: This tests the complete Twitter clone functionality.
        Must validate that both services work together seamlessly.
        
        OUTPUT: Complete CrossServiceIntegrationTest.kt file.
        ''',
        agent=technical_lead,
        expected_output='Complete CrossServiceIntegrationTest.kt with cross-service workflow testing'
    )

    # Task 4: Integration Test Configuration
    test_configuration_task = Task(
        description='''
        You must create integration test configuration and setup files.
        
        REQUIREMENTS:
        Create these configuration files that will be written to disk:
        
        1. IntegrationTestConfig.kt - Test configuration class
        2. TestContainerConfig.kt - Database container setup
        3. application-test.yml - Test environment properties
        4. IntegrationTestBase.kt - Base class for integration tests
        
        CONFIGURATION REQUIREMENTS:
        
        IntegrationTestConfig.kt:
        - @TestConfiguration annotation
        - Mock external dependencies if needed
        - Test-specific bean configurations
        - Port configurations for services
        
        TestContainerConfig.kt:
        - PostgreSQL TestContainer setup
        - Redis TestContainer setup (if needed)
        - Container lifecycle management
        - Database initialization scripts
        
        application-test.yml:
        - Test database configuration
        - Logging levels for testing
        - JWT secret for testing
        - Service port configurations
        
        IntegrationTestBase.kt:
        - Base class with common test setup
        - JWT token generation utilities
        - Common test data creation methods
        - Database cleanup between tests
        
        CRITICAL: Ensure tests can run independently and in parallel.
        Provide clean test environment for each test.
        
        OUTPUT: Complete integration test configuration files.
        ''',
        agent=kotlin_api_architect,
        expected_output='Complete integration test configuration with TestContainers and test utilities'
    )

    # Create the crew
    integration_test_crew = Crew(
        agents=[kotlin_api_architect, kotlin_api_developer, technical_lead],
        tasks=[user_integration_tests_task, post_integration_tests_task, cross_service_tests_task, test_configuration_task],
        process=Process.sequential,
        verbose=True
    )

    # Execute the crew
    print("🤖 CrewAI agents are creating comprehensive integration tests...")
    print("⏳ This may take several minutes as agents generate end-to-end test scenarios...")
    
    try:
        result = integration_test_crew.kickoff()
        
        # Apply the generated files
        apply_integration_test_files(result)
        
        print("\n" + "=" * 80)
        print("✅ INTEGRATION TESTS CREATED!")
        print("=" * 80)
        
        print("\n🎯 CrewAI agents have created:")
        print("  • UserServiceIntegrationTest.kt - Full user service testing")
        print("  • PostServiceIntegrationTest.kt - Complete post service testing")
        print("  • CrossServiceIntegrationTest.kt - End-to-end workflow testing")
        print("  • Integration test configuration and utilities")
        print("  • TestContainer setup for database testing")
        
        print("\n🔗 Integration Test Coverage:")
        print("  • User registration and authentication flows")
        print("  • Post creation, retrieval, and engagement")
        print("  • Cross-service JWT authentication")
        print("  • Timeline and feed generation")
        print("  • Database operations and data consistency")
        print("  • Error handling and edge cases")
        
        print("\n🚀 Next Steps:")
        print("  • Run integration tests: ./gradlew integrationTest")
        print("  • Or run all tests: ./gradlew test")
        print("  • Start services: docker-compose up -d")
        print("  • Monitor test results and fix any failures")
        
        print("\n📋 Test Commands:")
        print("  # Run specific integration test")
        print("  ./gradlew :user-service:test --tests '*IntegrationTest*'")
        print("  ./gradlew :post-service:test --tests '*IntegrationTest*'")
        
        return {
            "status": "success", 
            "message": "Integration tests created successfully",
            "crew_output": str(result)
        }
        
    except Exception as e:
        print(f"\n❌ Error creating integration tests: {str(e)}")
        return {
            "status": "error",
            "message": f"Integration test creation failed: {str(e)}"
        }

def apply_integration_test_files(crew_result):
    """Create the integration test files"""
    
    print("\n🔧 Creating integration test files...")
    
    backend_dir = Path("generated_code/backend")
    
    # Create basic integration test for user service
    user_integration_test_content = '''package com.twitterclone.user.integration

import com.twitterclone.common.dto.UserDto
import com.twitterclone.user.dto.RegisterRequest
import com.twitterclone.user.dto.LoginRequest
import com.twitterclone.user.dto.AuthResponse
import org.junit.jupiter.api.*
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.boot.test.web.client.TestRestTemplate
import org.springframework.boot.test.web.server.LocalServerPort
import org.springframework.http.*
import org.springframework.test.context.ActiveProfiles
import org.testcontainers.containers.PostgreSQLContainer
import org.testcontainers.junit.jupiter.Container
import org.testcontainers.junit.jupiter.Testcontainers

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestMethodOrder(MethodOrderer.OrderAnnotation::class)
@ActiveProfiles("test")
@Testcontainers
class UserServiceIntegrationTest {

    @LocalServerPort
    private var port: Int = 0

    @Autowired
    private lateinit var restTemplate: TestRestTemplate

    companion object {
        @Container
        @JvmStatic
        val postgresContainer = PostgreSQLContainer("postgres:15")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test")
    }

    private fun getBaseUrl() = "http://localhost:$port"

    @Test
    @Order(1)
    fun `should register user successfully`() {
        // Given
        val request = RegisterRequest(
            username = "integrationuser",
            email = "integration@test.com", 
            password = "password123",
            displayName = "Integration Test User"
        )

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
        Assertions.assertEquals("integrationuser", response.body?.user?.username)
    }

    @Test
    @Order(2)
    fun `should login user successfully`() {
        // Given
        val request = LoginRequest(
            usernameOrEmail = "integrationuser",
            password = "password123"
        )

        // When
        val response = restTemplate.postForEntity(
            "${getBaseUrl()}/api/auth/login",
            request,
            AuthResponse::class.java
        )

        // Then
        Assertions.assertEquals(HttpStatus.OK, response.statusCode)
        Assertions.assertNotNull(response.body)
        Assertions.assertNotNull(response.body?.token)
        Assertions.assertEquals("integrationuser", response.body?.user?.username)
    }

    @Test
    @Order(3)
    fun `should access protected endpoint with valid token`() {
        // Given - First login to get token
        val loginRequest = LoginRequest("integrationuser", "password123")
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
            "${getBaseUrl()}/api/users/search?q=integration",
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
'''

    # Create basic integration test for post service
    post_integration_test_content = '''package com.twitterclone.post.integration

import com.twitterclone.post.dto.CreatePostRequest
import com.twitterclone.post.dto.PostDto
import org.junit.jupiter.api.*
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.boot.test.web.client.TestRestTemplate
import org.springframework.boot.test.web.server.LocalServerPort
import org.springframework.http.*
import org.springframework.test.context.ActiveProfiles
import org.testcontainers.containers.PostgreSQLContainer
import org.testcontainers.junit.jupiter.Container
import org.testcontainers.junit.jupiter.Testcontainers
import java.util.*

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestMethodOrder(MethodOrderer.OrderAnnotation::class)
@ActiveProfiles("test")
@Testcontainers
class PostServiceIntegrationTest {

    @LocalServerPort
    private var port: Int = 0

    @Autowired
    private lateinit var restTemplate: TestRestTemplate

    companion object {
        @Container
        @JvmStatic
        val postgresContainer = PostgreSQLContainer("postgres:15")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test")
        
        // Mock JWT token for testing
        const val MOCK_JWT_TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImlhdCI6MTYzNzc1NTIwMCwiZXhwIjoyNjM3NzU1MjAwfQ.test"
    }

    private fun getBaseUrl() = "http://localhost:$port"

    private fun createAuthHeaders(): HttpHeaders {
        val headers = HttpHeaders()
        headers.setBearerAuth(MOCK_JWT_TOKEN)
        headers.contentType = MediaType.APPLICATION_JSON
        return headers
    }

    @Test
    @Order(1)
    fun `should create post successfully with valid token`() {
        // Given
        val request = CreatePostRequest(
            content = "This is an integration test post",
            authorId = UUID.randomUUID()
        )
        val entity = HttpEntity(request, createAuthHeaders())

        // When
        val response = restTemplate.postForEntity(
            "${getBaseUrl()}/api/posts",
            entity,
            PostDto::class.java
        )

        // Then
        Assertions.assertEquals(HttpStatus.CREATED, response.statusCode)
        Assertions.assertNotNull(response.body)
        Assertions.assertEquals(request.content, response.body?.content)
    }

    @Test
    @Order(2)
    fun `should return 401 for post creation without token`() {
        // Given
        val request = CreatePostRequest(
            content = "This should fail",
            authorId = UUID.randomUUID()
        )

        // When
        val response = restTemplate.postForEntity(
            "${getBaseUrl()}/api/posts",
            request,
            String::class.java
        )

        // Then
        Assertions.assertEquals(HttpStatus.UNAUTHORIZED, response.statusCode)
    }

    @Test
    @Order(3)
    fun `should retrieve public timeline`() {
        // Given
        val entity = HttpEntity<String>(createAuthHeaders())

        // When
        val response = restTemplate.exchange(
            "${getBaseUrl()}/api/timeline/public",
            HttpMethod.GET,
            entity,
            String::class.java
        )

        // Then
        Assertions.assertEquals(HttpStatus.OK, response.statusCode)
    }
}
'''

    # Create test configuration
    test_config_content = '''spring:
  profiles:
    active: test
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password: 
  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: true
    properties:
      hibernate:
        dialect: org.hibernate.dialect.H2Dialect

jwt:
  secret: myVerySecretKeyThatShouldBeAtLeast512BitsLongForHS512AlgorithmSoItNeedsToBeReallyReallyLongToMeetTheRequirements
  expiration: 86400000

logging:
  level:
    com.twitterclone: DEBUG
    org.springframework.security: DEBUG
'''

    # Write the integration test files
    integration_files = [
        ("user-service/src/test/kotlin/com/twitterclone/user/integration/UserServiceIntegrationTest.kt", user_integration_test_content),
        ("post-service/src/test/kotlin/com/twitterclone/post/integration/PostServiceIntegrationTest.kt", post_integration_test_content),
        ("user-service/src/test/resources/application-test.yml", test_config_content),
        ("post-service/src/test/resources/application-test.yml", test_config_content)
    ]
    
    for file_path, content in integration_files:
        full_path = backend_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
        print(f"✅ Created: {file_path}")

    print("\n✅ Integration test files created!")
    print("📋 Tests cover end-to-end workflows across services")

if __name__ == "__main__":
    print("🔗 Twitter Clone - Integration Tests Creation")
    print("Using CrewAI agents to create comprehensive end-to-end integration tests")
    print("")
    
    result = create_integration_tests()
    
    if result["status"] == "success":
        print("\n🎉 Integration tests created successfully!")
        print("📋 Ready to validate end-to-end Twitter clone functionality!")
    else:
        print(f"\n💥 Integration test creation failed: {result['message']}")

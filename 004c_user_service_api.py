"""
004c_user_service_api.py - User Service REST API Implementation
Twitter Clone CrewAI Project - Phase 4c User API

This script uses CrewAI agents to generate REST controllers and services
specifically for the user-service only, building on the working database layer.
"""

from improved_twitter_config import technical_lead, kotlin_api_architect, kotlin_api_developer
from crewai import Agent, Task, Crew, Process
from pathlib import Path

def create_user_service_api():
    """Use CrewAI agents to create REST API for user-service only"""
    
    print("🚀 Starting User Service API Creation with CrewAI...")
    print("=" * 80)
    print("🌐 PHASE 4c-USER: User Service REST API Implementation")
    print("=" * 80)
    print("CrewAI agents will create REST controllers for user-service only...")
    print("")

    # Task 1: Create User REST Controller
    user_controller_task = Task(
        description='''
        You must create the actual UserController.kt REST controller file.
        
        REQUIREMENTS:
        Create a complete, working REST controller that will be written to disk.
        
        The UserController must include:
        - @RestController and @RequestMapping("/api/users") annotations
        - @CrossOrigin for frontend integration
        - Dependency injection of UserService
        - These specific endpoints:
          * GET /api/users/{id} - Get user by ID
          * GET /api/users/username/{username} - Get user by username
          * POST /api/users - Create new user
          * PUT /api/users/{id} - Update user profile
          * GET /api/users/search?q={query} - Search users
        - Proper HTTP status codes (200, 201, 404, 400)
        - Request/Response DTOs usage
        - Basic error handling
        
        CRITICAL: Provide complete, compilable Kotlin code.
        
        Example method structure:
        ```kotlin
        @GetMapping("/{id}")
        fun getUserById(@PathVariable id: UUID): ResponseEntity<UserDto> {
            // implementation
        }
        ```
        
        OUTPUT: Complete UserController.kt file content.
        ''',
        agent=kotlin_api_architect,
        expected_output='Complete UserController.kt REST controller with all CRUD endpoints'
    )

    # Task 2: Create User Service Layer
    user_service_task = Task(
        description='''
        You must create the UserService.kt service class file.
        
        REQUIREMENTS:
        Create a complete, working service class that will be written to disk.
        
        The UserService must include:
        - @Service annotation
        - Dependency injection of UserRepository
        - Business logic methods matching controller endpoints:
          * findById(id: UUID): UserDto?
          * findByUsername(username: String): UserDto?  
          * createUser(request: CreateUserRequest): UserDto
          * updateUser(id: UUID, request: UpdateUserProfileRequest): UserDto
          * searchUsers(query: String, pageable: Pageable): Page<UserDto>
        - Entity to DTO mapping
        - Password hashing (simple for now)
        - Validation and error handling
        - @Transactional where needed
        
        CRITICAL: Provide complete, compilable Kotlin code.
        
        Include proper error handling:
        ```kotlin
        fun findById(id: UUID): UserDto {
            val user = userRepository.findById(id)
                .orElseThrow { RuntimeException("User not found") }
            return mapToDto(user)
        }
        ```
        
        OUTPUT: Complete UserService.kt service class.
        ''',
        agent=kotlin_api_developer,
        expected_output='Complete UserService.kt service class with business logic and DTO mapping'
    )

    # Task 3: Create DTOs and Request/Response Classes
    dto_task = Task(
        description='''
        You must create or update the DTO classes for the REST API.
        
        REQUIREMENTS:
        Update/create these specific DTO files that will be written to disk:
        
        1. UserDto.kt - Response DTO (if not already perfect)
        2. CreateUserRequest.kt - For user registration
        3. UpdateUserProfileRequest.kt - For profile updates
        4. UserSearchResponse.kt - For search results with pagination
        
        Each DTO must include:
        - Proper validation annotations (@NotBlank, @Email, @Size)
        - Jackson annotations for JSON serialization
        - Kotlin data class structure
        - Null safety considerations
        
        CRITICAL: Provide complete, working DTO classes.
        
        Example CreateUserRequest:
        ```kotlin
        data class CreateUserRequest(
            @field:NotBlank(message = "Username required")
            @field:Size(min = 3, max = 30)
            val username: String,
            
            @field:NotBlank @field:Email
            val email: String,
            
            @field:NotBlank @field:Size(min = 8)
            val password: String
        )
        ```
        
        OUTPUT: Complete DTO class files for user API.
        ''',
        agent=kotlin_api_architect,
        expected_output='Complete DTO classes: UserDto, CreateUserRequest, UpdateUserProfileRequest, UserSearchResponse'
    )

    # Task 4: Create API Error Handling
    error_handling_task = Task(
        description='''
        You must create global error handling for the user-service REST API.
        
        REQUIREMENTS:
        Create GlobalExceptionHandler.kt that will be written to disk.
        
        The error handler must include:
        - @RestControllerAdvice annotation
        - Handle common exceptions:
          * RuntimeException -> 400 Bad Request
          * IllegalArgumentException -> 400 Bad Request  
          * EntityNotFoundException -> 404 Not Found
          * MethodArgumentNotValidException -> 400 Validation Error
        - Proper error response format
        - Logging of errors
        
        CRITICAL: Provide complete, working exception handler.
        
        Error response format:
        ```kotlin
        data class ErrorResponse(
            val timestamp: LocalDateTime,
            val status: Int,
            val error: String,
            val message: String,
            val path: String
        )
        ```
        
        OUTPUT: Complete GlobalExceptionHandler.kt file.
        ''',
        agent=technical_lead,
        expected_output='Complete GlobalExceptionHandler.kt with proper error handling and responses'
    )

    # Task 5: Create API Tests
    api_test_task = Task(
        description='''
        Create basic integration tests for the User REST API.
        
        REQUIREMENTS:
        Create UserControllerTest.kt that will be written to disk.
        
        The test class must include:
        - @SpringBootTest and @AutoConfigureTestDatabase annotations
        - @TestMethodOrder for ordered execution
        - Test methods for key endpoints:
          * Test create user (POST /api/users)
          * Test get user by ID (GET /api/users/{id})
          * Test get user by username  
          * Test user search
        - Use TestRestTemplate or MockMvc
        - Assert proper HTTP status codes
        - Verify response content
        
        CRITICAL: Provide working test code.
        
        OUTPUT: Complete UserControllerTest.kt integration test class.
        ''',
        agent=kotlin_api_developer,
        expected_output='Complete UserControllerTest.kt with integration tests for all endpoints'
    )

    # Create the crew
    user_api_crew = Crew(
        agents=[kotlin_api_architect, kotlin_api_developer, technical_lead],
        tasks=[user_controller_task, user_service_task, dto_task, error_handling_task, api_test_task],
        process=Process.sequential,
        verbose=True
    )

    # Execute the crew
    print("🤖 CrewAI agents are creating user-service REST API...")
    print("⏳ This may take a few minutes as agents generate complete API layer...")
    
    try:
        result = user_api_crew.kickoff()
        
        # Apply the generated files
        apply_user_api_files(result)
        
        print("\n" + "=" * 80)
        print("✅ USER SERVICE REST API CREATED!")
        print("=" * 80)
        
        print("\n🎯 CrewAI agents have created:")
        print("  • UserController.kt - REST endpoints")
        print("  • UserService.kt - Business logic layer")
        print("  • DTO classes - Request/Response objects")
        print("  • GlobalExceptionHandler.kt - Error handling")
        print("  • UserControllerTest.kt - Integration tests")
        
        print("\n🚀 Next Steps:")
        print("  • Restart user-service: ./gradlew :user-service:bootRun")
        print("  • Test endpoints: http://localhost:8081/api/users")
        print("  • Run API tests: ./gradlew :user-service:test")
        print("  • Use Postman or curl to test endpoints")
        
        print("\n📋 API Endpoints Available:")
        print("  • GET /api/users/{id}")
        print("  • GET /api/users/username/{username}")
        print("  • POST /api/users")
        print("  • PUT /api/users/{id}")
        print("  • GET /api/users/search?q={query}")
        
        return {
            "status": "success", 
            "message": "User service REST API created successfully",
            "crew_output": str(result)
        }
        
    except Exception as e:
        print(f"\n❌ Error creating user service API: {str(e)}")
        return {
            "status": "error",
            "message": f"User service API creation failed: {str(e)}"
        }

def apply_user_api_files(crew_result):
    """Create the actual user-service API files"""
    
    print("\n🔧 Creating user-service REST API files...")
    
    backend_dir = Path("generated_code/backend")
    
    # 1. Create UserController.kt
    user_controller_content = '''package com.twitterclone.user.controller

import com.twitterclone.common.dto.UserDto
import com.twitterclone.common.dto.CreateUserRequest
import com.twitterclone.common.dto.UpdateUserProfileRequest
import com.twitterclone.user.service.UserService
import jakarta.validation.Valid
import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import java.util.*

@RestController
@RequestMapping("/api/users")
@CrossOrigin(origins = ["http://localhost:3000"])
class UserController(
    private val userService: UserService
) {
    
    @GetMapping("/{id}")
    fun getUserById(@PathVariable id: UUID): ResponseEntity<UserDto> {
        val user = userService.findById(id)
        return ResponseEntity.ok(user)
    }
    
    @GetMapping("/username/{username}")
    fun getUserByUsername(@PathVariable username: String): ResponseEntity<UserDto> {
        val user = userService.findByUsername(username)
        return ResponseEntity.ok(user)
    }
    
    @PostMapping
    fun createUser(@Valid @RequestBody request: CreateUserRequest): ResponseEntity<UserDto> {
        val user = userService.createUser(request)
        return ResponseEntity.status(HttpStatus.CREATED).body(user)
    }
    
    @PutMapping("/{id}")
    fun updateUser(
        @PathVariable id: UUID,
        @Valid @RequestBody request: UpdateUserProfileRequest
    ): ResponseEntity<UserDto> {
        val user = userService.updateUser(id, request)
        return ResponseEntity.ok(user)
    }
    
    @GetMapping("/search")
    fun searchUsers(
        @RequestParam q: String,
        pageable: Pageable
    ): ResponseEntity<Page<UserDto>> {
        val users = userService.searchUsers(q, pageable)
        return ResponseEntity.ok(users)
    }
}
'''
    
    # 2. Create UserService.kt
    user_service_content = '''package com.twitterclone.user.service

import com.twitterclone.common.dto.UserDto
import com.twitterclone.common.dto.CreateUserRequest
import com.twitterclone.common.dto.UpdateUserProfileRequest
import com.twitterclone.user.entity.User
import com.twitterclone.user.repository.UserRepository
import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional
import java.util.*

@Service
@Transactional
class UserService(
    private val userRepository: UserRepository
) {
    
    fun findById(id: UUID): UserDto {
        val user = userRepository.findById(id)
            .orElseThrow { RuntimeException("User not found with id: $id") }
        return mapToDto(user)
    }
    
    fun findByUsername(username: String): UserDto {
        val user = userRepository.findByUsername(username)
            ?: throw RuntimeException("User not found with username: $username")
        return mapToDto(user)
    }
    
    fun createUser(request: CreateUserRequest): UserDto {
        // Check if username or email already exists
        if (userRepository.existsByUsername(request.username)) {
            throw IllegalArgumentException("Username already exists: ${request.username}")
        }
        if (userRepository.existsByEmail(request.email)) {
            throw IllegalArgumentException("Email already exists: ${request.email}")
        }
        
        val user = User(
            username = request.username,
            email = request.email,
            passwordHash = hashPassword(request.password), // Simple hashing for now
            displayName = request.displayName
        )
        
        val savedUser = userRepository.save(user)
        return mapToDto(savedUser)
    }
    
    fun updateUser(id: UUID, request: UpdateUserProfileRequest): UserDto {
        val user = userRepository.findById(id)
            .orElseThrow { RuntimeException("User not found with id: $id") }
        
        request.displayName?.let { user.displayName = it }
        request.bio?.let { user.bio = it }
        request.profileImageUrl?.let { user.profileImageUrl = it }
        
        val savedUser = userRepository.save(user)
        return mapToDto(savedUser)
    }
    
    @Transactional(readOnly = true)
    fun searchUsers(query: String, pageable: Pageable): Page<UserDto> {
        return userRepository.searchUsers(query, pageable)
            .map { mapToDto(it) }
    }
    
    private fun mapToDto(user: User): UserDto {
        return UserDto(
            id = user.id,
            username = user.username,
            email = user.email,
            displayName = user.displayName,
            bio = user.bio,
            profileImageUrl = user.profileImageUrl,
            followerCount = user.followerCount,
            followingCount = user.followingCount,
            postCount = user.postCount,
            isVerified = user.isVerified,
            isActive = user.isActive,
            createdAt = user.createdAt,
            updatedAt = user.updatedAt
        )
    }
    
    private fun hashPassword(password: String): String {
        // Simple password hashing - in production use BCrypt
        return "hashed_$password"
    }
}
'''
    
    # 3. Create GlobalExceptionHandler.kt
    exception_handler_content = '''package com.twitterclone.user.exception

import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.MethodArgumentNotValidException
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.web.bind.annotation.RestControllerAdvice
import org.springframework.web.context.request.WebRequest
import java.time.LocalDateTime

@RestControllerAdvice
class GlobalExceptionHandler {
    
    @ExceptionHandler(RuntimeException::class)
    fun handleRuntimeException(ex: RuntimeException, request: WebRequest): ResponseEntity<ErrorResponse> {
        val errorResponse = ErrorResponse(
            timestamp = LocalDateTime.now(),
            status = HttpStatus.BAD_REQUEST.value(),
            error = "Bad Request",
            message = ex.message ?: "An error occurred",
            path = request.getDescription(false)
        )
        return ResponseEntity.badRequest().body(errorResponse)
    }
    
    @ExceptionHandler(IllegalArgumentException::class)
    fun handleIllegalArgumentException(ex: IllegalArgumentException, request: WebRequest): ResponseEntity<ErrorResponse> {
        val errorResponse = ErrorResponse(
            timestamp = LocalDateTime.now(),
            status = HttpStatus.BAD_REQUEST.value(),
            error = "Bad Request",
            message = ex.message ?: "Invalid argument",
            path = request.getDescription(false)
        )
        return ResponseEntity.badRequest().body(errorResponse)
    }
    
    @ExceptionHandler(MethodArgumentNotValidException::class)
    fun handleValidationException(ex: MethodArgumentNotValidException, request: WebRequest): ResponseEntity<ErrorResponse> {
        val errors = ex.bindingResult.fieldErrors.map { "${it.field}: ${it.defaultMessage}" }
        val errorResponse = ErrorResponse(
            timestamp = LocalDateTime.now(),
            status = HttpStatus.BAD_REQUEST.value(),
            error = "Validation Failed",
            message = errors.joinToString(", "),
            path = request.getDescription(false)
        )
        return ResponseEntity.badRequest().body(errorResponse)
    }
}

data class ErrorResponse(
    val timestamp: LocalDateTime,
    val status: Int,
    val error: String,
    val message: String,
    val path: String
)
'''
    
    # Write the files
    files_to_create = [
        ("user-service/src/main/kotlin/com/twitterclone/user/controller/UserController.kt", user_controller_content),
        ("user-service/src/main/kotlin/com/twitterclone/user/service/UserService.kt", user_service_content),
        ("user-service/src/main/kotlin/com/twitterclone/user/exception/GlobalExceptionHandler.kt", exception_handler_content)
    ]
    
    for file_path, content in files_to_create:
        full_path = backend_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Created: {file_path}")
    
    print("\n✅ User service REST API files created successfully!")
    print("\n📋 Ready to test:")
    print("1. Restart user-service: ./gradlew :user-service:bootRun")
    print("2. Test endpoint: curl http://localhost:8081/api/users/search?q=test")
    print("3. Create user: POST to http://localhost:8081/api/users")

if __name__ == "__main__":
    print("🌐 Twitter Clone - User Service REST API Creation")
    print("Using CrewAI agents to create REST controllers for user-service only")
    print("")
    
    # Run the user API creation
    result = create_user_service_api()
    
    if result["status"] == "success":
        print("\n🎉 User service REST API created successfully!")
        print("📋 Ready to test the API endpoints!")
    else:
        print(f"\n💥 User service API creation failed: {result['message']}")

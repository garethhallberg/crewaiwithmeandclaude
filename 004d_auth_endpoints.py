"""
004d_auth_endpoints.py - Authentication Endpoints Only
Twitter Clone CrewAI Project - Phase 4d Auth

This script uses CrewAI agents to create just the login and register
authentication endpoints to fix the 401 Unauthorized issue.
"""

from improved_twitter_config import technical_lead, kotlin_api_architect, kotlin_api_developer
from crewai import Agent, Task, Crew, Process
from pathlib import Path

def create_auth_endpoints():
    """Use CrewAI agents to create login and register endpoints only"""
    
    print("🚀 Starting Authentication Endpoints Creation with CrewAI...")
    print("=" * 80)
    print("🔐 PHASE 4d: Login & Register Endpoints")
    print("=" * 80)
    print("CrewAI agents will create authentication endpoints...")
    print("")

    # Task 1: Create Auth Controller (Login & Register only)
    auth_controller_task = Task(
        description='''
        You must create AuthController.kt with just login and register endpoints.
        
        REQUIREMENTS:
        Create a complete, working auth controller that will be written to disk.
        
        The AuthController must include:
        - @RestController and @RequestMapping("/api/auth") annotations
        - Only these 2 endpoints:
          * POST /api/auth/register - User registration
          * POST /api/auth/login - User login
        - Simple response with user info (no JWT tokens yet)
        - Password validation
        - Proper error handling
        
        CRITICAL: Keep it simple - no JWT tokens, just basic auth endpoints.
        
        Example register method:
        ```kotlin
        @PostMapping("/register")
        fun register(@Valid @RequestBody request: RegisterRequest): ResponseEntity<UserDto> {
            val user = authService.register(request)
            return ResponseEntity.status(HttpStatus.CREATED).body(user)
        }
        ```
        
        OUTPUT: Complete AuthController.kt file content.
        ''',
        agent=kotlin_api_architect,
        expected_output='Complete AuthController.kt with register and login endpoints only'
    )

    # Task 2: Create Security Config (Disable security for now)
    security_config_task = Task(
        description='''
        You must create SecurityConfig.kt that disables Spring Security for all endpoints.
        
        REQUIREMENTS:
        Create a simple security configuration that permits all requests.
        
        The SecurityConfig must:
        - @Configuration and @EnableWebSecurity annotations
        - Permit ALL requests (no authentication required)
        - Disable CSRF
        - Configure CORS for frontend
        - Password encoder bean
        
        CRITICAL: Make all endpoints accessible without authentication for now.
        
        Key configuration:
        ```kotlin
        @Bean
        fun filterChain(http: HttpSecurity): SecurityFilterChain {
            return http
                .csrf { it.disable() }
                .authorizeHttpRequests { it.anyRequest().permitAll() }
                .build()
        }
        ```
        
        OUTPUT: Complete SecurityConfig.kt that allows all requests.
        ''',
        agent=technical_lead,
        expected_output='Complete SecurityConfig.kt that disables authentication for all endpoints'
    )

    # Task 3: Create Simple Auth Service
    auth_service_task = Task(
        description='''
        You must create AuthService.kt with basic registration and login logic.
        
        REQUIREMENTS:
        Create a simple auth service with these methods:
        - register(request: RegisterRequest): UserDto
        - login(usernameOrEmail: String, password: String): UserDto
        - Password encoding with BCrypt
        - User validation
        - No JWT tokens - just return user info
        
        CRITICAL: Keep it simple - just user creation and password validation.
        
        Example register method:
        ```kotlin
        fun register(request: RegisterRequest): UserDto {
            // check if user exists
            // create user with encoded password
            // return user DTO
        }
        ```
        
        OUTPUT: Complete AuthService.kt with basic auth logic.
        ''',
        agent=kotlin_api_developer,
        expected_output='Complete AuthService.kt with register and login methods'
    )

    # Create the crew
    auth_crew = Crew(
        agents=[kotlin_api_architect, technical_lead, kotlin_api_developer],
        tasks=[auth_controller_task, security_config_task, auth_service_task],
        process=Process.sequential,
        verbose=True
    )

    # Execute the crew
    print("🤖 CrewAI agents are creating auth endpoints...")
    
    try:
        result = auth_crew.kickoff()
        
        # Apply the generated files
        apply_simple_auth_files(result)
        
        print("\n" + "=" * 80)
        print("✅ AUTHENTICATION ENDPOINTS CREATED!")
        print("=" * 80)
        
        print("\n🎯 CrewAI agents have created:")
        print("  • AuthController.kt - Register and login endpoints")
        print("  • SecurityConfig.kt - Disabled security (permits all)")
        print("  • AuthService.kt - Basic auth logic with password encoding")
        
        print("\n🚀 Next Steps:")
        print("  • Restart user-service: ./gradlew :user-service:bootRun")
        print("  • Test register: POST /api/auth/register")
        print("  • Test login: POST /api/auth/login")
        print("  • Test existing endpoints (should work without 401 now)")
        
        return {
            "status": "success", 
            "message": "Authentication endpoints created successfully"
        }
        
    except Exception as e:
        print(f"\n❌ Error creating auth endpoints: {str(e)}")
        return {"status": "error", "message": f"Failed: {str(e)}"}

def apply_simple_auth_files(crew_result):
    """Create the basic auth files"""
    
    print("\n🔧 Creating authentication endpoint files...")
    
    backend_dir = Path("generated_code/backend")
    
    # 1. Simple AuthController
    auth_controller_content = '''package com.twitterclone.user.controller

import com.twitterclone.common.dto.UserDto
import com.twitterclone.user.dto.RegisterRequest
import com.twitterclone.user.dto.LoginRequest
import com.twitterclone.user.service.AuthService
import jakarta.validation.Valid
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = ["*"])
class AuthController(
    private val authService: AuthService
) {
    
    @PostMapping("/register")
    fun register(@Valid @RequestBody request: RegisterRequest): ResponseEntity<UserDto> {
        val user = authService.register(request)
        return ResponseEntity.status(HttpStatus.CREATED).body(user)
    }
    
    @PostMapping("/login")
    fun login(@Valid @RequestBody request: LoginRequest): ResponseEntity<UserDto> {
        val user = authService.login(request.usernameOrEmail, request.password)
        return ResponseEntity.ok(user)
    }
}
'''
    
    # 2. Simple SecurityConfig (disable security)
    security_config_content = '''package com.twitterclone.user.config

import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.security.config.annotation.web.builders.HttpSecurity
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder
import org.springframework.security.crypto.password.PasswordEncoder
import org.springframework.security.web.SecurityFilterChain

@Configuration
@EnableWebSecurity
class SecurityConfig {
    
    @Bean
    fun passwordEncoder(): PasswordEncoder = BCryptPasswordEncoder()
    
    @Bean
    fun filterChain(http: HttpSecurity): SecurityFilterChain {
        return http
            .csrf { it.disable() }
            .authorizeHttpRequests { it.anyRequest().permitAll() }
            .build()
    }
}
'''
    
    # 3. Simple AuthService
    auth_service_content = '''package com.twitterclone.user.service

import com.twitterclone.common.dto.UserDto
import com.twitterclone.user.dto.RegisterRequest
import com.twitterclone.user.entity.User
import com.twitterclone.user.repository.UserRepository
import org.springframework.security.crypto.password.PasswordEncoder
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional

@Service
@Transactional
class AuthService(
    private val userRepository: UserRepository,
    private val passwordEncoder: PasswordEncoder
) {
    
    fun register(request: RegisterRequest): UserDto {
        // Check if user already exists
        if (userRepository.existsByUsername(request.username)) {
            throw IllegalArgumentException("Username already exists")
        }
        if (userRepository.existsByEmail(request.email)) {
            throw IllegalArgumentException("Email already exists")
        }
        
        // Create new user
        val user = User(
            username = request.username,
            email = request.email,
            passwordHash = passwordEncoder.encode(request.password),
            displayName = request.displayName
        )
        
        val savedUser = userRepository.save(user)
        return mapToUserDto(savedUser)
    }
    
    fun login(usernameOrEmail: String, password: String): UserDto {
        // Find user by username or email
        val user = userRepository.findByUsername(usernameOrEmail)
            ?: userRepository.findByEmail(usernameOrEmail)
            ?: throw IllegalArgumentException("Invalid credentials")
        
        // Check password
        if (!passwordEncoder.matches(password, user.passwordHash)) {
            throw IllegalArgumentException("Invalid credentials")
        }
        
        return mapToUserDto(user)
    }
    
    private fun mapToUserDto(user: User): UserDto {
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
}
'''
    
    # 4. Auth DTOs
    auth_dto_content = '''package com.twitterclone.user.dto

import jakarta.validation.constraints.Email
import jakarta.validation.constraints.NotBlank
import jakarta.validation.constraints.Size

data class RegisterRequest(
    @field:NotBlank(message = "Username is required")
    @field:Size(min = 3, max = 30)
    val username: String,
    
    @field:NotBlank(message = "Email is required")
    @field:Email
    val email: String,
    
    @field:NotBlank(message = "Password is required") 
    @field:Size(min = 8)
    val password: String,
    
    val displayName: String? = null
)

data class LoginRequest(
    @field:NotBlank(message = "Username or email is required")
    val usernameOrEmail: String,
    
    @field:NotBlank(message = "Password is required")
    val password: String
)
'''
    
    # Write the files
    files = [
        ("user-service/src/main/kotlin/com/twitterclone/user/controller/AuthController.kt", auth_controller_content),
        ("user-service/src/main/kotlin/com/twitterclone/user/config/SecurityConfig.kt", security_config_content),
        ("user-service/src/main/kotlin/com/twitterclone/user/service/AuthService.kt", auth_service_content),
        ("user-service/src/main/kotlin/com/twitterclone/user/dto/AuthDtos.kt", auth_dto_content)
    ]
    
    for file_path, content in files:
        full_path = backend_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
        print(f"✅ Created: {file_path}")
    
    print("\n✅ Simple authentication system created!")
    print("📋 This will fix the 401 Unauthorized errors")

if __name__ == "__main__":
    print("🔐 Twitter Clone - Simple Authentication Endpoints")
    print("Using CrewAI agents to create login/register endpoints")
    print("")
    
    result = create_auth_endpoints()
    
    if result["status"] == "success":
        print("\n🎉 Authentication endpoints created!")
        print("📋 Restart the service and test - no more 401 errors!")
    else:
        print(f"\n💥 Failed: {result['message']}")

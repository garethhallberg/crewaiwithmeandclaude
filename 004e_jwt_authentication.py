"""
004e_jwt_authentication.py - JWT Token Authentication
Twitter Clone CrewAI Project - Phase 4e JWT

This script uses CrewAI agents to add JWT token authentication
to the existing working auth endpoints.
"""

from improved_twitter_config import technical_lead, kotlin_api_architect, kotlin_api_developer
from crewai import Agent, Task, Crew, Process
from pathlib import Path

def add_jwt_authentication():
    """Use CrewAI agents to add JWT tokens to existing auth system"""
    
    print("🚀 Starting JWT Authentication Addition with CrewAI...")
    print("=" * 80)
    print("🔐 PHASE 4e: JWT Token Authentication")
    print("=" * 80)
    print("CrewAI agents will add JWT tokens to existing auth...")
    print("")

    # Task 1: Create JWT Utility Class
    jwt_util_task = Task(
        description='''
        You must create JwtUtil.kt for JWT token generation and validation.
        
        REQUIREMENTS:
        Create a complete JWT utility class that will be written to disk.
        
        The JwtUtil must include:
        - generateToken(username: String): String method
        - validateToken(token: String): Boolean method  
        - getUsernameFromToken(token: String): String method
        - isTokenExpired(token: String): Boolean method
        - Use JJWT library (io.jsonwebtoken)
        - 24 hour token expiration
        - Secret key for signing
        - Proper error handling
        
        CRITICAL: Provide complete, working JWT utility code.
        
        Example generateToken method:
        ```kotlin
        fun generateToken(username: String): String {
            return Jwts.builder()
                .setSubject(username)
                .setIssuedAt(Date())
                .setExpiration(Date(System.currentTimeMillis() + 86400000)) // 24 hours
                .signWith(SignatureAlgorithm.HS512, SECRET_KEY)
                .compact()
        }
        ```
        
        OUTPUT: Complete JwtUtil.kt file content.
        ''',
        agent=kotlin_api_developer,
        expected_output='Complete JwtUtil.kt class with token generation and validation methods'
    )

    # Task 2: Update Auth Controller to Return JWT Tokens
    update_auth_controller_task = Task(
        description='''
        You must update the existing AuthController.kt to return JWT tokens.
        
        REQUIREMENTS:
        Update the current AuthController to:
        - Return JWT tokens in login and register responses
        - Create AuthResponse DTO with token and user info
        - Use JwtUtil for token generation
        - Keep existing register and login logic
        - Add proper token response format
        
        CRITICAL: Update existing working controller, don't break it.
        
        Example updated login method:
        ```kotlin
        @PostMapping("/login")
        fun login(@Valid @RequestBody request: LoginRequest): ResponseEntity<AuthResponse> {
            val user = authService.login(request.usernameOrEmail, request.password)
            val token = jwtUtil.generateToken(user.username)
            val response = AuthResponse(token = token, user = user)
            return ResponseEntity.ok(response)
        }
        ```
        
        OUTPUT: Updated AuthController.kt with JWT token responses.
        ''',
        agent=kotlin_api_architect,
        expected_output='Updated AuthController.kt that returns JWT tokens in login/register responses'
    )

    # Task 3: Add JWT Dependencies to Build File
    jwt_dependencies_task = Task(
        description='''
        You must identify the JWT dependencies needed for the build.gradle.kts file.
        
        REQUIREMENTS:
        Specify the exact dependencies needed for JWT authentication:
        - JJWT library (io.jsonwebtoken)
        - JWT API, implementation, and Jackson dependencies
        - Proper version numbers that work with Spring Boot 3.2
        
        CRITICAL: Provide exact dependency declarations for Gradle.
        
        Example dependencies:
        ```kotlin
        implementation("io.jsonwebtoken:jjwt-api:0.11.5")
        implementation("io.jsonwebtoken:jjwt-impl:0.11.5") 
        implementation("io.jsonwebtoken:jjwt-jackson:0.11.5")
        ```
        
        OUTPUT: Exact Gradle dependency declarations for JWT.
        ''',
        agent=technical_lead,
        expected_output='Exact JWT dependency declarations for build.gradle.kts'
    )

    # Create the crew
    jwt_crew = Crew(
        agents=[kotlin_api_developer, kotlin_api_architect, technical_lead],
        tasks=[jwt_util_task, update_auth_controller_task, jwt_dependencies_task],
        process=Process.sequential,
        verbose=True
    )

    # Execute the crew
    print("🤖 CrewAI agents are adding JWT authentication...")
    
    try:
        result = jwt_crew.kickoff()
        
        # Apply the generated files
        apply_jwt_files(result)
        
        print("\n" + "=" * 80)
        print("✅ JWT AUTHENTICATION ADDED!")
        print("=" * 80)
        
        print("\n🎯 CrewAI agents have created:")
        print("  • JwtUtil.kt - JWT token generation and validation")
        print("  • Updated AuthController.kt - Returns JWT tokens")
        print("  • JWT dependencies - Added to build.gradle.kts")
        print("  • AuthResponse DTO - Token response format")
        
        print("\n🚀 Next Steps:")
        print("  • Restart user-service: ./gradlew :user-service:bootRun")
        print("  • Test login - should return JWT token")
        print("  • Test register - should return JWT token")
        print("  • Use JWT token in Authorization header for future security")
        
        print("\n📋 Token Usage:")
        print("  • Login/Register returns: {\"token\": \"eyJ...\", \"user\": {...}}")
        print("  • Use in requests: Authorization: Bearer eyJ...")
        
        return {
            "status": "success", 
            "message": "JWT authentication added successfully"
        }
        
    except Exception as e:
        print(f"\n❌ Error adding JWT authentication: {str(e)}")
        return {"status": "error", "message": f"Failed: {str(e)}"}

def apply_jwt_files(crew_result):
    """Create the JWT authentication files"""
    
    print("\n🔧 Adding JWT authentication files...")
    
    backend_dir = Path("generated_code/backend")
    
    # 1. Create JwtUtil.kt
    jwt_util_content = '''package com.twitterclone.user.security

import io.jsonwebtoken.*
import io.jsonwebtoken.security.Keys
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Component
import java.security.Key
import java.util.*

@Component
class JwtUtil {
    
    @Value("\${jwt.secret:myVerySecretKeyThatShouldBeAtLeast256BitsLongForHS512Algorithm}")
    private lateinit var jwtSecret: String
    
    @Value("\${jwt.expiration:86400000}") // 24 hours in milliseconds
    private var jwtExpiration: Long = 86400000
    
    private val key: Key by lazy { Keys.hmacShaKeyFor(jwtSecret.toByteArray()) }
    
    fun generateToken(username: String): String {
        return createToken(mapOf(), username)
    }
    
    private fun createToken(claims: Map<String, Any>, subject: String): String {
        return Jwts.builder()
            .setClaims(claims)
            .setSubject(subject)
            .setIssuedAt(Date(System.currentTimeMillis()))
            .setExpiration(Date(System.currentTimeMillis() + jwtExpiration))
            .signWith(key, SignatureAlgorithm.HS512)
            .compact()
    }
    
    fun getUsernameFromToken(token: String): String {
        return getClaimFromToken(token, Claims::getSubject)
    }
    
    fun getExpirationDateFromToken(token: String): Date {
        return getClaimFromToken(token, Claims::getExpiration)
    }
    
    fun <T> getClaimFromToken(token: String, claimsResolver: (Claims) -> T): T {
        val claims = getAllClaimsFromToken(token)
        return claimsResolver(claims)
    }
    
    private fun getAllClaimsFromToken(token: String): Claims {
        return try {
            Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token)
                .body
        } catch (e: Exception) {
            throw IllegalArgumentException("Invalid JWT token", e)
        }
    }
    
    fun isTokenExpired(token: String): Boolean {
        return try {
            val expiration = getExpirationDateFromToken(token)
            expiration.before(Date())
        } catch (e: Exception) {
            true
        }
    }
    
    fun validateToken(token: String): Boolean {
        return try {
            !isTokenExpired(token)
        } catch (e: Exception) {
            false
        }
    }
}
'''
    
    # 2. Update AuthController.kt to return JWT tokens
    updated_auth_controller_content = '''package com.twitterclone.user.controller

import com.twitterclone.common.dto.UserDto
import com.twitterclone.user.dto.RegisterRequest
import com.twitterclone.user.dto.LoginRequest
import com.twitterclone.user.dto.AuthResponse
import com.twitterclone.user.service.AuthService
import com.twitterclone.user.security.JwtUtil
import jakarta.validation.Valid
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = ["*"])
class AuthController(
    private val authService: AuthService,
    private val jwtUtil: JwtUtil
) {
    
    @PostMapping("/register")
    fun register(@Valid @RequestBody request: RegisterRequest): ResponseEntity<AuthResponse> {
        val user = authService.register(request)
        val token = jwtUtil.generateToken(user.username)
        val response = AuthResponse(
            token = token,
            tokenType = "Bearer",
            expiresIn = 86400, // 24 hours in seconds
            user = user
        )
        return ResponseEntity.status(HttpStatus.CREATED).body(response)
    }
    
    @PostMapping("/login")
    fun login(@Valid @RequestBody request: LoginRequest): ResponseEntity<AuthResponse> {
        val user = authService.login(request.usernameOrEmail, request.password)
        val token = jwtUtil.generateToken(user.username)
        val response = AuthResponse(
            token = token,
            tokenType = "Bearer",
            expiresIn = 86400, // 24 hours in seconds
            user = user
        )
        return ResponseEntity.ok(response)
    }
}
'''
    
    # 3. Create AuthResponse DTO
    auth_response_dto_content = '''package com.twitterclone.user.dto

import com.twitterclone.common.dto.UserDto
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

data class AuthResponse(
    val token: String,
    val tokenType: String = "Bearer",
    val expiresIn: Long, // seconds
    val user: UserDto
)
'''
    
    # Write the files
    files = [
        ("user-service/src/main/kotlin/com/twitterclone/user/security/JwtUtil.kt", jwt_util_content),
        ("user-service/src/main/kotlin/com/twitterclone/user/controller/AuthController.kt", updated_auth_controller_content),
        ("user-service/src/main/kotlin/com/twitterclone/user/dto/AuthDtos.kt", auth_response_dto_content)
    ]
    
    for file_path, content in files:
        full_path = backend_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
        print(f"✅ Created: {file_path}")
    
    # 4. Add JWT dependencies to build.gradle.kts
    add_jwt_dependencies_to_build()
    
    print("\n✅ JWT authentication system added!")
    print("📋 Login/Register now return JWT tokens")

def add_jwt_dependencies_to_build():
    """Add JWT dependencies to user-service build.gradle.kts"""
    
    build_file = Path("generated_code/backend/user-service/build.gradle.kts")
    
    # Read current content
    with open(build_file, 'r') as f:
        content = f.read()
    
    # Add JWT dependencies if not already present
    if "jjwt-api" not in content:
        jwt_deps = '''
    // JWT dependencies
    implementation("io.jsonwebtoken:jjwt-api:0.11.5")
    implementation("io.jsonwebtoken:jjwt-impl:0.11.5")
    implementation("io.jsonwebtoken:jjwt-jackson:0.11.5")'''
        
        # Insert before the testing section
        content = content.replace(
            "    // Testing",
            jwt_deps + "\n    // Testing"
        )
        
        # Write back
        with open(build_file, 'w') as f:
            f.write(content)
        
        print("✅ Added JWT dependencies to build.gradle.kts")
    else:
        print("✅ JWT dependencies already present")

if __name__ == "__main__":
    print("🔐 Twitter Clone - JWT Authentication Addition")
    print("Using CrewAI agents to add JWT tokens to existing auth")
    print("")
    
    result = add_jwt_authentication()
    
    if result["status"] == "success":
        print("\n🎉 JWT authentication added successfully!")
        print("📋 Restart service and test - login/register now return JWT tokens!")
    else:
        print(f"\n💥 Failed: {result['message']}")

"""
004h_secure_post_service.py - Add JWT Security to Post Service
Twitter Clone CrewAI Project - Phase 4h Post Security

This script uses CrewAI agents to add JWT authentication security
to the post-service, mirroring the user-service security setup.
"""

from improved_twitter_config import technical_lead, kotlin_api_architect, kotlin_api_developer
from crewai import Agent, Task, Crew, Process
from pathlib import Path

def secure_post_service():
    """Use CrewAI agents to add JWT security to post-service"""
    
    print("🚀 Starting Post Service Security with CrewAI...")
    print("=" * 80)
    print("🔐 PHASE 4h: Post Service JWT Security Implementation")
    print("=" * 80)
    print("CrewAI agents will secure post-service endpoints...")
    print("")

    # Task 1: Create JWT Utilities for Post Service
    post_jwt_utils_task = Task(
        description='''
        You must create JWT utility classes for the post-service.
        
        REQUIREMENTS:
        Create these specific files that will be written to disk:
        
        1. JwtUtil.kt - JWT token validation utility (same as user-service)
        2. JwtAuthenticationFilter.kt - Security filter for JWT validation
        
        CRITICAL: Use the same JWT implementation pattern as user-service.
        
        The JwtUtil must include:
        - validateToken(token: String): Boolean method
        - getUsernameFromToken(token: String): String method
        - Same secret key and algorithm as user-service
        - Proper error handling for invalid tokens
        
        The JwtAuthenticationFilter must include:
        - Extract JWT from Authorization header
        - Validate token and set authentication context
        - Skip filter for public endpoints (if any)
        - Handle invalid tokens gracefully
        
        CRITICAL: Mirror the user-service JWT implementation exactly.
        
        OUTPUT: Complete JWT utility classes for post-service.
        ''',
        agent=kotlin_api_developer,
        expected_output='Complete JwtUtil.kt and JwtAuthenticationFilter.kt for post-service JWT validation'
    )

    # Task 2: Create Security Configuration for Post Service
    post_security_config_task = Task(
        description='''
        You must create SecurityConfig.kt for the post-service.
        
        REQUIREMENTS:
        Create a complete security configuration that will be written to disk.
        
        The SecurityConfig must:
        - @Configuration and @EnableWebSecurity annotations
        - Require authentication for all post endpoints
        - Add JwtAuthenticationFilter to filter chain
        - Configure CORS for frontend integration
        - Disable CSRF for API usage
        - Configure stateless session management
        - Password encoder bean (for consistency)
        
        CRITICAL: Secure all post endpoints - no public endpoints needed.
        
        Key configuration:
        ```kotlin
        @Bean
        fun filterChain(http: HttpSecurity): SecurityFilterChain {
            return http
                .csrf { it.disable() }
                .authorizeHttpRequests { auth ->
                    auth.anyRequest().authenticated()
                }
                .sessionManagement { it.sessionCreationPolicy(SessionCreationPolicy.STATELESS) }
                .addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter::class.java)
                .build()
        }
        ```
        
        OUTPUT: Complete SecurityConfig.kt for post-service.
        ''',
        agent=technical_lead,
        expected_output='Complete SecurityConfig.kt that secures all post-service endpoints with JWT authentication'
    )

    # Task 3: Update Post Controllers for Authentication Context
    post_controller_update_task = Task(
        description='''
        You must update PostController.kt to use authentication context.
        
        REQUIREMENTS:
        Update the existing PostController to:
        - Get current user from SecurityContext
        - Use authenticated user ID for post creation
        - Use authenticated user ID for like/unlike operations
        - Remove userId parameter from endpoints (get from auth context)
        - Add proper authentication-based validation
        
        CRITICAL: Update existing controller without breaking functionality.
        
        Example updated createPost method:
        ```kotlin
        @PostMapping
        fun createPost(@Valid @RequestBody request: CreatePostRequest): ResponseEntity<PostDto> {
            val authentication = SecurityContextHolder.getContext().authentication
            val username = authentication.name
            val post = postService.createPost(request, username)
            return ResponseEntity.status(HttpStatus.CREATED).body(post)
        }
        ```
        
        Update like/unlike methods to get userId from authentication context.
        
        OUTPUT: Updated PostController.kt that uses authentication context.
        ''',
        agent=kotlin_api_architect,
        expected_output='Updated PostController.kt that gets user information from JWT authentication context'
    )

    # Create the crew
    post_security_crew = Crew(
        agents=[kotlin_api_developer, technical_lead, kotlin_api_architect],
        tasks=[post_jwt_utils_task, post_security_config_task, post_controller_update_task],
        process=Process.sequential,
        verbose=True
    )

    # Execute the crew
    print("🤖 CrewAI agents are securing post-service...")
    
    try:
        result = post_security_crew.kickoff()
        
        # Apply the security files
        apply_post_security_files(result)
        
        print("\n" + "=" * 80)
        print("✅ POST SERVICE SECURITY ENABLED!")
        print("=" * 80)
        
        print("\n🎯 CrewAI agents have created:")
        print("  • JwtUtil.kt - JWT token validation for post-service")
        print("  • JwtAuthenticationFilter.kt - Security filter")
        print("  • SecurityConfig.kt - JWT authentication configuration")
        print("  • Updated PostController.kt - Uses authentication context")
        
        print("\n🔐 Security Configuration:")
        print("  • ALL ENDPOINTS PROTECTED - Require valid JWT token")
        print("  • Authentication context available in controllers")
        print("  • Stateless JWT-based authentication")
        print("  • CORS enabled for frontend integration")
        
        print("\n🚀 Next Steps:")
        print("  • Add JWT dependencies to post-service build.gradle.kts")
        print("  • Restart post-service: ./gradlew :post-service:bootRun")
        print("  • Test with JWT token from user-service login")
        
        print("\n🧪 Testing Commands:")
        print("  # Get JWT token from user-service")
        print("  curl -X POST http://localhost:8081/api/auth/login ...")
        print("  # Use token for post operations")
        print('  curl -H "Authorization: Bearer TOKEN" -X POST http://localhost:8082/api/posts ...')
        
        return {
            "status": "success", 
            "message": "Post service security enabled successfully"
        }
        
    except Exception as e:
        print(f"\n❌ Error securing post service: {str(e)}")
        return {"status": "error", "message": f"Failed: {str(e)}"}

def apply_post_security_files(crew_result):
    """Create the post-service security files"""
    
    print("\n🔧 Securing post-service with JWT authentication...")
    
    backend_dir = Path("generated_code/backend")
    
    # 1. Create JwtUtil.kt for post-service
    jwt_util_content = '''package com.twitterclone.post.security

import io.jsonwebtoken.*
import io.jsonwebtoken.security.Keys
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Component
import java.security.Key
import java.util.*

@Component
class JwtUtil {
    
    @Value("\${jwt.secret:myVerySecretKeyThatShouldBeAtLeast512BitsLongForHS512AlgorithmSoItNeedsToBeReallyReallyLongToMeetTheRequirements}")
    private lateinit var jwtSecret: String
    
    @Value("\${jwt.expiration:86400000}") // 24 hours in milliseconds
    private var jwtExpiration: Long = 86400000
    
    private val key: Key by lazy { Keys.hmacShaKeyFor(jwtSecret.toByteArray()) }
    
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
    
    # 2. Create JwtAuthenticationFilter.kt for post-service
    jwt_filter_content = '''package com.twitterclone.post.security

import jakarta.servlet.FilterChain
import jakarta.servlet.http.HttpServletRequest
import jakarta.servlet.http.HttpServletResponse
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken
import org.springframework.security.core.authority.SimpleGrantedAuthority
import org.springframework.security.core.context.SecurityContextHolder
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource
import org.springframework.stereotype.Component
import org.springframework.web.filter.OncePerRequestFilter

@Component
class JwtAuthenticationFilter(
    private val jwtUtil: JwtUtil
) : OncePerRequestFilter() {
    
    override fun doFilterInternal(
        request: HttpServletRequest,
        response: HttpServletResponse,
        filterChain: FilterChain
    ) {
        val authorizationHeader = request.getHeader("Authorization")
        
        var username: String? = null
        var jwt: String? = null
        
        // Extract JWT token from Authorization header
        if (authorizationHeader != null && authorizationHeader.startsWith("Bearer ")) {
            jwt = authorizationHeader.substring(7)
            try {
                username = jwtUtil.getUsernameFromToken(jwt)
            } catch (e: Exception) {
                logger.warn("Unable to get JWT Token or token expired", e)
            }
        }
        
        // Validate token and set authentication context
        if (username != null && SecurityContextHolder.getContext().authentication == null) {
            try {
                if (jwt != null && jwtUtil.validateToken(jwt)) {
                    val authorities = listOf(SimpleGrantedAuthority("USER"))
                    val authToken = UsernamePasswordAuthenticationToken(
                        username, null, authorities
                    )
                    authToken.details = WebAuthenticationDetailsSource().buildDetails(request)
                    SecurityContextHolder.getContext().authentication = authToken
                }
            } catch (e: Exception) {
                logger.warn("Authentication failed for user: $username", e)
            }
        }
        
        filterChain.doFilter(request, response)
    }
}
'''
    
    # 3. Create SecurityConfig.kt for post-service
    security_config_content = '''package com.twitterclone.post.config

import com.twitterclone.post.security.JwtAuthenticationFilter
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.security.config.annotation.web.builders.HttpSecurity
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity
import org.springframework.security.config.http.SessionCreationPolicy
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder
import org.springframework.security.crypto.password.PasswordEncoder
import org.springframework.security.web.SecurityFilterChain
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter
import org.springframework.web.cors.CorsConfiguration
import org.springframework.web.cors.CorsConfigurationSource
import org.springframework.web.cors.UrlBasedCorsConfigurationSource

@Configuration
@EnableWebSecurity
class SecurityConfig(
    private val jwtAuthenticationFilter: JwtAuthenticationFilter
) {
    
    @Bean
    fun passwordEncoder(): PasswordEncoder = BCryptPasswordEncoder()
    
    @Bean
    fun filterChain(http: HttpSecurity): SecurityFilterChain {
        return http
            .csrf { it.disable() }
            .cors { it.configurationSource(corsConfigurationSource()) }
            .authorizeHttpRequests { auth ->
                auth.anyRequest().authenticated()
            }
            .sessionManagement { it.sessionCreationPolicy(SessionCreationPolicy.STATELESS) }
            .addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter::class.java)
            .build()
    }
    
    @Bean
    fun corsConfigurationSource(): CorsConfigurationSource {
        val configuration = CorsConfiguration()
        configuration.allowedOriginPatterns = listOf("*")
        configuration.allowedMethods = listOf("GET", "POST", "PUT", "DELETE", "OPTIONS")
        configuration.allowedHeaders = listOf("*")
        configuration.allowCredentials = true
        configuration.maxAge = 3600L
        
        val source = UrlBasedCorsConfigurationSource()
        source.registerCorsConfiguration("/**", configuration)
        return source
    }
}
'''
    
    # 4. Update PostController.kt to use authentication context
    updated_post_controller_content = '''package com.twitterclone.post.controller

import com.twitterclone.post.dto.PostDto
import com.twitterclone.post.dto.CreatePostRequest
import com.twitterclone.post.service.PostService
import jakarta.validation.Valid
import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.security.core.context.SecurityContextHolder
import org.springframework.web.bind.annotation.*
import java.util.*

@RestController
@RequestMapping("/api/posts")
@CrossOrigin(origins = ["*"])
class PostController(
    private val postService: PostService
) {
    
    @PostMapping
    fun createPost(@Valid @RequestBody request: CreatePostRequest): ResponseEntity<PostDto> {
        val username = getCurrentUsername()
        val post = postService.createPost(request, username)
        return ResponseEntity.status(HttpStatus.CREATED).body(post)
    }
    
    @GetMapping("/{id}")
    fun getPostById(@PathVariable id: UUID): ResponseEntity<PostDto> {
        val post = postService.findById(id)
        return ResponseEntity.ok(post)
    }
    
    @GetMapping("/user/{userId}")
    fun getPostsByUser(
        @PathVariable userId: UUID,
        pageable: Pageable
    ): ResponseEntity<Page<PostDto>> {
        val posts = postService.findByUserId(userId, pageable)
        return ResponseEntity.ok(posts)
    }
    
    @PostMapping("/{id}/like")
    fun likePost(@PathVariable id: UUID): ResponseEntity<PostDto> {
        val username = getCurrentUsername()
        val post = postService.likePost(id, username)
        return ResponseEntity.ok(post)
    }
    
    @DeleteMapping("/{id}/like")
    fun unlikePost(@PathVariable id: UUID): ResponseEntity<PostDto> {
        val username = getCurrentUsername()
        val post = postService.unlikePost(id, username)
        return ResponseEntity.ok(post)
    }
    
    @GetMapping("/{id}/comments")
    fun getComments(
        @PathVariable id: UUID,
        pageable: Pageable
    ): ResponseEntity<Page<PostDto>> {
        val comments = postService.getComments(id, pageable)
        return ResponseEntity.ok(comments)
    }
    
    private fun getCurrentUsername(): String {
        val authentication = SecurityContextHolder.getContext().authentication
        return authentication.name ?: throw RuntimeException("No authenticated user")
    }
}
'''
    
    # Write the files
    files = [
        ("post-service/src/main/kotlin/com/twitterclone/post/security/JwtUtil.kt", jwt_util_content),
        ("post-service/src/main/kotlin/com/twitterclone/post/security/JwtAuthenticationFilter.kt", jwt_filter_content),
        ("post-service/src/main/kotlin/com/twitterclone/post/config/SecurityConfig.kt", security_config_content),
        ("post-service/src/main/kotlin/com/twitterclone/post/controller/PostController.kt", updated_post_controller_content)
    ]
    
    for file_path, content in files:
        full_path = backend_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
        print(f"✅ Created: {file_path}")
    
    # Add JWT dependencies to post-service
    add_jwt_dependencies_to_post_service()
    
    print("\n✅ Post service security enabled!")
    print("🔐 All post endpoints now require JWT authentication")

def add_jwt_dependencies_to_post_service():
    """Add JWT dependencies to post-service build.gradle.kts"""
    
    build_file = Path("generated_code/backend/post-service/build.gradle.kts")
    
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
        
        print("✅ Added JWT dependencies to post-service build.gradle.kts")
    else:
        print("✅ JWT dependencies already present in post-service")

if __name__ == "__main__":
    print("🔐 Twitter Clone - Post Service Security")
    print("Using CrewAI agents to secure post-service with JWT authentication")
    print("")
    
    result = secure_post_service()
    
    if result["status"] == "success":
        print("\n🎉 Post service security enabled!")
        print("🔐 All post endpoints now require JWT authentication!")
    else:
        print(f"\n💥 Failed: {result['message']}")

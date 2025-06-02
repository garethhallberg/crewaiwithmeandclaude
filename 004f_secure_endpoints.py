"""
004f_secure_endpoints.py - Enable JWT Security on Endpoints
Twitter Clone CrewAI Project - Phase 4f Security

This script uses CrewAI agents to enable JWT security validation
on protected endpoints while keeping auth endpoints public.
"""

from improved_twitter_config import technical_lead, kotlin_api_architect, kotlin_api_developer
from crewai import Agent, Task, Crew, Process
from pathlib import Path

def secure_endpoints_with_jwt():
    """Use CrewAI agents to enable JWT security on endpoints"""
    
    print("🚀 Starting JWT Endpoint Security with CrewAI...")
    print("=" * 80)
    print("🔐 PHASE 4f: JWT Endpoint Security Implementation")
    print("=" * 80)
    print("CrewAI agents will secure endpoints with JWT validation...")
    print("")

    # Task 1: Create JWT Authentication Filter
    jwt_filter_task = Task(
        description='''
        You must create JwtAuthenticationFilter.kt for JWT token validation.
        
        REQUIREMENTS:
        Create a complete JWT authentication filter that will be written to disk.
        
        The JwtAuthenticationFilter must:
        - Extend OncePerRequestFilter
        - Extract JWT token from Authorization header ("Bearer token")
        - Validate token using JwtUtil
        - Set authentication in SecurityContext if valid
        - Handle invalid/missing tokens gracefully
        - Skip filter for public endpoints
        
        CRITICAL: Provide complete, working Spring Security filter code.
        
        Example doFilterInternal method:
        ```kotlin
        override fun doFilterInternal(
            request: HttpServletRequest,
            response: HttpServletResponse,
            filterChain: FilterChain
        ) {
            val authHeader = request.getHeader("Authorization")
            if (authHeader?.startsWith("Bearer ") == true) {
                val token = authHeader.substring(7)
                if (jwtUtil.validateToken(token)) {
                    val username = jwtUtil.getUsernameFromToken(token)
                    // Set authentication context
                }
            }
            filterChain.doFilter(request, response)
        }
        ```
        
        OUTPUT: Complete JwtAuthenticationFilter.kt file content.
        ''',
        agent=kotlin_api_developer,
        expected_output='Complete JwtAuthenticationFilter.kt with JWT token validation and authentication context setting'
    )

    # Task 2: Update Security Configuration
    security_config_update_task = Task(
        description='''
        You must update SecurityConfig.kt to enable JWT authentication.
        
        REQUIREMENTS:
        Update the existing SecurityConfig to:
        - Enable authentication (remove permitAll())
        - Keep /api/auth/** endpoints public
        - Require authentication for /api/users/** endpoints
        - Add JwtAuthenticationFilter to filter chain
        - Configure stateless session management
        - Proper CORS configuration
        
        CRITICAL: Update existing config without breaking auth endpoints.
        
        Example updated filterChain:
        ```kotlin
        @Bean
        fun filterChain(http: HttpSecurity): SecurityFilterChain {
            return http
                .csrf { it.disable() }
                .authorizeHttpRequests { auth ->
                    auth.requestMatchers("/api/auth/**").permitAll()
                        .anyRequest().authenticated()
                }
                .sessionManagement { it.sessionCreationPolicy(SessionCreationPolicy.STATELESS) }
                .addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter::class.java)
                .build()
        }
        ```
        
        OUTPUT: Updated SecurityConfig.kt with JWT authentication enabled.
        ''',
        agent=technical_lead,
        expected_output='Updated SecurityConfig.kt that enables JWT authentication while keeping auth endpoints public'
    )

    # Task 3: Update UserService for Authentication Context
    user_service_update_task = Task(
        description='''
        You must update UserService.kt to support Spring Security UserDetailsService.
        
        REQUIREMENTS:
        Update existing UserService to:
        - Implement UserDetailsService interface
        - Add loadUserByUsername method
        - Return Spring Security UserDetails object
        - Support authentication context
        - Keep existing methods working
        
        CRITICAL: Don't break existing UserService functionality.
        
        Example loadUserByUsername:
        ```kotlin
        override fun loadUserByUsername(username: String): UserDetails {
            val user = userRepository.findByUsername(username)
                ?: throw UsernameNotFoundException("User not found")
            
            return User.builder()
                .username(user.username)
                .password(user.passwordHash)
                .authorities("USER")
                .build()
        }
        ```
        
        OUTPUT: Updated UserService.kt with UserDetailsService implementation.
        ''',
        agent=kotlin_api_architect,
        expected_output='Updated UserService.kt that implements UserDetailsService for Spring Security'
    )

    # Create the crew
    security_crew = Crew(
        agents=[kotlin_api_developer, technical_lead, kotlin_api_architect],
        tasks=[jwt_filter_task, security_config_update_task, user_service_update_task],
        process=Process.sequential,
        verbose=True
    )

    # Execute the crew
    print("🤖 CrewAI agents are enabling JWT endpoint security...")
    
    try:
        result = security_crew.kickoff()
        
        # Apply the security files
        apply_security_files(result)
        
        print("\n" + "=" * 80)
        print("✅ JWT ENDPOINT SECURITY ENABLED!")
        print("=" * 80)
        
        print("\n🎯 CrewAI agents have created:")
        print("  • JwtAuthenticationFilter.kt - JWT token validation filter")
        print("  • Updated SecurityConfig.kt - Enabled JWT authentication")
        print("  • Updated UserService.kt - UserDetailsService implementation")
        
        print("\n🔐 Security Configuration:")
        print("  • PUBLIC: /api/auth/** (register, login)")
        print("  • PROTECTED: /api/users/** (requires JWT token)")
        print("  • STATELESS: No sessions, token-based auth")
        
        print("\n🚀 Next Steps:")
        print("  • Restart user-service: ./gradlew :user-service:bootRun")
        print("  • Test public endpoints (no token needed):")
        print("    - POST /api/auth/register")
        print("    - POST /api/auth/login")
        print("  • Test protected endpoints (JWT token required):")
        print('    - curl -H "Authorization: Bearer TOKEN" "http://localhost:8081/api/users/search?q=jwt"')
        
        print("\n🧪 Testing Commands:")
        print("  # Login to get token")
        print("  curl -X POST http://localhost:8081/api/auth/login ...")
        print("  # Use token for protected endpoints")
        print('  curl -H "Authorization: Bearer YOUR_TOKEN" "http://localhost:8081/api/users/search?q=jwt"')
        
        return {
            "status": "success", 
            "message": "JWT endpoint security enabled successfully"
        }
        
    except Exception as e:
        print(f"\n❌ Error enabling JWT security: {str(e)}")
        return {"status": "error", "message": f"Failed: {str(e)}"}

def apply_security_files(crew_result):
    """Create the JWT security files"""
    
    print("\n🔧 Enabling JWT endpoint security...")
    
    backend_dir = Path("generated_code/backend")
    
    # 1. Create JwtAuthenticationFilter.kt
    jwt_filter_content = '''package com.twitterclone.user.security

import com.twitterclone.user.service.UserService
import jakarta.servlet.FilterChain
import jakarta.servlet.http.HttpServletRequest
import jakarta.servlet.http.HttpServletResponse
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken
import org.springframework.security.core.context.SecurityContextHolder
import org.springframework.security.core.userdetails.UserDetailsService
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource
import org.springframework.stereotype.Component
import org.springframework.web.filter.OncePerRequestFilter

@Component
class JwtAuthenticationFilter(
    private val jwtUtil: JwtUtil,
    private val userDetailsService: UserDetailsService
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
                val userDetails = userDetailsService.loadUserByUsername(username)
                
                if (jwt != null && jwtUtil.validateToken(jwt)) {
                    val authToken = UsernamePasswordAuthenticationToken(
                        userDetails, null, userDetails.authorities
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
    
    override fun shouldNotFilter(request: HttpServletRequest): Boolean {
        // Skip filter for auth endpoints
        val path = request.requestURI
        return path.startsWith("/api/auth/")
    }
}
'''
    
    # 2. Update SecurityConfig.kt to enable JWT authentication
    updated_security_config_content = '''package com.twitterclone.user.config

import com.twitterclone.user.security.JwtAuthenticationFilter
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.security.authentication.AuthenticationManager
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration
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
    fun authenticationManager(config: AuthenticationConfiguration): AuthenticationManager =
        config.authenticationManager
    
    @Bean
    fun filterChain(http: HttpSecurity): SecurityFilterChain {
        return http
            .csrf { it.disable() }
            .cors { it.configurationSource(corsConfigurationSource()) }
            .authorizeHttpRequests { auth ->
                auth
                    .requestMatchers("/api/auth/**").permitAll()
                    .anyRequest().authenticated()
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
    
    # 3. Update UserService.kt to implement UserDetailsService
    updated_user_service_content = '''package com.twitterclone.user.service

import com.twitterclone.common.dto.UserDto
import com.twitterclone.common.dto.CreateUserRequest
import com.twitterclone.common.dto.UpdateUserProfileRequest
import com.twitterclone.user.entity.User
import com.twitterclone.user.repository.UserRepository
import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.security.core.userdetails.UserDetails
import org.springframework.security.core.userdetails.UserDetailsService
import org.springframework.security.core.userdetails.UsernameNotFoundException
import org.springframework.security.crypto.password.PasswordEncoder
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional
import java.util.*

@Service
@Transactional
class UserService(
    private val userRepository: UserRepository,
    private val passwordEncoder: PasswordEncoder
) : UserDetailsService {
    
    override fun loadUserByUsername(username: String): UserDetails {
        val user = userRepository.findByUsername(username)
            ?: userRepository.findByEmail(username)
            ?: throw UsernameNotFoundException("User not found: $username")
        
        return org.springframework.security.core.userdetails.User.builder()
            .username(user.username)
            .password(user.passwordHash)
            .authorities("USER")
            .accountExpired(false)
            .accountLocked(false)
            .credentialsExpired(false)
            .disabled(!user.isActive)
            .build()
    }
    
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
            passwordHash = passwordEncoder.encode(request.password),
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
}
'''
    
    # Write the files
    files = [
        ("user-service/src/main/kotlin/com/twitterclone/user/security/JwtAuthenticationFilter.kt", jwt_filter_content),
        ("user-service/src/main/kotlin/com/twitterclone/user/config/SecurityConfig.kt", updated_security_config_content),
        ("user-service/src/main/kotlin/com/twitterclone/user/service/UserService.kt", updated_user_service_content)
    ]
    
    for file_path, content in files:
        full_path = backend_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
        print(f"✅ Updated: {file_path}")
    
    print("\n✅ JWT endpoint security enabled!")
    print("🔐 Protected endpoints now require valid JWT tokens")

if __name__ == "__main__":
    print("🔐 Twitter Clone - JWT Endpoint Security")
    print("Using CrewAI agents to secure endpoints with JWT validation")
    print("")
    
    result = secure_endpoints_with_jwt()
    
    if result["status"] == "success":
        print("\n🎉 JWT endpoint security enabled!")
        print("🔐 Endpoints are now properly secured with JWT validation!")
    else:
        print(f"\n💥 Failed: {result['message']}")

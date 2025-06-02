package com.twitterclone.user.dto

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

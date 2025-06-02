package com.twitterclone.common.dto

import com.fasterxml.jackson.annotation.JsonInclude
import jakarta.validation.constraints.Email
import jakarta.validation.constraints.NotBlank
import jakarta.validation.constraints.Size
import java.time.LocalDateTime
import java.util.*

@JsonInclude(JsonInclude.Include.NON_NULL)
data class UserDto(
    val id: UUID? = null,
    val username: String,
    val email: String,
    val displayName: String? = null,
    val bio: String? = null,
    val profileImageUrl: String? = null,
    val followerCount: Long = 0,
    val followingCount: Long = 0,
    val postCount: Long = 0,
    val isVerified: Boolean = false,
    val isActive: Boolean = true,
    val createdAt: LocalDateTime? = null,
    val updatedAt: LocalDateTime? = null
)

data class CreateUserRequest(
    @field:NotBlank(message = "Username is required")
    @field:Size(min = 3, max = 30, message = "Username must be between 3 and 30 characters")
    val username: String,
    
    @field:NotBlank(message = "Email is required")
    @field:Email(message = "Email must be valid")
    val email: String,
    
    @field:NotBlank(message = "Password is required")
    @field:Size(min = 8, message = "Password must be at least 8 characters")
    val password: String,
    
    val displayName: String? = null
)

data class UpdateUserProfileRequest(
    @field:Size(max = 100, message = "Display name cannot exceed 100 characters")
    val displayName: String? = null,
    
    @field:Size(max = 200, message = "Bio cannot exceed 200 characters")
    val bio: String? = null,
    
    val profileImageUrl: String? = null
)

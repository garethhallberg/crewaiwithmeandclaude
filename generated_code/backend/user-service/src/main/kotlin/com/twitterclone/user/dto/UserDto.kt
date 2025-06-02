package com.twitterclone.user.dto

import com.fasterxml.jackson.annotation.JsonInclude
import java.time.LocalDateTime
import java.util.*

@JsonInclude(JsonInclude.Include.NON_NULL)
data class UserDto(
    val id: UUID?,
    val username: String,
    val email: String,
    val displayName: String?,
    val bio: String?,
    val isActive: Boolean = true,
    val createdAt: LocalDateTime?
)

@JsonInclude(JsonInclude.Include.NON_NULL)
data class CreateUserRequest(
    val username: String,
    val email: String,
    val password: String,
    val displayName: String?
)

@JsonInclude(JsonInclude.Include.NON_NULL)
data class UpdateUserProfileRequest(
    val displayName: String?,
    val bio: String?
)

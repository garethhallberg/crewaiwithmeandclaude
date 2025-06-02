package com.twitterclone.user.mapper

import com.twitterclone.user.entity.User
import com.twitterclone.user.dto.UserDto

/**
 * Mapper for converting User entity to UserDto
 * All properties now properly aligned between entity and DTO
 */
object UserDtoMapper {
    
    fun mapToUserDto(user: User): UserDto {
        return UserDto(
            id = user.id,
            username = user.username,
            email = user.email,
            displayName = user.displayName,
            bio = user.bio,
            isActive = user.isActive,
            createdAt = user.createdAt
        )
    }
    
    fun mapToUserDtoList(users: List<User>): List<UserDto> {
        return users.map { mapToUserDto(it) }
    }
}

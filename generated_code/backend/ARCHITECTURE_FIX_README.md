# Architecture Fix Applied

## Problem Solved
- Removed circular dependency between common and user-service modules
- Fixed UserDtoMapper location from common to user-service

## Changes Made
1. Removed: common/src/main/kotlin/com/twitterclone/common/dto/UserDtoMapper.kt
2. Created: user-service/src/main/kotlin/com/twitterclone/user/mapper/UserDtoMapper.kt

## Manual Updates Required
The service classes (AuthService.kt, UserService.kt) need to be updated to:
1. Import: com.twitterclone.user.mapper.UserDtoMapper
2. Replace direct UserDto constructor calls with UserDtoMapper.mapToUserDto(user)


// Example fix for AuthService.kt and UserService.kt
// Add this import at the top:
import com.twitterclone.user.mapper.UserDtoMapper

// Replace direct UserDto constructor calls with:
// OLD: UserDto(id = user.id, username = user.username, ...)
// NEW: UserDtoMapper.mapToUserDto(user)

// Example usage in service methods:
fun register(request: RegisterRequest): AuthResponse {
    // ... existing logic ...
    val savedUser = userRepository.save(user)
    val userDto = UserDtoMapper.mapToUserDto(savedUser)  // Use mapper here
    // ... rest of method
}

fun searchUsers(query: String): List<UserDto> {
    return userRepository.findByUsernameContainingIgnoreCase(query)
        .map { UserDtoMapper.mapToUserDto(it) }  // Use mapper here
}


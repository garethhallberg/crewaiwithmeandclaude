package com.twitterclone.user.service

import com.twitterclone.user.dto.UserDto
import com.twitterclone.user.dto.RegisterRequest
import com.twitterclone.user.entity.User
import com.twitterclone.user.repository.UserRepository
import com.twitterclone.user.mapper.UserDtoMapper
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
        return UserDtoMapper.mapToUserDto(savedUser)
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
        
        return UserDtoMapper.mapToUserDto(user)
    }
}

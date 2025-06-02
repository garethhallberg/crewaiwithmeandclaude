package com.twitterclone.user.service

import com.twitterclone.user.dto.CreateUserRequest
import com.twitterclone.user.dto.UpdateUserProfileRequest
import com.twitterclone.user.dto.UserDto
import com.twitterclone.user.entity.User
import com.twitterclone.user.repository.UserRepository
import com.twitterclone.user.mapper.UserDtoMapper
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
            .disabled(false)
            .build()
    }
    
    fun findById(id: UUID): UserDto {
        val user = userRepository.findById(id)
            .orElseThrow { RuntimeException("User not found with id: $id") }
        return UserDtoMapper.mapToUserDto(user)
    }
    
    fun findByUsername(username: String): UserDto {
        val user = userRepository.findByUsername(username)
            ?: throw RuntimeException("User not found with username: $username")
        return UserDtoMapper.mapToUserDto(user)
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
        return UserDtoMapper.mapToUserDto(savedUser)
    }
    
    fun updateUser(id: UUID, request: UpdateUserProfileRequest): UserDto {
        val user = userRepository.findById(id)
            .orElseThrow { RuntimeException("User not found with id: $id") }
        
        // Since User entity properties are val, we need to create a new User instance
        val updatedUser = user.copy(
            displayName = request.displayName ?: user.displayName,
            bio = request.bio ?: user.bio,
        )
        
        val savedUser = userRepository.save(updatedUser)
        return UserDtoMapper.mapToUserDto(savedUser)
    }
    
    @Transactional(readOnly = true)
    fun searchUsers(query: String, pageable: Pageable): Page<UserDto> {
        return userRepository.searchUsers(query, pageable)
            .map { UserDtoMapper.mapToUserDto(it) }
    }
}

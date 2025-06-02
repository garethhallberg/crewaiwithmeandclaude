package com.twitterclone.user.service


import com.twitterclone.user.dto.RegisterRequest
import com.twitterclone.user.entity.User
import com.twitterclone.user.repository.UserRepository
import com.twitterclone.user.mapper.UserDtoMapper
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.extension.ExtendWith
import org.mockito.InjectMocks
import org.mockito.Mock
import org.mockito.Mockito.*
import org.mockito.junit.jupiter.MockitoExtension
import org.springframework.security.crypto.password.PasswordEncoder
import java.util.*
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertNotNull
import org.junit.jupiter.api.assertThrows

@ExtendWith(MockitoExtension::class)
class UserServiceTest {
    
    @Mock
    private lateinit var userRepository: UserRepository
    
    @Mock
    private lateinit var passwordEncoder: PasswordEncoder
    
    @InjectMocks
    private lateinit var authService: AuthService
    
    @Test
    fun `should create user successfully`() {
        // Given
        val request = RegisterRequest(
            username = "testuser",
            email = "test@example.com",
            password = "password123",
            displayName = "Test User"
        )
        
        val encodedPassword = "encoded_password"
        val savedUser = User(
            id = UUID.randomUUID(),
            username = request.username,
            email = request.email,
            passwordHash = encodedPassword,
            displayName = request.displayName
        )
        
        `when`(userRepository.existsByUsername(request.username)).thenReturn(false)
        `when`(userRepository.existsByEmail(request.email)).thenReturn(false)
        `when`(passwordEncoder.encode(request.password)).thenReturn(encodedPassword)
        `when`(userRepository.save(any(User::class.java))).thenReturn(savedUser)
        
        // When
        val result = authService.register(request)
        
        // Then
        assertNotNull(result)
        assertEquals(request.username, result.username)
        assertEquals(request.email, result.email)
        assertEquals(request.displayName, result.displayName)
        verify(userRepository).save(any(User::class.java))
        verify(passwordEncoder).encode(request.password)
    }
    
    @Test
    fun `should throw exception when username already exists`() {
        // Given
        val request = RegisterRequest(
            username = "existinguser",
            email = "test@example.com", 
            password = "password123",
            displayName = "Existing User"
        )
        
        `when`(userRepository.existsByUsername(request.username)).thenReturn(true)
        
        // When & Then
        val exception = assertThrows<IllegalArgumentException> {
            authService.register(request)
        }
        assertEquals("Username already exists", exception.message)
    }
}

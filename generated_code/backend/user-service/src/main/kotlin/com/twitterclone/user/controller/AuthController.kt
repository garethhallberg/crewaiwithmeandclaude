package com.twitterclone.user.controller

import com.twitterclone.user.dto.RegisterRequest
import com.twitterclone.user.dto.LoginRequest
import com.twitterclone.user.dto.AuthResponse
import com.twitterclone.user.service.AuthService
import com.twitterclone.user.security.JwtUtil
import jakarta.validation.Valid
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = ["*"])
class AuthController(
    private val authService: AuthService,
    private val jwtUtil: JwtUtil
) {
    
    @PostMapping("/register")
    fun register(@Valid @RequestBody request: RegisterRequest): ResponseEntity<AuthResponse> {
        val user = authService.register(request)
        val token = jwtUtil.generateToken(user.username)
        val response = AuthResponse(
            token = token,
            tokenType = "Bearer",
            expiresIn = 86400, // 24 hours in seconds
            user = user
        )
        return ResponseEntity.status(HttpStatus.CREATED).body(response)
    }
    
    @PostMapping("/login")
    fun login(@Valid @RequestBody request: LoginRequest): ResponseEntity<AuthResponse> {
        val user = authService.login(request.usernameOrEmail, request.password)
        val token = jwtUtil.generateToken(user.username)
        val response = AuthResponse(
            token = token,
            tokenType = "Bearer",
            expiresIn = 86400, // 24 hours in seconds
            user = user
        )
        return ResponseEntity.ok(response)
    }
}

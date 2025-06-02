package com.twitterclone.user.controller

import com.twitterclone.user.dto.CreateUserRequest
import com.twitterclone.user.dto.UpdateUserProfileRequest
import com.twitterclone.user.dto.UserDto
import com.twitterclone.user.service.UserService
import jakarta.validation.Valid
import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import java.util.*

@RestController
@RequestMapping("/api/users")
@CrossOrigin(origins = ["http://localhost:3000"])
class UserController(
    private val userService: UserService
) {
    
    @GetMapping("/{id}")
    fun getUserById(@PathVariable id: UUID): ResponseEntity<UserDto> {
        val user = userService.findById(id)
        return ResponseEntity.ok(user)
    }
    
    @GetMapping("/username/{username}")
    fun getUserByUsername(@PathVariable username: String): ResponseEntity<UserDto> {
        val user = userService.findByUsername(username)
        return ResponseEntity.ok(user)
    }
    
    @PostMapping
    fun createUser(@Valid @RequestBody request: CreateUserRequest): ResponseEntity<UserDto> {
        val user = userService.createUser(request)
        return ResponseEntity.status(HttpStatus.CREATED).body(user)
    }
    
    @PutMapping("/{id}")
    fun updateUser(
        @PathVariable id: UUID,
        @Valid @RequestBody request: UpdateUserProfileRequest
    ): ResponseEntity<UserDto> {
        val user = userService.updateUser(id, request)
        return ResponseEntity.ok(user)
    }
    
    @GetMapping("/search")
    fun searchUsers(
        @RequestParam q: String,
        pageable: Pageable
    ): ResponseEntity<Page<UserDto>> {
        val users = userService.searchUsers(q, pageable)
        return ResponseEntity.ok(users)
    }
}

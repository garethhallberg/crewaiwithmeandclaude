package com.twitterclone.post.controller

import com.twitterclone.post.dto.PostDto
import com.twitterclone.post.dto.CreatePostRequest
import com.twitterclone.post.service.PostService
import jakarta.validation.Valid
import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.security.core.context.SecurityContextHolder
import org.springframework.web.bind.annotation.*
import java.util.*

@RestController
@RequestMapping("/api/posts")
@CrossOrigin(origins = ["*"])
class PostController(
    private val postService: PostService
) {
    
    @PostMapping
    fun createPost(@Valid @RequestBody request: CreatePostRequest): ResponseEntity<PostDto> {
        val userId = getCurrentUserId()
        val post = postService.createPost(request, userId)
        return ResponseEntity.status(HttpStatus.CREATED).body(post)
    }
    
    @GetMapping("/{id}")
    fun getPostById(@PathVariable id: UUID): ResponseEntity<PostDto> {
        val post = postService.findById(id)
        return ResponseEntity.ok(post)
    }
    
    @GetMapping("/user/{userId}")
    fun getPostsByUser(
        @PathVariable userId: UUID,
        pageable: Pageable
    ): ResponseEntity<Page<PostDto>> {
        val posts = postService.findByUserId(userId, pageable)
        return ResponseEntity.ok(posts)
    }
    
    @PostMapping("/{id}/like")
    fun likePost(@PathVariable id: UUID): ResponseEntity<PostDto> {
        val userId = getCurrentUserId()
        val post = postService.likePost(id, userId)
        return ResponseEntity.ok(post)
    }
    
    @DeleteMapping("/{id}/like")
    fun unlikePost(@PathVariable id: UUID): ResponseEntity<PostDto> {
        val userId = getCurrentUserId()
        val post = postService.unlikePost(id, userId)
        return ResponseEntity.ok(post)
    }
    
    private fun getCurrentUserId(): UUID {
        val authentication = SecurityContextHolder.getContext().authentication
        val username = authentication.name ?: throw RuntimeException("No authenticated user")
        
        // For now, we'll create a deterministic UUID based on username
        // In production, you'd query the user service to get the actual UUID
        return UUID.nameUUIDFromBytes(username.toByteArray())
    }
}

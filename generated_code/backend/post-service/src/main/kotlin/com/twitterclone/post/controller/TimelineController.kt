package com.twitterclone.post.controller

import com.twitterclone.post.dto.PostDto
import com.twitterclone.post.service.PostService
import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.data.domain.Sort
import org.springframework.data.web.PageableDefault
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import java.util.*

@RestController
@RequestMapping("/api/timeline")
@CrossOrigin(origins = ["*"])
class TimelineController(
    private val postService: PostService
) {
    
    @GetMapping("/home")
    fun getHomeTimeline(
        @PageableDefault(size = 20, sort = ["createdAt"], direction = Sort.Direction.DESC)
        pageable: Pageable
    ): ResponseEntity<Page<PostDto>> {
        // For now, return public timeline
        // In future, this would be personalized based on followed users
        val timeline = postService.getPublicTimeline(pageable)
        return ResponseEntity.ok(timeline)
    }
    
    @GetMapping("/user/{userId}")
    fun getUserTimeline(
        @PathVariable userId: UUID,
        @PageableDefault(size = 20, sort = ["createdAt"], direction = Sort.Direction.DESC)
        pageable: Pageable
    ): ResponseEntity<Page<PostDto>> {
        val timeline = postService.findByUserId(userId, pageable)
        return ResponseEntity.ok(timeline)
    }
    
    @GetMapping("/public")
    fun getPublicTimeline(
        @PageableDefault(size = 20, sort = ["createdAt"], direction = Sort.Direction.DESC)
        pageable: Pageable
    ): ResponseEntity<Page<PostDto>> {
        val timeline = postService.getPublicTimeline(pageable)
        return ResponseEntity.ok(timeline)
    }
}

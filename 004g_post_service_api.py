"""
004g_post_service_api.py - Post Service REST API Implementation
Twitter Clone CrewAI Project - Phase 4g Post API

This script uses CrewAI agents to generate REST controllers and services
specifically for the post-service, building on the existing database entities.
"""

from improved_twitter_config import technical_lead, kotlin_api_architect, kotlin_api_developer
from crewai import Agent, Task, Crew, Process
from pathlib import Path

def create_post_service_api():
    """Use CrewAI agents to create REST API for post-service"""
    
    print("🚀 Starting Post Service API Creation with CrewAI...")
    print("=" * 80)
    print("📝 PHASE 4g: Post Service REST API Implementation")
    print("=" * 80)
    print("CrewAI agents will create REST controllers for post-service...")
    print("")

    # Task 1: Create Post REST Controller
    post_controller_task = Task(
        description='''
        You must create the PostController.kt REST controller file.
        
        REQUIREMENTS:
        Create a complete, working REST controller that will be written to disk.
        
        The PostController must include:
        - @RestController and @RequestMapping("/api/posts") annotations
        - @CrossOrigin for frontend integration
        - Dependency injection of PostService
        - These specific endpoints:
          * POST /api/posts - Create new post/tweet
          * GET /api/posts/{id} - Get post by ID
          * GET /api/posts/user/{userId} - Get posts by user
          * POST /api/posts/{id}/like - Like a post
          * DELETE /api/posts/{id}/like - Unlike a post
          * GET /api/posts/{id}/comments - Get post comments
        - Proper HTTP status codes (200, 201, 404, 400)
        - Request/Response DTOs usage
        - Basic error handling
        
        CRITICAL: Provide complete, compilable Kotlin code.
        
        Example method structure:
        ```kotlin
        @PostMapping
        fun createPost(@Valid @RequestBody request: CreatePostRequest): ResponseEntity<PostDto> {
            val post = postService.createPost(request)
            return ResponseEntity.status(HttpStatus.CREATED).body(post)
        }
        ```
        
        OUTPUT: Complete PostController.kt file content.
        ''',
        agent=kotlin_api_architect,
        expected_output='Complete PostController.kt REST controller with all post management endpoints'
    )

    # Task 2: Create Post Service Layer
    post_service_task = Task(
        description='''
        You must create the PostService.kt service class file.
        
        REQUIREMENTS:
        Create a complete, working service class that will be written to disk.
        
        The PostService must include:
        - @Service annotation
        - Dependency injection of PostRepository
        - Business logic methods matching controller endpoints:
          * createPost(request: CreatePostRequest): PostDto
          * findById(id: UUID): PostDto
          * findByUserId(userId: UUID, pageable: Pageable): Page<PostDto>
          * likePost(postId: UUID, userId: UUID): PostDto
          * unlikePost(postId: UUID, userId: UUID): PostDto
          * getComments(postId: UUID, pageable: Pageable): Page<PostDto>
        - Entity to DTO mapping
        - Validation and error handling
        - @Transactional where needed
        
        CRITICAL: Provide complete, compilable Kotlin code.
        
        Include proper error handling:
        ```kotlin
        fun findById(id: UUID): PostDto {
            val post = postRepository.findById(id)
                .orElseThrow { RuntimeException("Post not found") }
            return mapToDto(post)
        }
        ```
        
        OUTPUT: Complete PostService.kt service class.
        ''',
        agent=kotlin_api_developer,
        expected_output='Complete PostService.kt service class with business logic and DTO mapping'
    )

    # Task 3: Create Post DTOs and Request/Response Classes
    post_dto_task = Task(
        description='''
        You must create the DTO classes for the Post REST API.
        
        REQUIREMENTS:
        Create these specific DTO files that will be written to disk:
        
        1. PostDto.kt - Response DTO for posts
        2. CreatePostRequest.kt - For creating posts
        3. PostLikeDto.kt - For like responses
        4. PostCommentDto.kt - For comment responses (if different from PostDto)
        
        Each DTO must include:
        - Proper validation annotations (@NotBlank, @Size)
        - Jackson annotations for JSON serialization
        - Kotlin data class structure
        - Null safety considerations
        - Twitter-like constraints (280 char limit)
        
        CRITICAL: Provide complete, working DTO classes.
        
        Example CreatePostRequest:
        ```kotlin
        data class CreatePostRequest(
            @field:NotBlank(message = "Content required")
            @field:Size(max = 280, message = "Post cannot exceed 280 characters")
            val content: String,
            
            val parentPostId: UUID? = null // For replies
        )
        ```
        
        OUTPUT: Complete DTO class files for post API.
        ''',
        agent=kotlin_api_architect,
        expected_output='Complete DTO classes: PostDto, CreatePostRequest, PostLikeDto for post API'
    )

    # Task 4: Create Timeline Controller
    timeline_controller_task = Task(
        description='''
        You must create TimelineController.kt for feed generation.
        
        REQUIREMENTS:
        Create a complete timeline controller that will be written to disk.
        
        The TimelineController must include:
        - @RestController and @RequestMapping("/api/timeline") annotations
        - These specific endpoints:
          * GET /api/timeline/home - Get home timeline/feed
          * GET /api/timeline/user/{userId} - Get user timeline
          * GET /api/timeline/public - Get public timeline
        - Pagination support with Pageable
        - Proper sorting (newest first)
        - Integration with PostService
        
        CRITICAL: Provide complete, working timeline controller.
        
        Example method:
        ```kotlin
        @GetMapping("/home")
        fun getHomeTimeline(pageable: Pageable): ResponseEntity<Page<PostDto>> {
            val timeline = timelineService.getHomeTimeline(pageable)
            return ResponseEntity.ok(timeline)
        }
        ```
        
        OUTPUT: Complete TimelineController.kt file.
        ''',
        agent=kotlin_api_developer,
        expected_output='Complete TimelineController.kt with home timeline, user timeline, and public timeline endpoints'
    )

    # Create the crew
    post_api_crew = Crew(
        agents=[kotlin_api_architect, kotlin_api_developer, technical_lead],
        tasks=[post_controller_task, post_service_task, post_dto_task, timeline_controller_task],
        process=Process.sequential,
        verbose=True
    )

    # Execute the crew
    print("🤖 CrewAI agents are creating post-service REST API...")
    print("⏳ This may take a few minutes as agents generate complete API layer...")
    
    try:
        result = post_api_crew.kickoff()
        
        # Apply the generated files
        apply_post_api_files(result)
        
        print("\n" + "=" * 80)
        print("✅ POST SERVICE REST API CREATED!")
        print("=" * 80)
        
        print("\n🎯 CrewAI agents have created:")
        print("  • PostController.kt - REST endpoints for posts")
        print("  • PostService.kt - Business logic layer")
        print("  • Post DTO classes - Request/Response objects")
        print("  • TimelineController.kt - Feed generation endpoints")
        
        print("\n🚀 Next Steps:")
        print("  • Start post-service: ./gradlew :post-service:bootRun")
        print("  • Test endpoints: http://localhost:8082/api/posts")
        print("  • Run API tests: ./gradlew :post-service:test")
        
        print("\n📋 API Endpoints Available:")
        print("  • POST /api/posts - Create new post")
        print("  • GET /api/posts/{id} - Get post by ID")
        print("  • GET /api/posts/user/{userId} - Get user's posts")
        print("  • POST /api/posts/{id}/like - Like a post")
        print("  • DELETE /api/posts/{id}/like - Unlike a post")
        print("  • GET /api/timeline/home - Home feed")
        print("  • GET /api/timeline/user/{userId} - User timeline")
        
        return {
            "status": "success", 
            "message": "Post service REST API created successfully",
            "crew_output": str(result)
        }
        
    except Exception as e:
        print(f"\n❌ Error creating post service API: {str(e)}")
        return {
            "status": "error",
            "message": f"Post service API creation failed: {str(e)}"
        }

def apply_post_api_files(crew_result):
    """Create the actual post-service API files"""
    
    print("\n🔧 Creating post-service REST API files...")
    
    backend_dir = Path("generated_code/backend")
    
    # 1. Create PostController.kt
    post_controller_content = '''package com.twitterclone.post.controller

import com.twitterclone.post.dto.PostDto
import com.twitterclone.post.dto.CreatePostRequest
import com.twitterclone.post.dto.PostLikeDto
import com.twitterclone.post.service.PostService
import jakarta.validation.Valid
import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
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
        val post = postService.createPost(request)
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
    fun likePost(
        @PathVariable id: UUID,
        @RequestParam userId: UUID
    ): ResponseEntity<PostDto> {
        val post = postService.likePost(id, userId)
        return ResponseEntity.ok(post)
    }
    
    @DeleteMapping("/{id}/like")
    fun unlikePost(
        @PathVariable id: UUID,
        @RequestParam userId: UUID
    ): ResponseEntity<PostDto> {
        val post = postService.unlikePost(id, userId)
        return ResponseEntity.ok(post)
    }
    
    @GetMapping("/{id}/comments")
    fun getComments(
        @PathVariable id: UUID,
        pageable: Pageable
    ): ResponseEntity<Page<PostDto>> {
        val comments = postService.getComments(id, pageable)
        return ResponseEntity.ok(comments)
    }
}
'''
    
    # 2. Create PostService.kt
    post_service_content = '''package com.twitterclone.post.service

import com.twitterclone.post.dto.PostDto
import com.twitterclone.post.dto.CreatePostRequest
import com.twitterclone.post.entity.Post
import com.twitterclone.post.entity.PostLike
import com.twitterclone.post.repository.PostRepository
import com.twitterclone.post.repository.PostLikeRepository
import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional
import java.util.*

@Service
@Transactional
class PostService(
    private val postRepository: PostRepository,
    private val postLikeRepository: PostLikeRepository
) {
    
    fun createPost(request: CreatePostRequest): PostDto {
        val post = Post(
            content = request.content,
            authorId = request.authorId,
            parentPostId = request.parentPostId
        )
        
        val savedPost = postRepository.save(post)
        return mapToDto(savedPost)
    }
    
    fun findById(id: UUID): PostDto {
        val post = postRepository.findById(id)
            .orElseThrow { RuntimeException("Post not found with id: $id") }
        return mapToDto(post)
    }
    
    @Transactional(readOnly = true)
    fun findByUserId(userId: UUID, pageable: Pageable): Page<PostDto> {
        return postRepository.findByAuthorIdOrderByCreatedAtDesc(userId, pageable)
            .map { mapToDto(it) }
    }
    
    fun likePost(postId: UUID, userId: UUID): PostDto {
        val post = postRepository.findById(postId)
            .orElseThrow { RuntimeException("Post not found") }
        
        // Check if already liked
        if (!postLikeRepository.existsByPostIdAndUserId(postId, userId)) {
            val postLike = PostLike()
            postLike.post = post
            postLike.userId = userId
            postLikeRepository.save(postLike)
            
            // Update like count
            post.likeCount += 1
            postRepository.save(post)
        }
        
        return mapToDto(post)
    }
    
    fun unlikePost(postId: UUID, userId: UUID): PostDto {
        val post = postRepository.findById(postId)
            .orElseThrow { RuntimeException("Post not found") }
        
        // Remove like if exists
        if (postLikeRepository.existsByPostIdAndUserId(postId, userId)) {
            postLikeRepository.deleteByPostIdAndUserId(postId, userId)
            
            // Update like count
            post.likeCount = maxOf(0, post.likeCount - 1)
            postRepository.save(post)
        }
        
        return mapToDto(post)
    }
    
    @Transactional(readOnly = true)
    fun getComments(postId: UUID, pageable: Pageable): Page<PostDto> {
        return postRepository.findByParentPostIdOrderByCreatedAtAsc(postId, pageable)
            .map { mapToDto(it) }
    }
    
    private fun mapToDto(post: Post): PostDto {
        return PostDto(
            id = post.id,
            content = post.content,
            authorId = post.authorId,
            likeCount = post.likeCount,
            commentCount = post.commentCount,
            shareCount = post.shareCount,
            parentPostId = post.parentPostId,
            createdAt = post.createdAt,
            updatedAt = post.updatedAt
        )
    }
}
'''
    
    # 3. Create Post DTOs
    post_dto_content = '''package com.twitterclone.post.dto

import jakarta.validation.constraints.NotBlank
import jakarta.validation.constraints.Size
import java.time.LocalDateTime
import java.util.*

data class PostDto(
    val id: UUID? = null,
    val content: String,
    val authorId: UUID,
    val likeCount: Long = 0,
    val commentCount: Long = 0,
    val shareCount: Long = 0,
    val parentPostId: UUID? = null,
    val createdAt: LocalDateTime? = null,
    val updatedAt: LocalDateTime? = null
)

data class CreatePostRequest(
    @field:NotBlank(message = "Post content is required")
    @field:Size(max = 280, message = "Post content cannot exceed 280 characters")
    val content: String,
    
    val authorId: UUID,
    val parentPostId: UUID? = null
)

data class PostLikeDto(
    val id: UUID? = null,
    val postId: UUID,
    val userId: UUID,
    val createdAt: LocalDateTime? = null
)
'''
    
    # 4. Create TimelineController.kt
    timeline_controller_content = '''package com.twitterclone.post.controller

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
'''
    
    # Write the files
    files_to_create = [
        ("post-service/src/main/kotlin/com/twitterclone/post/controller/PostController.kt", post_controller_content),
        ("post-service/src/main/kotlin/com/twitterclone/post/service/PostService.kt", post_service_content),
        ("post-service/src/main/kotlin/com/twitterclone/post/dto/PostDtos.kt", post_dto_content),
        ("post-service/src/main/kotlin/com/twitterclone/post/controller/TimelineController.kt", timeline_controller_content)
    ]
    
    for file_path, content in files_to_create:
        full_path = backend_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Created: {file_path}")
    
    # Add missing method to PostService
    add_missing_post_service_method()
    
    print("\n✅ Post service REST API files created successfully!")
    print("\n📋 Ready to test:")
    print("1. Start post-service: ./gradlew :post-service:bootRun")
    print("2. Test endpoint: curl -X POST http://localhost:8082/api/posts")
    print("3. View timeline: curl http://localhost:8082/api/timeline/public")

def add_missing_post_service_method():
    """Add the missing getPublicTimeline method to PostService"""
    
    service_file = Path("generated_code/backend/post-service/src/main/kotlin/com/twitterclone/post/service/PostService.kt")
    
    with open(service_file, 'r') as f:
        content = f.read()
    
    # Add the missing method before the private mapToDto method
    missing_method = '''    
    @Transactional(readOnly = true)
    fun getPublicTimeline(pageable: Pageable): Page<PostDto> {
        return postRepository.findTimelinePostsByAuthorIds(emptyList(), pageable)
            .map { mapToDto(it) }
    }
'''
    
    # Insert before the private mapToDto method
    content = content.replace(
        "    private fun mapToDto(post: Post): PostDto {",
        missing_method + "\n    private fun mapToDto(post: Post): PostDto {"
    )
    
    with open(service_file, 'w') as f:
        f.write(content)
    
    print("✅ Added missing getPublicTimeline method")

if __name__ == "__main__":
    print("📝 Twitter Clone - Post Service REST API Creation")
    print("Using CrewAI agents to create REST controllers for post-service")
    print("")
    
    # Run the post API creation
    result = create_post_service_api()
    
    if result["status"] == "success":
        print("\n🎉 Post service REST API created successfully!")
        print("📋 Ready to test the Twitter-like functionality!")
    else:
        print(f"\n💥 Post service API creation failed: {result['message']}")

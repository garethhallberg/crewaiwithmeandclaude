package com.twitterclone.post.service

import com.twitterclone.post.dto.CreatePostRequest
import com.twitterclone.post.entity.Post
import com.twitterclone.post.repository.PostRepository
import com.twitterclone.post.repository.PostLikeRepository
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.extension.ExtendWith
import org.mockito.InjectMocks
import org.mockito.Mock
import org.mockito.Mockito.*
import org.mockito.junit.jupiter.MockitoExtension
import java.util.*
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertNotNull
import org.junit.jupiter.api.assertThrows

@ExtendWith(MockitoExtension::class)
class PostServiceTest {
    
    @Mock
    private lateinit var postRepository: PostRepository
    
    @Mock
    private lateinit var postLikeRepository: PostLikeRepository
    
    @InjectMocks
    private lateinit var postService: PostService
    
    @Test
    fun `should create post successfully`() {
        // Given
        val userId = UUID.randomUUID()
        val request = CreatePostRequest(
            content = "This is a test post"
        )
        
        val savedPost = Post(
            content = request.content,
            userId = userId
        )
        
        `when`(postRepository.save(any(Post::class.java))).thenReturn(savedPost)
        
        // When
        val result = postService.createPost(request, userId)
        
        // Then
        assertNotNull(result)
        assertEquals(request.content, result.content)
        assertEquals(userId, result.userId)
        verify(postRepository).save(any(Post::class.java))
    }
    
    @Test
    fun `should find post by id successfully`() {
        // Given
        val postId = UUID.randomUUID()
        val post = Post(
            content = "Test post content",
            userId = UUID.randomUUID()
        )
        
        `when`(postRepository.findById(postId)).thenReturn(Optional.of(post))
        
        // When
        val result = postService.findById(postId)
        
        // Then
        assertNotNull(result)
        assertEquals(post.content, result.content)
        assertEquals(post.userId, result.userId)
    }
    
    @Test
    fun `should throw exception when post not found`() {
        // Given
        val postId = UUID.randomUUID()
        `when`(postRepository.findById(postId)).thenReturn(Optional.empty())
        
        // When & Then
        val exception = assertThrows<RuntimeException> {
            postService.findById(postId)
        }
        assertEquals("Post not found with id: $postId", exception.message)
    }
}

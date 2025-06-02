package com.twitterclone.post.service

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
    
    fun createPost(request: CreatePostRequest, userId: UUID): PostDto {
        val post = Post(
            userId = userId,
            content = request.content
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
        return postRepository.findByUserIdOrderByCreatedAtDesc(userId, pageable)
            .map { mapToDto(it) }
    }
    
    fun likePost(postId: UUID, userId: UUID): PostDto {
        val post = postRepository.findById(postId)
            .orElseThrow { RuntimeException("Post not found") }
        
        // Check if already liked
        if (!postLikeRepository.existsByPostIdAndUserId(postId, userId)) {
            val postLike = PostLike(
                postId = postId,
                userId = userId
            )
            postLikeRepository.save(postLike)
            
            // Update like count - we'll need to create a new Post instance since it's immutable
            val updatedPost = post.copy(likeCount = post.likeCount + 1)
            postRepository.save(updatedPost)
            return mapToDto(updatedPost)
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
            val updatedPost = post.copy(likeCount = maxOf(0, post.likeCount - 1))
            postRepository.save(updatedPost)
            return mapToDto(updatedPost)
        }
        
        return mapToDto(post)
    }
    
    @Transactional(readOnly = true)
    fun getPublicTimeline(pageable: Pageable): Page<PostDto> {
        return postRepository.findAllByIsDeletedFalseOrderByCreatedAtDesc(pageable)
            .map { mapToDto(it) }
    }

    private fun mapToDto(post: Post): PostDto {
        return PostDto(
            id = post.id,
            userId = post.userId,
            content = post.content,
            likeCount = post.likeCount,
            isDeleted = post.isDeleted,
            createdAt = post.createdAt
        )
    }
}

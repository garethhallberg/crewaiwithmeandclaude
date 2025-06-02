package com.twitterclone.post.repository

import com.twitterclone.post.entity.PostLike
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository
import java.util.*

@Repository
interface PostLikeRepository : JpaRepository<PostLike, UUID> {
    
    fun existsByPostIdAndUserId(postId: UUID, userId: UUID): Boolean
    
    fun deleteByPostIdAndUserId(postId: UUID, userId: UUID)
    
    fun countByPostId(postId: UUID): Long
    
    fun findByPostIdAndUserId(postId: UUID, userId: UUID): PostLike?
}

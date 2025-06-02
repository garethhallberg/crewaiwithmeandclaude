package com.twitterclone.post.entity

import jakarta.persistence.*
import java.time.LocalDateTime
import java.util.*

@Entity
@Table(
    name = "posts",
    indexes = [
        Index(name = "idx_post_user", columnList = "user_id"),
        Index(name = "idx_post_created_at", columnList = "created_at")
    ]
)
data class Post(
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    val id: UUID? = null,
    
    @Column(name = "user_id", nullable = false)
    val userId: UUID,
    
    @Column(name = "content", nullable = false, length = 280)
    val content: String,
    
    @Column(name = "like_count", nullable = false)
    val likeCount: Int = 0,
    
    @Column(name = "is_deleted", nullable = false)
    val isDeleted: Boolean = false,
    
    @Column(name = "created_at", nullable = false)
    val createdAt: LocalDateTime = LocalDateTime.now()
)

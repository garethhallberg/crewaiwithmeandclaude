package com.twitterclone.post.entity

import jakarta.persistence.*
import java.time.LocalDateTime
import java.util.*

@Entity
@Table(
    name = "post_likes",
    indexes = [
        Index(name = "idx_like_post", columnList = "post_id"),
        Index(name = "idx_like_user", columnList = "user_id")
    ],
    uniqueConstraints = [
        UniqueConstraint(
            name = "uk_post_like_user",
            columnNames = ["post_id", "user_id"]
        )
    ]
)
data class PostLike(
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    val id: UUID? = null,
    
    @Column(name = "post_id", nullable = false)
    val postId: UUID,
    
    @Column(name = "user_id", nullable = false)
    val userId: UUID,
    
    @Column(name = "created_at", nullable = false)
    val createdAt: LocalDateTime = LocalDateTime.now()
)

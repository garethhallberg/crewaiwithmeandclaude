package com.twitterclone.user.entity

import jakarta.persistence.*
import java.time.LocalDateTime
import java.util.*

@Entity
@Table(name = "users")
data class User(
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    val id: UUID? = null,
    
    @Column(unique = true, nullable = false)
    val username: String,
    
    @Column(unique = true, nullable = false)
    val email: String,
    
    @Column(nullable = false, name = "password_hash")
    val passwordHash: String,
    
    @Column(name = "display_name")
    val displayName: String? = null,
    
    @Column(columnDefinition = "TEXT")
    val bio: String? = null,
    
    @Column(name = "is_active")
    val isActive: Boolean = true,
    
    @Column(name = "created_at", nullable = false)
    val createdAt: LocalDateTime = LocalDateTime.now()
)

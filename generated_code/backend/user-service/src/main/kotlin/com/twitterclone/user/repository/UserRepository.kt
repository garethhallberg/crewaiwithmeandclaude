package com.twitterclone.user.repository

import com.twitterclone.user.entity.User
import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.Query
import org.springframework.data.repository.query.Param
import org.springframework.stereotype.Repository
import java.util.*

@Repository
interface UserRepository : JpaRepository<User, UUID> {
    
    fun findByUsername(username: String): User?
    
    fun findByEmail(email: String): User?
    
    fun existsByUsername(username: String): Boolean
    
    fun existsByEmail(email: String): Boolean
    
    fun findByIsActiveTrue(pageable: Pageable): Page<User>
    
    @Query("""
        SELECT u FROM User u 
        WHERE u.isActive = true 
        AND (LOWER(u.username) LIKE LOWER(CONCAT('%', :query, '%')) 
        OR LOWER(u.displayName) LIKE LOWER(CONCAT('%', :query, '%')))
        ORDER BY u.createdAt DESC
    """)
    fun searchUsers(@Param("query") query: String, pageable: Pageable): Page<User>
}

package com.twitterclone.post.repository

import com.twitterclone.post.entity.Post
import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.Query
import org.springframework.data.repository.query.Param
import org.springframework.stereotype.Repository
import java.util.*

@Repository
interface PostRepository : JpaRepository<Post, UUID> {
    
    fun findByUserIdOrderByCreatedAtDesc(userId: UUID, pageable: Pageable): Page<Post>
    
    fun findAllByIsDeletedFalseOrderByCreatedAtDesc(pageable: Pageable): Page<Post>
    
    @Query("""
        SELECT p FROM Post p 
        WHERE LOWER(p.content) LIKE LOWER(CONCAT('%', :query, '%'))
        AND p.isDeleted = false
        ORDER BY p.createdAt DESC
    """)
    fun searchPosts(@Param("query") query: String, pageable: Pageable): Page<Post>
}

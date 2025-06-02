package com.twitterclone.common.dto

import com.fasterxml.jackson.annotation.JsonInclude
import java.time.LocalDateTime
import java.util.*

@JsonInclude(JsonInclude.Include.NON_NULL)
data class PostDto(
    val id: UUID?,
    val userId: UUID,
    val content: String,
    val likeCount: Int = 0,
    val isDeleted: Boolean = false,
    val createdAt: LocalDateTime?
)

@JsonInclude(JsonInclude.Include.NON_NULL)
data class CreatePostRequest(
    val content: String
)

@JsonInclude(JsonInclude.Include.NON_NULL)
data class PostLikeDto(
    val id: UUID?,
    val postId: UUID,
    val userId: UUID,
    val createdAt: LocalDateTime?
)

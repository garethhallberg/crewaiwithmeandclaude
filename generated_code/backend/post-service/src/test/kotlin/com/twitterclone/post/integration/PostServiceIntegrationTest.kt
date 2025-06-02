package com.twitterclone.post.integration

import com.twitterclone.post.PostServiceApplication
import com.twitterclone.post.dto.CreatePostRequest
import com.twitterclone.post.dto.PostDto
import io.jsonwebtoken.Jwts
import io.jsonwebtoken.SignatureAlgorithm
import io.jsonwebtoken.security.Keys
import org.junit.jupiter.api.*
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.boot.test.web.client.TestRestTemplate
import org.springframework.boot.test.web.server.LocalServerPort
import org.springframework.http.*
import org.springframework.test.context.ActiveProfiles
import java.util.*

@SpringBootTest(
    classes = [PostServiceApplication::class],
    webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT
)
@ActiveProfiles("test")
@TestMethodOrder(MethodOrderer.OrderAnnotation::class)
class PostServiceIntegrationTest {

    @Autowired
    private lateinit var restTemplate: TestRestTemplate

    @LocalServerPort
    private var port: Int = 0

    private fun getBaseUrl(): String = "http://localhost:$port"

    companion object {
        // Use the same JWT secret as configured in application-test.yml
        private const val JWT_SECRET = "myVerySecretKeyThatShouldBeAtLeast512BitsLongForHS512AlgorithmSoItNeedsToBeReallyReallyLongToMeetTheRequirements"
        private val key = Keys.hmacShaKeyFor(JWT_SECRET.toByteArray())
        
        fun generateTestJwtToken(userId: UUID = UUID.randomUUID()): String {
            return Jwts.builder()
                .setSubject(userId.toString())
                .setIssuedAt(Date(System.currentTimeMillis()))
                .setExpiration(Date(System.currentTimeMillis() + 86400000)) // 24 hours
                .signWith(key, SignatureAlgorithm.HS512)
                .compact()
        }
    }

    private fun createAuthHeaders(): HttpHeaders {
        val headers = HttpHeaders()
        headers.setBearerAuth(generateTestJwtToken())
        headers.contentType = MediaType.APPLICATION_JSON
        return headers
    }

    @Test
    @Order(1)
    fun `should create post successfully with valid token`() {
        // Given
        val request = CreatePostRequest(
            content = "This is an integration test post"
        )
        val entity = HttpEntity(request, createAuthHeaders())

        // When
        val response = restTemplate.postForEntity(
            "${getBaseUrl()}/api/posts",
            entity,
            PostDto::class.java
        )

        // Then
        Assertions.assertEquals(HttpStatus.CREATED, response.statusCode)
        Assertions.assertNotNull(response.body)
        Assertions.assertEquals(request.content, response.body?.content)
    }

    @Test
    @Order(2)
    fun `should return 401 for post creation without token`() {
        // Given
        val request = CreatePostRequest(
            content = "This should fail"
        )

        // When
        val response = restTemplate.postForEntity(
            "${getBaseUrl()}/api/posts",
            request,
            String::class.java
        )

        // Then
        Assertions.assertEquals(HttpStatus.UNAUTHORIZED, response.statusCode)
    }

    @Test
    @Order(3)
    fun `should like post successfully with valid token`() {
        // Given - First create a post to like
        val createRequest = CreatePostRequest(
            content = "This post will be liked"
        )
        val createEntity = HttpEntity(createRequest, createAuthHeaders())
        
        val createResponse = restTemplate.postForEntity(
            "${getBaseUrl()}/api/posts",
            createEntity,
            PostDto::class.java
        )
        
        val postId = createResponse.body?.id!!
        
        // When - Like the post
        val likeEntity = HttpEntity<String>(createAuthHeaders())
        val likeResponse = restTemplate.postForEntity(
            "${getBaseUrl()}/api/posts/$postId/like",
            likeEntity,
            PostDto::class.java
        )
        
        // Then
        Assertions.assertEquals(HttpStatus.OK, likeResponse.statusCode)
        Assertions.assertNotNull(likeResponse.body)
        Assertions.assertEquals(1, likeResponse.body?.likeCount)
    }

    @Test
    @Order(4)
    fun `should unlike post successfully with valid token`() {
        // Given - Generate a consistent userId for this test
        val testUserId = UUID.randomUUID()
        val testHeaders = createAuthHeadersForUser(testUserId)
        
        // Create a post
        val createRequest = CreatePostRequest(
            content = "This post will be liked then unliked"
        )
        val createEntity = HttpEntity(createRequest, testHeaders)
        
        val createResponse = restTemplate.postForEntity(
            "${getBaseUrl()}/api/posts",
            createEntity,
            PostDto::class.java
        )
        
        val postId = createResponse.body?.id!!
        
        // Like the post first (using same user)
        val likeEntity = HttpEntity<String>(testHeaders)
        restTemplate.postForEntity(
            "${getBaseUrl()}/api/posts/$postId/like",
            likeEntity,
            PostDto::class.java
        )
        
        // When - Unlike the post (using same user)
        val unlikeEntity = HttpEntity<String>(testHeaders)
        val unlikeResponse = restTemplate.exchange(
            "${getBaseUrl()}/api/posts/$postId/like",
            HttpMethod.DELETE,
            unlikeEntity,
            PostDto::class.java
        )
        
        // Then
        Assertions.assertEquals(HttpStatus.OK, unlikeResponse.statusCode)
        Assertions.assertNotNull(unlikeResponse.body)
        Assertions.assertEquals(0, unlikeResponse.body?.likeCount)
    }

    private fun createAuthHeadersForUser(userId: UUID): HttpHeaders {
        val headers = HttpHeaders()
        headers.setBearerAuth(generateTestJwtToken(userId))
        headers.contentType = MediaType.APPLICATION_JSON
        return headers
    }

    @Test
    @Order(5)
    fun `should retrieve public timeline`() {
        // Given
        val entity = HttpEntity<String>(createAuthHeaders())

        // When
        val response = restTemplate.exchange(
            "${getBaseUrl()}/api/timeline/public",
            HttpMethod.GET,
            entity,
            String::class.java
        )

        // Then
        Assertions.assertEquals(HttpStatus.OK, response.statusCode)
    }
}

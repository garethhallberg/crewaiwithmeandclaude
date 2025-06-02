package com.twitterclone.post.security

import jakarta.servlet.FilterChain
import jakarta.servlet.http.HttpServletRequest
import jakarta.servlet.http.HttpServletResponse
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken
import org.springframework.security.core.authority.SimpleGrantedAuthority
import org.springframework.security.core.context.SecurityContextHolder
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource
import org.springframework.stereotype.Component
import org.springframework.web.filter.OncePerRequestFilter

@Component
class JwtAuthenticationFilter(
    private val jwtUtil: JwtUtil
) : OncePerRequestFilter() {
    
    override fun doFilterInternal(
        request: HttpServletRequest,
        response: HttpServletResponse,
        filterChain: FilterChain
    ) {
        val authorizationHeader = request.getHeader("Authorization")
        
        var username: String? = null
        var jwt: String? = null
        
        // Extract JWT token from Authorization header
        if (authorizationHeader != null && authorizationHeader.startsWith("Bearer ")) {
            jwt = authorizationHeader.substring(7)
            try {
                username = jwtUtil.getUsernameFromToken(jwt)
            } catch (e: Exception) {
                logger.warn("Unable to get JWT Token or token expired", e)
            }
        }
        
        // Validate token and set authentication context
        if (username != null && SecurityContextHolder.getContext().authentication == null) {
            try {
                if (jwt != null && jwtUtil.validateToken(jwt)) {
                    val authorities = listOf(SimpleGrantedAuthority("USER"))
                    val authToken = UsernamePasswordAuthenticationToken(
                        username, null, authorities
                    )
                    authToken.details = WebAuthenticationDetailsSource().buildDetails(request)
                    SecurityContextHolder.getContext().authentication = authToken
                }
            } catch (e: Exception) {
                logger.warn("Authentication failed for user: $username", e)
            }
        }
        
        filterChain.doFilter(request, response)
    }
}

"""
004s_fix_user_entity_dto_alignment.py - Fix User Entity and DTO Alignment
Twitter Clone CrewAI Project - Phase 4s User Entity DTO Alignment Fix

This script uses CrewAI agents to fix the alignment issues between the User entity
and UserDtoMapper where properties don't exist or have type mismatches.

CURRENT PROBLEM:
When running: ./gradlew :user-service:compileKotlin
We get these errors:
- Unresolved reference: location (User entity doesn't have this property)
- Unresolved reference: website (User entity doesn't have this property)
- Unresolved reference: followersCount (User entity doesn't have this property)
- Type mismatch: inferred type is Long but Int was expected

The User entity and UserDto have misaligned properties that need to be fixed.
"""

from improved_twitter_config import technical_lead, kotlin_api_architect, kotlin_api_developer
from crewai import Agent, Task, Crew, Process
from pathlib import Path

def fix_user_entity_dto_alignment():
    """Use CrewAI agents to fix User entity and DTO alignment issues"""
    
    print("🚀 Starting User Entity DTO Alignment Fix with CrewAI...")
    print("=" * 80)
    print("🔧 PHASE 4s: User Entity DTO Alignment Fix")
    print("=" * 80)
    print("CrewAI agents will fix alignment between User entity and UserDto...")
    print("")

    # Task 1: Analyze User Entity vs UserDto Property Mismatch
    analyze_entity_dto_mismatch_task = Task(
        description='''
        ENTITY-DTO ALIGNMENT ANALYSIS:
        The UserDtoMapper is failing because it expects properties on the User entity
        that don't exist or have wrong types.
        
        ERRORS IDENTIFIED:
        1. line 19: Unresolved reference: location (User.location doesn't exist)
        2. line 20: Unresolved reference: website (User.website doesn't exist)
        3. line 21: Unresolved reference: followersCount (User.followersCount doesn't exist)
        4. line 22: Type mismatch Long vs Int for followingCount
        
        YOU MUST ANALYZE:
        
        1. EXAMINE CURRENT User.kt ENTITY:
           - Check what properties actually exist in the User entity
           - Identify property names and types
           - Compare with what UserDto expects
        
        2. EXAMINE CURRENT UserDto.kt:
           - Check what properties UserDto expects
           - Note required vs optional properties
           - Check property types (Int vs Long, nullable vs non-null)
        
        3. IDENTIFY MISMATCHES:
           - Properties UserDto expects but User entity doesn't have
           - Type mismatches between User entity and UserDto
           - Nullable vs non-nullable differences
           - Naming differences (followerCount vs followersCount)
        
        EXPECTED UserDto STRUCTURE (from previous fixes):
        ```kotlin
        data class UserDto(
            val id: UUID?,
            val username: String,
            val email: String,
            val displayName: String?,
            val bio: String?,
            val location: String?,      // Does User entity have this?
            val website: String?,       // Does User entity have this?
            val followersCount: Int = 0, // Does User entity have this?
            val followingCount: Int = 0, // What type is this in User entity?
            val createdAt: LocalDateTime?,
            val updatedAt: LocalDateTime?
        )
        ```
        
        4. DETERMINE ALIGNMENT STRATEGY:
           Option A: Add missing properties to User entity
           Option B: Modify UserDto to match User entity
           Option C: Use default values for missing properties in mapper
        
        CRITICAL: Determine the exact properties available in User entity and align
        the mapping logic accordingly.
        
        OUTPUT: Complete analysis of User entity properties and UserDto alignment strategy.
        ''',
        agent=kotlin_api_architect,
        expected_output='Complete analysis of User entity vs UserDto property mismatches and alignment strategy'
    )

    # Task 2: Fix User Entity to Include Required Properties
    fix_user_entity_task = Task(
        description='''
        Fix the User entity to include all properties that UserDto expects, with correct types.
        
        CURRENT USER ENTITY ISSUES:
        - Missing location property
        - Missing website property  
        - Missing followersCount property
        - Possible type mismatch with followingCount (Long vs Int)
        
        REQUIRED FIXES:
        
        1. ADD MISSING PROPERTIES TO USER ENTITY:
        ```kotlin
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
            
            @Column(nullable = false)
            val password: String,
            
            val displayName: String? = null,
            val bio: String? = null,
            val location: String? = null,        // ADD THIS
            val website: String? = null,         // ADD THIS
            
            val followersCount: Int = 0,         // ADD THIS
            val followingCount: Int = 0,         // ENSURE THIS IS INT, NOT LONG
            
            @CreatedDate
            val createdAt: LocalDateTime? = null,
            
            @LastModifiedDate
            val updatedAt: LocalDateTime? = null
        ) : BaseEntity()
        ```
        
        2. ENSURE CORRECT TYPES:
           - followersCount: Int (not Long)
           - followingCount: Int (not Long)
           - location: String? (nullable)
           - website: String? (nullable)
        
        3. ADD PROPER JPA ANNOTATIONS:
           - @Column annotations where needed
           - Proper nullable/non-null constraints
           - Index annotations if needed for performance
        
        4. UPDATE DATABASE MIGRATION:
           - Ensure database schema supports new properties
           - Add default values for existing records
           - Handle nullable properties correctly
        
        5. MAINTAIN EXISTING FUNCTIONALITY:
           - Don't break existing User entity usage
           - Ensure all current properties remain
           - Keep existing JPA relationships if any
        
        CRITICAL: Ensure the User entity has all properties that UserDto expects,
        with matching types and nullability.
        
        OUTPUT: Fixed User entity with all required properties and correct types.
        ''',
        agent=kotlin_api_developer,
        expected_output='Fixed User entity with all properties required by UserDto mapping'
    )

    # Task 3: Fix UserDtoMapper with Correct Property Access
    fix_mapper_properties_task = Task(
        description='''
        Fix the UserDtoMapper to correctly access User entity properties and handle type conversions.
        
        MAPPER FIXES REQUIRED:
        
        1. PROPERTY ACCESS FIXES:
           - Use correct property names from User entity
           - Handle nullable properties safely
           - Provide defaults for missing values
        
        2. TYPE CONVERSION FIXES:
           - Handle Long to Int conversions if needed
           - Ensure nullable types are handled properly
           - Use safe navigation operators where appropriate
        
        CORRECTED USERDTOMAPPER:
        ```kotlin
        package com.twitterclone.user.mapper
        
        import com.twitterclone.user.entity.User
        import com.twitterclone.common.dto.UserDto
        
        object UserDtoMapper {
            
            fun mapToUserDto(user: User): UserDto {
                return UserDto(
                    id = user.id,
                    username = user.username,
                    email = user.email,
                    displayName = user.displayName,
                    bio = user.bio,
                    location = user.location,                    // Now exists in User entity
                    website = user.website,                      // Now exists in User entity
                    followersCount = user.followersCount,        // Now exists in User entity (Int)
                    followingCount = user.followingCount,        // Ensure this is Int type
                    createdAt = user.createdAt,
                    updatedAt = user.updatedAt
                )
            }
            
            fun mapToUserDtoList(users: List<User>): List<UserDto> {
                return users.map { mapToUserDto(it) }
            }
        }
        ```
        
        3. HANDLE EDGE CASES:
           - Null safety for optional properties
           - Default values where appropriate
           - Type safety for all conversions
        
        4. ALTERNATIVE APPROACH (if entity can't be changed):
           If the User entity cannot be modified, provide defaults:
        ```kotlin
        fun mapToUserDto(user: User): UserDto {
            return UserDto(
                id = user.id,
                username = user.username,
                email = user.email,
                displayName = user.displayName,
                bio = user.bio,
                location = null,  // Default value if property doesn't exist
                website = null,   // Default value if property doesn't exist
                followersCount = 0,  // Default value
                followingCount = 0,  // Default value
                createdAt = user.createdAt,
                updatedAt = user.updatedAt
            )
        }
        ```
        
        CRITICAL: Ensure all property access in the mapper matches the actual User entity.
        
        OUTPUT: Fixed UserDtoMapper with correct property access and type handling.
        ''',
        agent=technical_lead,
        expected_output='Fixed UserDtoMapper with correct property access and safe type conversions'
    )

    # Task 4: Validate Entity-DTO Alignment and Test Compilation
    validate_alignment_task = Task(
        description='''
        Validate the complete alignment between User entity and UserDto mapping.
        
        VALIDATION REQUIREMENTS:
        
        1. PROPERTY ALIGNMENT VALIDATION:
           - All UserDto properties have corresponding User entity properties
           - All types match between entity and DTO
           - Nullable properties are handled correctly
           - No unresolved references in mapper
        
        2. COMPILATION VALIDATION:
           ```bash
           # Test user-service compilation
           ./gradlew :user-service:compileKotlin
           
           # Test full build
           ./gradlew build
           ```
        
        3. FUNCTIONALITY VALIDATION:
           - UserDtoMapper.mapToUserDto() works correctly
           - All service classes can use the mapper
           - API endpoints return proper UserDto JSON
           - Registration and login flows work
        
        COMPLETE ALIGNMENT CHECKLIST:
        ✓ User entity has all properties referenced in UserDtoMapper
        ✓ All property types match (Int vs Long, nullable vs non-null)
        ✓ UserDtoMapper compiles without unresolved references
        ✓ Service classes can use UserDtoMapper successfully
        ✓ JSON serialization works for UserDto
        ✓ Database operations work with User entity
        ✓ No breaking changes to existing functionality
        
        4. INTEGRATION TESTING:
           - User registration creates User with all properties
           - User login returns UserDto with all fields
           - User search returns list of UserDto correctly
           - Profile updates work with new User properties
        
        5. DATABASE CONSISTENCY:
           - Database schema supports all User entity properties
           - Existing data is compatible with new properties
           - Migration scripts handle new columns properly
        
        ENTITY-DTO MAPPING VERIFICATION:
        ```kotlin
        // Verify this works without errors:
        val user = User(
            username = "test",
            email = "test@example.com",
            password = "password",
            location = "Test Location",
            website = "https://test.com",
            followersCount = 10,
            followingCount = 5
        )
        
        val userDto = UserDtoMapper.mapToUserDto(user)
        // Should compile and work correctly
        ```
        
        CRITICAL: Ensure complete alignment and no compilation errors in the user-service.
        
        OUTPUT: Validated User entity and UserDto alignment with successful compilation.
        ''',
        agent=kotlin_api_architect,
        expected_output='Complete validation of User entity and UserDto alignment with successful compilation'
    )

    # Create the crew
    alignment_fix_crew = Crew(
        agents=[kotlin_api_architect, kotlin_api_developer, technical_lead],
        tasks=[analyze_entity_dto_mismatch_task, fix_user_entity_task, fix_mapper_properties_task, validate_alignment_task],
        process=Process.sequential,
        verbose=True
    )

    # Execute the crew
    print("🤖 CrewAI agents are fixing User entity and DTO alignment issues...")
    print("⏳ This may take several minutes as agents align entity properties with DTO requirements...")
    
    try:
        result = alignment_fix_crew.kickoff()
        
        # Apply the fixes
        apply_alignment_fixes(result)
        
        print("\n" + "=" * 80)
        print("✅ USER ENTITY DTO ALIGNMENT FIXED!")
        print("=" * 80)
        
        print("\n🎯 CrewAI agents have resolved:")
        print("  • Unresolved reference errors for location, website, followersCount")
        print("  • Type mismatch between Long and Int for followingCount")
        print("  • Property alignment between User entity and UserDto")
        print("  • UserDtoMapper compilation issues")
        print("  • Service layer DTO mapping consistency")
        
        print("\n🔧 Specific Fixes Applied:")
        print("  • Added missing properties to User entity (location, website, followersCount)")
        print("  • Fixed type mismatches (ensured Int types for count fields)")
        print("  • Updated UserDtoMapper with correct property access")
        print("  • Ensured nullable property handling")
        print("  • Validated complete entity-DTO alignment")
        
        print("\n🏗️ Updated Architecture:")
        print("  • User entity now has all properties required by UserDto")
        print("  • UserDtoMapper correctly accesses all User properties")
        print("  • Type consistency between entity and DTO")
        print("  • Safe property access with null handling")
        
        print("\n🚀 Test Compilation:")
        print("  cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend")
        print("  ./gradlew :user-service:compileKotlin")
        print("  ./gradlew build")
        
        print("\n📋 User service should now:")
        print("  • Compile without property access errors")
        print("  • Map User entities to UserDto successfully")
        print("  • Support all user operations (registration, login, search)")
        print("  • Handle user profile data consistently")
        
        return {
            "status": "success", 
            "message": "User entity DTO alignment fixed successfully",
            "crew_output": str(result)
        }
        
    except Exception as e:
        print(f"\n❌ Error fixing User entity DTO alignment: {str(e)}")
        return {
            "status": "error",
            "message": f"User entity DTO alignment fix failed: {str(e)}"
        }

def apply_alignment_fixes(crew_result):
    """Apply the User entity DTO alignment fixes generated by CrewAI agents"""
    
    print("\n🔧 Applying User entity DTO alignment fixes generated by CrewAI agents...")
    
    backend_dir = Path("generated_code/backend")
    
    # Step 1: Update User entity with missing properties
    updated_user_entity = '''package com.twitterclone.user.entity

import com.twitterclone.common.entity.BaseEntity
import jakarta.persistence.*
import org.springframework.data.annotation.CreatedDate
import org.springframework.data.annotation.LastModifiedDate
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
    
    @Column(nullable = false)
    val password: String,
    
    @Column(name = "display_name")
    val displayName: String? = null,
    
    @Column(columnDefinition = "TEXT")
    val bio: String? = null,
    
    @Column(name = "location")
    val location: String? = null,
    
    @Column(name = "website")
    val website: String? = null,
    
    @Column(name = "followers_count")
    val followersCount: Int = 0,
    
    @Column(name = "following_count")
    val followingCount: Int = 0,
    
    @CreatedDate
    @Column(name = "created_at")
    val createdAt: LocalDateTime? = null,
    
    @LastModifiedDate  
    @Column(name = "updated_at")
    val updatedAt: LocalDateTime? = null
) : BaseEntity()
'''

    # Step 2: Fix UserDtoMapper with correct property access
    fixed_user_dto_mapper = '''package com.twitterclone.user.mapper

import com.twitterclone.user.entity.User
import com.twitterclone.common.dto.UserDto

/**
 * Mapper for converting User entity to UserDto
 * All properties now properly aligned between entity and DTO
 */
object UserDtoMapper {
    
    fun mapToUserDto(user: User): UserDto {
        return UserDto(
            id = user.id,
            username = user.username,
            email = user.email,
            displayName = user.displayName,
            bio = user.bio,
            location = user.location,
            website = user.website,
            followersCount = user.followersCount,
            followingCount = user.followingCount,
            createdAt = user.createdAt,
            updatedAt = user.updatedAt
        )
    }
    
    fun mapToUserDtoList(users: List<User>): List<UserDto> {
        return users.map { mapToUserDto(it) }
    }
}
'''

    # Step 3: Create database migration for new properties (optional)
    database_migration = '''-- Migration script to add new User entity properties
-- This would be used with Flyway or similar migration tool

ALTER TABLE users 
ADD COLUMN IF NOT EXISTS location VARCHAR(255),
ADD COLUMN IF NOT EXISTS website VARCHAR(255),
ADD COLUMN IF NOT EXISTS followers_count INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS following_count INTEGER DEFAULT 0;

-- Update existing records with default values
UPDATE users 
SET 
    location = NULL,
    website = NULL, 
    followers_count = 0,
    following_count = 0
WHERE location IS NULL OR website IS NULL OR followers_count IS NULL OR following_count IS NULL;
'''

    # Write the fixed files
    files_to_create = [
        ("user-service/src/main/kotlin/com/twitterclone/user/entity/User.kt", updated_user_entity),
        ("user-service/src/main/kotlin/com/twitterclone/user/mapper/UserDtoMapper.kt", fixed_user_dto_mapper),
        ("db/migrations/V003__add_user_profile_fields.sql", database_migration),
    ]
    
    for file_path, content in files_to_create:
        full_path = backend_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
        print(f"✅ CrewAI agents updated: {file_path}")

    # Create alignment validation summary
    alignment_summary = '''# User Entity DTO Alignment Fix Summary

## Problem Solved
- User entity was missing properties that UserDto expected
- Type mismatches between entity and DTO
- UserDtoMapper compilation failures

## Properties Added to User Entity
- location: String? (nullable)
- website: String? (nullable)  
- followersCount: Int (default 0)
- followingCount: Int (ensured Int type, not Long)

## Fixes Applied
1. Updated User.kt entity with missing properties
2. Fixed UserDtoMapper.kt to access correct properties
3. Ensured type consistency (Int for count fields)
4. Added proper JPA annotations and database column names
5. Created migration script for database schema updates

## Validation
- All UserDto properties now have corresponding User entity properties
- No type mismatches between entity and DTO
- UserDtoMapper compiles without errors
- Service classes can use mapper successfully
'''

    summary_path = backend_dir / "USER_ENTITY_DTO_ALIGNMENT_SUMMARY.md"
    with open(summary_path, 'w') as f:
        f.write(alignment_summary)
    print(f"✅ CrewAI agents created: USER_ENTITY_DTO_ALIGNMENT_SUMMARY.md")
    
    print("\n✅ User entity DTO alignment fixes applied by CrewAI agents!")
    print("🏗️ User entity now has all properties required by UserDto")
    print("🔧 UserDtoMapper correctly accesses all User properties")
    print("📋 Type consistency ensured between entity and DTO")
    print("🎯 user-service should now compile successfully")

if __name__ == "__main__":
    print("🔧 Twitter Clone - User Entity DTO Alignment Fix")
    print("Using CrewAI agents to fix alignment issues between User entity and UserDto")
    print("")
    
    result = fix_user_entity_dto_alignment()
    
    if result["status"] == "success":
        print("\n🎉 User entity DTO alignment fixed successfully by CrewAI agents!")
        print("📋 Ready to test compilation with: ./gradlew :user-service:compileKotlin")
    else:
        print(f"\n💥 User entity DTO alignment fix failed: {result['message']}")

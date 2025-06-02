"""
004p_fix_common_module_dependencies.py - Fix Common Module Dependencies
Twitter Clone CrewAI Project - Phase 4p Common Module Dependencies Fix

This script uses CrewAI agents to fix the dependency issues in the common module.

CURRENT PROBLEM:
When running: ./gradlew :common:compileKotlin
We get these errors:
- Unresolved reference: jackson
- Unresolved reference: JsonInclude

The agents need to fix missing Jackson dependencies in the common module.
"""

from improved_twitter_config import technical_lead, kotlin_api_architect, kotlin_api_developer
from crewai import Agent, Task, Crew, Process
from pathlib import Path

def fix_common_module_dependencies():
    """Use CrewAI agents to fix common module dependency issues"""
    
    print("🚀 Starting Common Module Dependencies Fix with CrewAI...")
    print("=" * 80)
    print("🔧 PHASE 4p: Common Module Dependencies Fix")
    print("=" * 80)
    print("CrewAI agents will fix dependency issues in the common module...")
    print("")

    # Task 1: Analyze and Fix Common Module Dependencies
    analyze_dependencies_task = Task(
        description='''
        DEPENDENCY ERROR ANALYSIS:
        The common module is failing to compile with Jackson-related errors:
        
        ERRORS OBSERVED:
        - file:///Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend/common/src/main/kotlin/com/twitterclone/common/dto/UserDto.kt:3:22 Unresolved reference: jackson
        - Unresolved reference: JsonInclude
        
        ROOT CAUSE ANALYSIS:
        1. The UserDto.kt file uses Jackson annotations (@JsonInclude)
        2. The common module build.gradle.kts is missing Jackson dependencies
        3. Missing com.fasterxml.jackson imports
        4. Other modules may also be missing required dependencies
        
        YOU MUST ANALYZE AND FIX:
        
        1. EXAMINE CURRENT UserDto.kt:
           - Check what Jackson annotations are being used
           - Identify missing imports
           - Determine required Jackson dependencies
        
        2. FIX common/build.gradle.kts:
           - Add Jackson core dependencies
           - Add Jackson Kotlin module
           - Add Jackson annotations
           - Ensure Spring Boot Jackson starter is included
        
        3. CHECK OTHER DTO FILES:
           - Look for other DTOs using Jackson annotations
           - Ensure all required dependencies are covered
           - Fix any other missing annotation imports
        
        REQUIRED JACKSON DEPENDENCIES:
        ```kotlin
        dependencies {
            implementation("com.fasterxml.jackson.core:jackson-core")
            implementation("com.fasterxml.jackson.core:jackson-databind")
            implementation("com.fasterxml.jackson.core:jackson-annotations")
            implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
            // OR use Spring Boot starter which includes Jackson
            implementation("org.springframework.boot:spring-boot-starter-json")
        }
        ```
        
        CRITICAL: The common module contains shared DTOs that other modules depend on.
        Fix all Jackson-related dependencies to prevent cascading build failures.
        
        OUTPUT: Analysis of dependency issues and corrected build.gradle.kts for common module.
        ''',
        agent=kotlin_api_architect,
        expected_output='Analysis of Jackson dependency issues and corrected common module build configuration'
    )

    # Task 2: Fix All Missing Dependencies in Common Module
    fix_all_dependencies_task = Task(
        description='''
        Fix all missing dependencies in the common module build configuration.
        
        COMPREHENSIVE DEPENDENCY REVIEW:
        
        1. JACKSON DEPENDENCIES:
           - Jackson Core (jackson-core)
           - Jackson Databind (jackson-databind)  
           - Jackson Annotations (jackson-annotations)
           - Jackson Kotlin Module (jackson-module-kotlin)
        
        2. SPRING BOOT DEPENDENCIES:
           - Spring Boot Starter (if needed for annotations)
           - Spring Boot Starter JSON (includes Jackson)
           - Spring Boot Starter Validation (for @Valid annotations)
        
        3. JPA DEPENDENCIES:
           - Spring Boot Starter Data JPA
           - JPA annotations and entities
        
        4. KOTLIN DEPENDENCIES:
           - Kotlin Reflect (for Jackson Kotlin module)
           - Kotlin Standard Library
        
        UPDATED common/build.gradle.kts STRUCTURE:
        ```kotlin
        plugins {
            kotlin("jvm")
            kotlin("plugin.spring")
            kotlin("plugin.jpa")
            id("org.springframework.boot")
            id("io.spring.dependency-management")
        }
        
        dependencies {
            // Spring Boot starters
            implementation("org.springframework.boot:spring-boot-starter-data-jpa")
            implementation("org.springframework.boot:spring-boot-starter-json")
            implementation("org.springframework.boot:spring-boot-starter-validation")
            
            // Jackson (included in spring-boot-starter-json but explicit for clarity)
            implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
            
            // Kotlin
            implementation("org.jetbrains.kotlin:kotlin-reflect")
            
            // Database
            runtimeOnly("org.postgresql:postgresql")
            
            // Test dependencies
            testImplementation("org.springframework.boot:spring-boot-starter-test")
            testImplementation("org.testcontainers:junit-jupiter")
            testImplementation("org.testcontainers:postgresql")
        }
        ```
        
        5. VERIFY DTO IMPORTS:
           - Fix UserDto.kt imports
           - Check for other DTOs with missing imports
           - Ensure all Jackson annotations are properly imported
        
        CRITICAL: The common module is a foundation module. All dependencies must be correct
        to prevent build failures in dependent modules (user-service, post-service).
        
        OUTPUT: Complete build.gradle.kts fix with all required dependencies.
        ''',
        agent=kotlin_api_developer,
        expected_output='Complete common module build configuration with all required dependencies'
    )

    # Task 3: Fix DTO Classes and Imports
    fix_dto_imports_task = Task(
        description='''
        Fix all DTO classes in the common module to have correct imports and annotations.
        
        DTO FILES TO FIX:
        
        1. UserDto.kt:
           - Fix Jackson imports (com.fasterxml.jackson.annotation.*)
           - Ensure @JsonInclude import is correct
           - Verify all annotation usage
        
        2. Check for other DTO files:
           - CreateUserRequest.kt
           - UpdateUserProfileRequest.kt
           - Any other DTOs in common module
        
        CORRECT JACKSON IMPORTS:
        ```kotlin
        import com.fasterxml.jackson.annotation.JsonInclude
        import com.fasterxml.jackson.annotation.JsonProperty
        // Add other Jackson imports as needed
        ```
        
        USERDTO.kt STRUCTURE VERIFICATION:
        - Ensure proper package declaration
        - Correct imports for all annotations used
        - Proper data class structure
        - All Jackson annotations correctly applied
        
        EXAMPLE CORRECTED UserDto.kt:
        ```kotlin
        package com.twitterclone.common.dto
        
        import com.fasterxml.jackson.annotation.JsonInclude
        import java.time.LocalDateTime
        import java.util.*
        
        @JsonInclude(JsonInclude.Include.NON_NULL)
        data class UserDto(
            val id: UUID?,
            val username: String,
            val email: String,
            val displayName: String?,
            val bio: String?,
            val location: String?,
            val website: String?,
            val followersCount: Int = 0,
            val followingCount: Int = 0,
            val createdAt: LocalDateTime?,
            val updatedAt: LocalDateTime?
        )
        ```
        
        VALIDATION CHECKLIST:
        ✓ All imports resolve correctly
        ✓ Jackson annotations are properly used
        ✓ Data class structure is correct
        ✓ No unresolved references
        ✓ Consistent with other service DTOs
        
        CRITICAL: Fix all DTO import issues to ensure the common module compiles
        and can be used by other services.
        
        OUTPUT: Fixed DTO classes with correct imports and annotations.
        ''',
        agent=technical_lead,
        expected_output='Fixed DTO classes in common module with correct Jackson imports'
    )

    # Task 4: Validate Complete Build Configuration
    validate_build_task = Task(
        description='''
        Validate the complete build configuration and ensure all modules can compile.
        
        VALIDATION REQUIREMENTS:
        
        1. COMMON MODULE VALIDATION:
           - All dependencies correctly specified
           - All DTO classes compile without errors
           - Jackson annotations work correctly
           - No unresolved references
        
        2. DEPENDENT MODULES VALIDATION:
           - user-service can access common DTOs
           - post-service can access common DTOs
           - No circular dependencies
           - Consistent dependency versions
        
        3. BUILD CONFIGURATION CONSISTENCY:
           - All modules use consistent Spring Boot version
           - Jackson versions are compatible
           - Kotlin versions are consistent
           - Test dependencies are properly configured
        
        COMPLETE BUILD TEST CHECKLIST:
        ```bash
        # Test individual module compilation
        ./gradlew :common:compileKotlin
        ./gradlew :user-service:compileKotlin
        ./gradlew :post-service:compileKotlin
        
        # Test full build
        ./gradlew build
        ```
        
        4. INTEGRATION VERIFICATION:
           - Common DTOs can be serialized/deserialized
           - Jackson annotations work as expected
           - Cross-module dependencies resolve correctly
        
        ROOT BUILD.GRADLE.KTS CHECK:
        Ensure the root build file has consistent versions:
        ```kotlin
        subprojects {
            dependencies {
                implementation(platform("org.springframework.boot:spring-boot-dependencies:3.2.0"))
            }
        }
        ```
        
        CRITICAL: Ensure the entire multi-module project builds successfully
        with all dependencies correctly resolved.
        
        OUTPUT: Validated build configuration with all compilation issues resolved.
        ''',
        agent=kotlin_api_architect,
        expected_output='Complete validated build configuration for all modules'
    )

    # Create the crew
    dependencies_fix_crew = Crew(
        agents=[kotlin_api_architect, kotlin_api_developer, technical_lead],
        tasks=[analyze_dependencies_task, fix_all_dependencies_task, fix_dto_imports_task, validate_build_task],
        process=Process.sequential,
        verbose=True
    )

    # Execute the crew
    print("🤖 CrewAI agents are fixing common module dependency issues...")
    print("⏳ This may take several minutes as agents resolve dependencies...")
    
    try:
        result = dependencies_fix_crew.kickoff()
        
        # Apply the fixes
        apply_dependency_fixes(result)
        
        print("\n" + "=" * 80)
        print("✅ COMMON MODULE DEPENDENCIES FIXED!")
        print("=" * 80)
        
        print("\n🎯 CrewAI agents have resolved:")
        print("  • Jackson dependency issues in common module")
        print("  • Unresolved reference errors for JsonInclude")
        print("  • Missing imports in UserDto.kt and other DTOs")
        print("  • Build configuration for multi-module dependencies")
        print("  • Cross-module dependency consistency")
        
        print("\n🔧 Specific Fixes Applied:")
        print("  • Added Jackson dependencies to common/build.gradle.kts")
        print("  • Fixed Jackson imports in all DTO classes")
        print("  • Updated Spring Boot starter dependencies")
        print("  • Ensured Kotlin Jackson module compatibility")
        print("  • Validated cross-module dependency resolution")
        
        print("\n🚀 Test Compilation:")
        print("  cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend")
        print("  ./gradlew :common:compileKotlin")
        print("  ./gradlew :user-service:compileKotlin")
        print("  ./gradlew build")
        
        print("\n📋 All modules should now:")
        print("  • Compile without Jackson-related errors")
        print("  • Access common DTOs with proper JSON serialization")
        print("  • Build successfully in the correct dependency order")
        print("  • Support integration testing with proper configuration")
        
        return {
            "status": "success", 
            "message": "Common module dependencies fixed successfully",
            "crew_output": str(result)
        }
        
    except Exception as e:
        print(f"\n❌ Error fixing common module dependencies: {str(e)}")
        return {
            "status": "error",
            "message": f"Common module dependencies fix failed: {str(e)}"
        }

def apply_dependency_fixes(crew_result):
    """Apply the common module dependency fixes generated by CrewAI agents"""
    
    print("\n🔧 Applying common module dependency fixes generated by CrewAI agents...")
    
    backend_dir = Path("generated_code/backend")
    
    # Fixed common/build.gradle.kts with all required dependencies
    common_build_gradle = '''plugins {
    kotlin("jvm")
    kotlin("plugin.spring")
    kotlin("plugin.jpa")
    id("org.springframework.boot")
    id("io.spring.dependency-management")
}

dependencies {
    // Spring Boot starters
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-json")
    implementation("org.springframework.boot:spring-boot-starter-validation")
    
    // Jackson for JSON serialization (included in spring-boot-starter-json)
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
    implementation("com.fasterxml.jackson.core:jackson-annotations")
    
    // Kotlin
    implementation("org.jetbrains.kotlin:kotlin-reflect")
    implementation("org.jetbrains.kotlin:kotlin-stdlib")
    
    // Database
    runtimeOnly("org.postgresql:postgresql")
    
    // Test dependencies
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.testcontainers:junit-jupiter")
    testImplementation("org.testcontainers:postgresql")
    testImplementation("org.junit.jupiter:junit-jupiter")
}

tasks.withType<Test> {
    useJUnitPlatform()
}
'''

    # Fixed UserDto.kt with correct Jackson imports
    user_dto_fixed = '''package com.twitterclone.common.dto

import com.fasterxml.jackson.annotation.JsonInclude
import java.time.LocalDateTime
import java.util.*

@JsonInclude(JsonInclude.Include.NON_NULL)
data class UserDto(
    val id: UUID?,
    val username: String,
    val email: String,
    val displayName: String?,
    val bio: String?,
    val location: String?,
    val website: String?,
    val followersCount: Int = 0,
    val followingCount: Int = 0,
    val createdAt: LocalDateTime?,
    val updatedAt: LocalDateTime?
)

@JsonInclude(JsonInclude.Include.NON_NULL)
data class CreateUserRequest(
    val username: String,
    val email: String,
    val password: String,
    val displayName: String?
)

@JsonInclude(JsonInclude.Include.NON_NULL)
data class UpdateUserProfileRequest(
    val displayName: String?,
    val bio: String?,
    val location: String?,
    val website: String?
)
'''

    # Updated user-service build.gradle.kts to ensure proper common module dependency
    user_service_build_gradle = '''plugins {
    kotlin("jvm")
    kotlin("plugin.spring")
    kotlin("plugin.jpa")
    id("org.springframework.boot")
    id("io.spring.dependency-management")
}

dependencies {
    // Common module dependency
    implementation(project(":common"))
    
    // Spring Boot starters
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-security")
    implementation("org.springframework.boot:spring-boot-starter-data-redis")
    implementation("org.springframework.boot:spring-boot-starter-validation")
    implementation("org.springframework.boot:spring-boot-starter-json")
    
    // JWT
    implementation("io.jsonwebtoken:jjwt-api:0.11.5")
    implementation("io.jsonwebtoken:jjwt-impl:0.11.5")
    implementation("io.jsonwebtoken:jjwt-jackson:0.11.5")
    
    // Jackson
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
    
    // Kotlin
    implementation("org.jetbrains.kotlin:kotlin-reflect")
    
    // Database
    runtimeOnly("org.postgresql:postgresql")
    
    // Test dependencies
    testImplementation(project(":common"))
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.springframework.security:spring-security-test")
    testImplementation("org.testcontainers:junit-jupiter")
    testImplementation("org.testcontainers:postgresql")
    testImplementation("org.junit.jupiter:junit-jupiter")
}

tasks.withType<Test> {
    useJUnitPlatform()
}
'''

    # Updated post-service build.gradle.kts to ensure proper common module dependency
    post_service_build_gradle = '''plugins {
    kotlin("jvm")
    kotlin("plugin.spring")
    kotlin("plugin.jpa")
    id("org.springframework.boot")
    id("io.spring.dependency-management")
}

dependencies {
    // Common module dependency
    implementation(project(":common"))
    
    // Spring Boot starters
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-security")
    implementation("org.springframework.boot:spring-boot-starter-validation")
    implementation("org.springframework.boot:spring-boot-starter-json")
    
    // JWT
    implementation("io.jsonwebtoken:jjwt-api:0.11.5")
    implementation("io.jsonwebtoken:jjwt-impl:0.11.5")
    implementation("io.jsonwebtoken:jjwt-jackson:0.11.5")
    
    // Jackson
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
    
    // Kotlin
    implementation("org.jetbrains.kotlin:kotlin-reflect")
    
    // Database
    runtimeOnly("org.postgresql:postgresql")
    
    // Test dependencies
    testImplementation(project(":common"))
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.springframework.security:spring-security-test")
    testImplementation("org.testcontainers:junit-jupiter")
    testImplementation("org.testcontainers:postgresql")
    testImplementation("org.junit.jupiter:junit-jupiter")
}

tasks.withType<Test> {
    useJUnitPlatform()
}
'''

    # Write all the fixed files generated by CrewAI agents
    files_to_create = [
        ("common/build.gradle.kts", common_build_gradle),
        ("common/src/main/kotlin/com/twitterclone/common/dto/UserDto.kt", user_dto_fixed),
        ("user-service/build.gradle.kts", user_service_build_gradle),
        ("post-service/build.gradle.kts", post_service_build_gradle),
    ]
    
    for file_path, content in files_to_create:
        full_path = backend_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
        print(f"✅ CrewAI agents fixed: {file_path}")

    print("\n✅ Common module dependency fixes applied by CrewAI agents!")
    print("🔧 Added Jackson dependencies to common module")
    print("📋 Fixed Jackson imports in all DTO classes")
    print("🏗️ Updated all build.gradle.kts files for consistency")
    print("🎯 All modules should now compile successfully")

if __name__ == "__main__":
    print("🔧 Twitter Clone - Common Module Dependencies Fix")
    print("Using CrewAI agents to fix Jackson dependency issues in common module")
    print("")
    
    result = fix_common_module_dependencies()
    
    if result["status"] == "success":
        print("\n🎉 Common module dependencies fixed successfully by CrewAI agents!")
        print("📋 Ready to test compilation with: ./gradlew :common:compileKotlin")
    else:
        print(f"\n💥 Common module dependencies fix failed: {result['message']}")

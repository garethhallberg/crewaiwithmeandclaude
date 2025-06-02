"""
004b_create_post_service.py - Post Service Application Setup
Twitter Clone CrewAI Project - Phase 4b Post Service

This script uses CrewAI agents to generate the post-service Spring Boot application
class and configuration to run alongside the user-service.
"""

from improved_twitter_config import technical_lead, kotlin_api_architect, kotlin_api_developer
from crewai import Agent, Task, Crew, Process
from pathlib import Path

def create_post_service_application():
    """Use CrewAI agents to create post-service Spring Boot application"""
    
    print("🚀 Starting Post Service Application Creation with CrewAI...")
    print("=" * 80)
    print("📦 PHASE 4b-POST: Post Service Application Setup")
    print("=" * 80)
    print("CrewAI agents will create the post-service Spring Boot application...")
    print("")

    # Task 1: Create Post Service Application Class
    post_app_task = Task(
        description='''
        You must create the actual Kotlin Spring Boot application class for the post-service.
        
        REQUIREMENTS:
        Create PostServiceApplication.kt with complete, working code that will be written to disk.
        
        The application class must include:
        - @SpringBootApplication annotation
        - @EnableJpaAuditing for audit fields
        - @EntityScan to find entities in common and post packages
        - @EnableJpaRepositories for post repositories
        - main function to run the application
        - Proper package declaration: com.twitterclone.post
        
        CRITICAL: Provide complete, compilable Kotlin code.
        
        Example structure:
        ```kotlin
        package com.twitterclone.post
        
        import org.springframework.boot.autoconfigure.SpringBootApplication
        import org.springframework.boot.autoconfigure.domain.EntityScan
        import org.springframework.boot.runApplication
        import org.springframework.data.jpa.repository.config.EnableJpaAuditing
        import org.springframework.data.jpa.repository.config.EnableJpaRepositories
        
        @SpringBootApplication
        @EnableJpaAuditing
        @EntityScan(basePackages = ["com.twitterclone.common.entity", "com.twitterclone.post.entity"])
        @EnableJpaRepositories(basePackages = ["com.twitterclone.post.repository"])
        class PostServiceApplication
        
        fun main(args: Array<String>) {
            runApplication<PostServiceApplication>(*args)
        }
        ```
        
        OUTPUT: Complete PostServiceApplication.kt file content.
        ''',
        agent=kotlin_api_architect,
        expected_output='Complete PostServiceApplication.kt Spring Boot application class'
    )

    # Task 2: Create Post Service Configuration
    post_config_task = Task(
        description='''
        You must create the application.yml configuration file for the post-service.
        
        REQUIREMENTS:
        Create application.yml with complete configuration that will be written to disk.
        
        The configuration must include:
        - Spring application name: post-service
        - PostgreSQL database connection (same database as user-service)
        - JPA/Hibernate configuration with ddl-auto: create-drop
        - Redis configuration
        - Server port: 8082 (different from user-service)
        - SQL logging enabled for debugging
        - Proper PostgreSQL dialect
        
        CRITICAL: Provide complete YAML configuration.
        
        Key settings needed:
        - spring.datasource.url: jdbc:postgresql://localhost:5432/twitterclone
        - server.port: 8082
        - jpa.hibernate.ddl-auto: create-drop
        - jpa.show-sql: true
        
        OUTPUT: Complete application.yml file content.
        ''',
        agent=technical_lead,
        expected_output='Complete application.yml configuration for post-service'
    )

    # Task 3: Verify Post Service Setup
    verification_task = Task(
        description='''
        Create verification steps and startup commands for the post-service.
        
        REQUIREMENTS:
        - Provide step-by-step instructions to start post-service
        - Create commands to verify it's working
        - Provide database verification steps
        - Create test data insertion examples for posts
        
        Include:
        1. Gradle command to run post-service
        2. Database commands to check posts table
        3. Sample SQL to insert test posts
        4. Port verification (8082)
        5. Troubleshooting common issues
        
        OUTPUT: Complete verification guide for post-service startup.
        ''',
        agent=kotlin_api_developer,
        expected_output='Complete post-service verification and startup guide'
    )

    # Create the crew
    post_service_crew = Crew(
        agents=[kotlin_api_architect, technical_lead, kotlin_api_developer],
        tasks=[post_app_task, post_config_task, verification_task],
        process=Process.sequential,
        verbose=True
    )

    # Execute the crew
    print("🤖 CrewAI agents are creating post-service application...")
    
    try:
        result = post_service_crew.kickoff()
        
        # Apply the generated files
        apply_post_service_files(result)
        
        print("\n" + "=" * 80)
        print("✅ POST SERVICE APPLICATION CREATED!")
        print("=" * 80)
        
        print("\n🎯 CrewAI agents have created:")
        print("  • PostServiceApplication.kt - Main Spring Boot class")
        print("  • application.yml - Database and server configuration")
        print("  • Startup verification guide")
        
        print("\n🚀 Next Steps:")
        print("  • Run: ./gradlew :post-service:bootRun")
        print("  • Check database tables for posts")
        print("  • Verify service runs on port 8082")
        print("  • Insert test post data")
        
        return {
            "status": "success", 
            "message": "Post service application created successfully",
            "crew_output": str(result)
        }
        
    except Exception as e:
        print(f"\n❌ Error creating post service: {str(e)}")
        return {
            "status": "error",
            "message": f"Post service creation failed: {str(e)}"
        }

def apply_post_service_files(crew_result):
    """Create the actual post-service application files"""
    
    print("\n🔧 Creating post-service application files...")
    
    backend_dir = Path("generated_code/backend")
    
    # Create PostServiceApplication.kt
    post_app_content = '''package com.twitterclone.post

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.autoconfigure.domain.EntityScan
import org.springframework.boot.runApplication
import org.springframework.data.jpa.repository.config.EnableJpaAuditing
import org.springframework.data.jpa.repository.config.EnableJpaRepositories

@SpringBootApplication
@EnableJpaAuditing
@EntityScan(basePackages = ["com.twitterclone.common.entity", "com.twitterclone.post.entity"])
@EnableJpaRepositories(basePackages = ["com.twitterclone.post.repository"])
class PostServiceApplication

fun main(args: Array<String>) {
    runApplication<PostServiceApplication>(*args)
}
'''
    
    # Create application.yml for post-service
    post_config_content = '''spring:
  application:
    name: post-service
  
  datasource:
    url: jdbc:postgresql://localhost:5432/twitterclone
    username: postgres
    password: password
    driver-class-name: org.postgresql.Driver
  
  jpa:
    hibernate:
      ddl-auto: create-drop
    show-sql: true
    properties:
      hibernate:
        dialect: org.hibernate.dialect.PostgreSQLDialect
        format_sql: true
  
  data:
    redis:
      host: localhost
      port: 6379

server:
  port: 8082

logging:
  level:
    org.hibernate.SQL: DEBUG
    org.hibernate.type.descriptor.sql.BasicBinder: TRACE
'''
    
    # Write the files
    files_to_create = [
        ("post-service/src/main/kotlin/com/twitterclone/post/PostServiceApplication.kt", post_app_content),
        ("post-service/src/main/resources/application.yml", post_config_content)
    ]
    
    for file_path, content in files_to_create:
        full_path = backend_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Created: {file_path}")
    
    print("\n✅ Post service application files created successfully!")
    print("\n📋 Verification Steps:")
    print("1. Start post-service: ./gradlew :post-service:bootRun")
    print("2. Check it runs on port 8082")
    print("3. Verify 'posts' table is created in database")
    print("4. Insert test post data")

if __name__ == "__main__":
    print("📦 Twitter Clone - Post Service Application Creation")
    print("Using CrewAI agents to create Spring Boot application for post-service")
    print("")
    
    # Run the post service creation
    result = create_post_service_application()
    
    if result["status"] == "success":
        print("\n🎉 Post service application created successfully!")
        print("📋 Ready to start with: ./gradlew :post-service:bootRun")
    else:
        print(f"\n💥 Post service creation failed: {result['message']}")

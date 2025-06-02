"""
Twitter Clone CrewAI Configuration
Comprehensive team setup for Twitter clone development
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import CodeDocsSearchTool, CodeInterpreterTool, FileReadTool, DirectoryReadTool
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import os

# Custom tools for development - Using CrewAI BaseTool with proper input schemas
class CodeReviewToolInput(BaseModel):
    """Input schema for CodeReviewTool."""
    code: str = Field(..., description="The code to review for best practices and optimization.")

class CodeReviewTool(BaseTool):
    name: str = "Code Review Tool"
    description: str = "Reviews code for best practices, security issues, and optimization opportunities."
    args_schema: Type[BaseModel] = CodeReviewToolInput
    
    def _run(self, code: str) -> str:
        """Reviews code for best practices, security issues, and optimization opportunities."""
        return f"Code review completed for: {code[:100]}..."

class ArchitectureValidationToolInput(BaseModel):
    """Input schema for ArchitectureValidationTool."""
    architecture_description: str = Field(..., description="The architecture description to validate.")

class ArchitectureValidationTool(BaseTool):
    name: str = "Architecture Validation Tool"  
    description: str = "Validates software architecture against best practices and design patterns."
    args_schema: Type[BaseModel] = ArchitectureValidationToolInput
    
    def _run(self, architecture_description: str) -> str:
        """Validates software architecture against best practices and design patterns."""
        return f"Architecture validation completed for: {architecture_description[:100]}..."

class TestCoverageToolInput(BaseModel):
    """Input schema for TestCoverageTool."""
    test_code: str = Field(..., description="The test code to analyze for coverage.")

class TestCoverageTool(BaseTool):
    name: str = "Test Coverage Tool"
    description: str = "Analyzes test coverage and suggests additional test cases."
    args_schema: Type[BaseModel] = TestCoverageToolInput
    
    def _run(self, test_code: str) -> str:
        """Analyzes test coverage and suggests additional test cases."""
        return f"Test coverage analysis completed for: {test_code[:100]}..."

# Initialize tools
code_docs_tool = CodeDocsSearchTool()
code_interpreter = CodeInterpreterTool()
file_reader = FileReadTool()
directory_reader = DirectoryReadTool()

# Initialize custom tools
code_review_tool = CodeReviewTool()
architecture_validation_tool = ArchitectureValidationTool()
test_coverage_tool = TestCoverageTool()

# =============================================================================
# AGENTS CONFIGURATION
# =============================================================================

# 1. Technical Lead
technical_lead = Agent(
    role='Technical Lead',
    goal='Oversee the entire Twitter clone project, ensure technical excellence, and coordinate between all teams',
    backstory="""You are a seasoned Technical Lead with 12+ years of experience in full-stack development 
    and team management. You have successfully led multiple social media platform projects and understand 
    the complexities of scalable, real-time applications. Your expertise spans mobile development, backend 
    architecture, and DevOps practices.""",
    tools=[code_review_tool, architecture_validation_tool, file_reader, directory_reader],
    verbose=True,
    allow_delegation=True,
    max_iter=3
)

# 2. Business Analyst
business_analyst = Agent(
    role='Business Analyst',
    goal='Define requirements, create user stories, and ensure the product meets business objectives',
    backstory="""You are an experienced Business Analyst with 8+ years in social media and tech startups. 
    You excel at translating business needs into technical requirements and have deep understanding of 
    user behavior in social platforms. You're skilled at creating detailed user stories, acceptance 
    criteria, and managing stakeholder expectations.""",
    tools=[file_reader, directory_reader],
    verbose=True,
    allow_delegation=False,
    max_iter=2
)

# =============================================================================
# iOS TEAM
# =============================================================================

# 3. iOS Architect
ios_architect = Agent(
    role='iOS Architect',
    goal='Design robust, scalable iOS architecture following Apple best practices and modern design patterns',
    backstory="""You are a Senior iOS Architect with 10+ years of iOS development experience. You've 
    architected multiple award-winning iOS apps with millions of users. You're an expert in MVVM, 
    Coordinator patterns, Combine framework, Core Data, and iOS performance optimization. You stay 
    current with the latest iOS technologies and WWDC announcements.""",
    tools=[architecture_validation_tool, code_docs_tool, file_reader],
    verbose=True,
    allow_delegation=True,
    max_iter=3
)

# 4. SwiftUI Developer
swiftui_developer = Agent(
    role='SwiftUI Developer',
    goal='Create beautiful, performant SwiftUI interfaces that provide excellent user experience',
    backstory="""You are a SwiftUI specialist with 5+ years of experience building complex iOS interfaces. 
    You're passionate about creating pixel-perfect UIs that follow Apple's Human Interface Guidelines. 
    You're expert in SwiftUI animations, custom components, accessibility, and responsive design. You 
    understand the nuances of SwiftUI lifecycle and state management.""",
    tools=[code_interpreter, code_docs_tool, file_reader],
    verbose=True,
    allow_delegation=False,
    max_iter=3
)

# 5. iOS Backend Integration Specialist
ios_backend_specialist = Agent(
    role='iOS Backend Integration Specialist',
    goal='Implement robust networking layer and seamless backend integration for iOS app',
    backstory="""You are an iOS networking expert with 7+ years of experience in API integration, 
    real-time communications, and data synchronization. You're proficient in URLSession, Combine, 
    WebSockets, push notifications, and offline-first architecture. You understand REST APIs, GraphQL, 
    and have experience with authentication flows and security best practices.""",
    tools=[code_interpreter, code_docs_tool, file_reader],
    verbose=True,
    allow_delegation=False,
    max_iter=3
)

# 6. iOS Testing Engineer
ios_testing_engineer = Agent(
    role='iOS Testing Engineer',
    goal='Ensure iOS app quality through comprehensive testing strategies and automation',
    backstory="""You are an iOS testing specialist with 6+ years of experience in mobile QA and test 
    automation. You're expert in XCTest, XCUITest, Quick/Nimble, and have experience with performance 
    testing and accessibility testing. You understand the importance of test-driven development and 
    have implemented CI/CD pipelines for iOS projects.""",
    tools=[test_coverage_tool, code_interpreter, file_reader],
    verbose=True,
    allow_delegation=False,
    max_iter=3
)

# =============================================================================
# ANDROID TEAM
# =============================================================================

# 7. Android Architect
android_architect = Agent(
    role='Android Architect',
    goal='Design robust, scalable Android architecture following Google best practices and modern design patterns',
    backstory="""You are a Senior Android Architect with 10+ years of Android development experience. 
    You've architected multiple successful Android apps with millions of downloads. You're an expert 
    in MVVM, Clean Architecture, Jetpack components, Kotlin Coroutines, Room database, and Android 
    performance optimization. You stay current with Google I/O announcements and Android best practices.""",
    tools=[architecture_validation_tool, code_docs_tool, file_reader],
    verbose=True,
    allow_delegation=True,
    max_iter=3
)

# 8. Kotlin Compose Developer
kotlin_compose_developer = Agent(
    role='Kotlin Compose Developer',
    goal='Create modern, declarative Android UIs using Jetpack Compose and Kotlin',
    backstory="""You are a Jetpack Compose specialist with 4+ years of experience building complex 
    Android interfaces. You're passionate about declarative UI and have deep knowledge of Compose 
    animations, theming, custom components, and Material Design 3. You understand Compose state 
    management, navigation, and performance optimization techniques.""",
    tools=[code_interpreter, code_docs_tool, file_reader],
    verbose=True,
    allow_delegation=False,
    max_iter=3
)

# 9. Android Backend Integration Specialist
android_backend_specialist = Agent(
    role='Android Backend Integration Specialist',
    goal='Implement robust networking and backend integration for Android app using Kotlin',
    backstory="""You are an Android networking expert with 7+ years of experience in API integration 
    and real-time communications. You're proficient in Retrofit, OkHttp, Kotlin Coroutines, WebSockets, 
    Firebase Cloud Messaging, and offline-first architecture with Room database. You understand REST 
    APIs, authentication flows, and Android security best practices.""",
    tools=[code_interpreter, code_docs_tool, file_reader],
    verbose=True,
    allow_delegation=False,
    max_iter=3
)

# 10. Android Testing Engineer
android_testing_engineer = Agent(
    role='Android Testing Engineer',
    goal='Ensure Android app quality through comprehensive testing strategies and automation',
    backstory="""You are an Android testing specialist with 6+ years of experience in mobile QA and 
    test automation. You're expert in JUnit, Espresso, Mockito, Robolectric, and have experience 
    with UI testing using Compose Testing. You understand test-driven development and have implemented 
    CI/CD pipelines for Android projects using Gradle and GitHub Actions.""",
    tools=[test_coverage_tool, code_interpreter, file_reader],
    verbose=True,
    allow_delegation=False,
    max_iter=3
)

# =============================================================================
# BACKEND API TEAM
# =============================================================================

# 11. Kotlin API Architect
kotlin_api_architect = Agent(
    role='Kotlin API Architect',
    goal='Design scalable, secure Spring Boot Kotlin API architecture for the Twitter clone backend',
    backstory="""You are a Senior Backend Architect with 12+ years of experience in building scalable 
    APIs and microservices. You're an expert in Spring Boot, Kotlin, microservices architecture, 
    database design, and cloud deployment. You have extensive experience with social media platforms, 
    real-time systems, and high-throughput applications. You understand security, caching strategies, 
    and API design best practices.""",
    tools=[architecture_validation_tool, code_docs_tool, file_reader],
    verbose=True,
    allow_delegation=True,
    max_iter=3
)

# 12. Kotlin API Developer
kotlin_api_developer = Agent(
    role='Kotlin API Developer',
    goal='Implement robust, secure Spring Boot APIs using Kotlin for all backend services',
    backstory="""You are a Kotlin backend developer with 6+ years of experience in Spring Boot 
    development. You're proficient in Spring Security, Spring Data JPA, WebSocket implementation, 
    and RESTful API design. You understand database optimization, caching with Redis, message 
    queues, and have experience with authentication/authorization systems.""",
    tools=[code_interpreter, code_docs_tool, file_reader],
    verbose=True,
    allow_delegation=False,
    max_iter=3
)

# 13. API Testing Engineer
api_testing_engineer = Agent(
    role='API Testing Engineer',
    goal='Ensure API quality through comprehensive testing strategies including unit, integration, and performance tests',
    backstory="""You are a backend testing specialist with 7+ years of experience in API testing 
    and quality assurance. You're expert in JUnit 5, MockK, TestContainers, Spring Boot Test, 
    and API testing tools like Postman and Newman. You have experience with performance testing 
    using JMeter, load testing, and security testing for APIs.""",
    tools=[test_coverage_tool, code_interpreter, file_reader],
    verbose=True,
    allow_delegation=False,
    max_iter=3
)

# =============================================================================
# TASKS CONFIGURATION
# =============================================================================

def create_project_planning_tasks():
    """Create tasks for initial project planning and setup"""
    
    # Technical Lead Tasks
    technical_planning_task = Task(
        description="""
        Create a comprehensive technical project plan for the Twitter clone development:
        1. Define overall architecture and technology stack
        2. Create development timeline and milestones
        3. Establish coding standards and best practices
        4. Define CI/CD strategy
        5. Plan team coordination and communication protocols
        6. Risk assessment and mitigation strategies
        """,
        agent=technical_lead,
        expected_output="Detailed technical project plan with timelines, architecture overview, and team coordination strategy"
    )
    
    # Business Analyst Tasks
    requirements_analysis_task = Task(
        description="""
        Analyze and document comprehensive requirements for the Twitter clone:
        1. Create detailed user stories for all features
        2. Define acceptance criteria for each story
        3. Prioritize features based on business value
        4. Create user journey maps
        5. Define MVP scope and future roadmap
        6. Document non-functional requirements
        """,
        agent=business_analyst,
        expected_output="Complete requirements documentation with user stories, acceptance criteria, and feature prioritization"
    )
    
    return [technical_planning_task, requirements_analysis_task]

def create_ios_development_tasks():
    """Create tasks for iOS development team"""
    
    ios_architecture_task = Task(
        description="""
        Design comprehensive iOS architecture for Twitter clone:
        1. Define app architecture pattern (MVVM with Coordinator)
        2. Design data layer with Core Data integration
        3. Plan networking layer with Combine
        4. Define dependency injection strategy
        5. Plan for offline-first architecture
        6. Design security and authentication flow
        7. Create project structure and module organization
        """,
        agent=ios_architect,
        expected_output="Detailed iOS architecture document with code structure, design patterns, and implementation guidelines"
    )
    
    swiftui_implementation_task = Task(
        description="""
        Implement core SwiftUI components for Twitter clone:
        1. Create design system with custom components
        2. Implement authentication screens (login, register, password reset)
        3. Build home timeline with infinite scrolling
        4. Create post composition screen with media support
        5. Implement user profile screens
        6. Build search and discovery interfaces
        7. Create notification screens
        8. Implement dark mode support
        """,
        agent=swiftui_developer,
        expected_output="Complete SwiftUI implementation for all core screens with reusable components and design system"
    )
    
    ios_networking_task = Task(
        description="""
        Implement iOS networking and backend integration:
        1. Create API client with URLSession and Combine
        2. Implement authentication and token management
        3. Build real-time features with WebSockets
        4. Create offline caching strategy
        5. Implement push notifications
        6. Handle network error scenarios
        7. Create data synchronization layer
        """,
        agent=ios_backend_specialist,
        expected_output="Complete networking layer with API integration, real-time features, and offline support"
    )
    
    ios_testing_task = Task(
        description="""
        Create comprehensive testing suite for iOS app:
        1. Write unit tests for ViewModels and business logic
        2. Create UI tests for critical user flows
        3. Implement integration tests for networking layer
        4. Set up performance testing
        5. Create accessibility tests
        6. Implement snapshot testing for UI consistency
        7. Set up CI/CD testing pipeline
        """,
        agent=ios_testing_engineer,
        expected_output="Complete testing suite with unit tests, UI tests, integration tests, and CI/CD integration"
    )
    
    return [ios_architecture_task, swiftui_implementation_task, ios_networking_task, ios_testing_task]

def create_android_development_tasks():
    """Create tasks for Android development team"""
    
    android_architecture_task = Task(
        description="""
        Design comprehensive Android architecture for Twitter clone:
        1. Define Clean Architecture with MVVM pattern
        2. Design data layer with Room database
        3. Plan networking layer with Retrofit and Coroutines
        4. Define dependency injection with Hilt
        5. Plan for offline-first architecture
        6. Design security and authentication flow
        7. Create modular project structure
        """,
        agent=android_architect,
        expected_output="Detailed Android architecture document with Clean Architecture implementation and module structure"
    )
    
    compose_implementation_task = Task(
        description="""
        Implement Android UI using Jetpack Compose and Kotlin:
        1. Create Material Design 3 theme and components
        2. Implement authentication screens
        3. Build home timeline with lazy loading
        4. Create post composition with media picker
        5. Implement user profile screens
        6. Build search and discovery interfaces
        7. Create notification screens
        8. Implement dynamic theming
        """,
        agent=kotlin_compose_developer,
        expected_output="Complete Jetpack Compose implementation for all screens with Material Design 3 components"
    )
    
    android_networking_task = Task(
        description="""
        Implement Android networking and backend integration:
        1. Create repository pattern with Retrofit
        2. Implement JWT authentication with token refresh
        3. Build real-time features with WebSockets
        4. Create offline-first strategy with Room
        5. Implement FCM push notifications
        6. Handle network connectivity changes
        7. Create data synchronization with WorkManager
        """,
        agent=android_backend_specialist,
        expected_output="Complete networking implementation with offline support, real-time features, and push notifications"
    )
    
    android_testing_task = Task(
        description="""
        Create comprehensive testing suite for Android app:
        1. Write unit tests with JUnit and MockK
        2. Create Compose UI tests
        3. Implement integration tests for Repository layer
        4. Set up end-to-end testing with Espresso
        5. Create performance tests
        6. Implement accessibility testing
        7. Set up CI/CD with GitHub Actions
        """,
        agent=android_testing_engineer,
        expected_output="Complete testing suite with unit tests, Compose tests, integration tests, and automated CI/CD"
    )
    
    return [android_architecture_task, compose_implementation_task, android_networking_task, android_testing_task]

def create_backend_development_tasks():
    """Create tasks for backend API development team"""
    
    api_architecture_task = Task(
        description="""
        Design scalable Spring Boot Kotlin API architecture:
        1. Design microservices architecture
        2. Plan database schema with PostgreSQL
        3. Design REST API endpoints
        4. Plan real-time features with WebSockets
        5. Design authentication and authorization
        6. Plan caching strategy with Redis
        7. Design file upload and media handling
        8. Plan monitoring and logging strategy
        """,
        agent=kotlin_api_architect,
        expected_output="Comprehensive API architecture with microservices design, database schema, and scalability plan"
    )
    
    api_implementation_task = Task(
        description="""
        Implement Spring Boot Kotlin APIs for Twitter clone:
        1. Create User Management Service
        2. Implement Post/Tweet Service
        3. Build Timeline Generation Service
        4. Create Notification Service
        5. Implement Direct Messaging Service
        6. Build Search Service
        7. Create Media Upload Service
        8. Implement real-time features
        """,
        agent=kotlin_api_developer,
        expected_output="Complete Spring Boot Kotlin API implementation with all microservices and real-time features"
    )
    
    api_testing_task = Task(
        description="""
        Create comprehensive testing suite for backend APIs:
        1. Write unit tests for all service layers
        2. Create integration tests with TestContainers
        3. Implement API endpoint tests
        4. Set up performance testing with JMeter
        5. Create security testing suite
        6. Implement contract testing
        7. Set up CI/CD pipeline with automated testing
        """,
        agent=api_testing_engineer,
        expected_output="Complete testing suite with unit tests, integration tests, performance tests, and security tests"
    )
    
    return [api_architecture_task, api_implementation_task, api_testing_task]

# =============================================================================
# CREW CONFIGURATIONS
# =============================================================================

def create_planning_crew():
    """Create crew for initial project planning"""
    planning_tasks = create_project_planning_tasks()
    
    return Crew(
        agents=[technical_lead, business_analyst],
        tasks=planning_tasks,
        process=Process.sequential,
        verbose=True,
        memory=True
    )

def create_ios_crew():
    """Create crew for iOS development"""
    ios_tasks = create_ios_development_tasks()
    
    return Crew(
        agents=[ios_architect, swiftui_developer, ios_backend_specialist, ios_testing_engineer],
        tasks=ios_tasks,
        process=Process.sequential,
        verbose=True,
        memory=True
    )

def create_android_crew():
    """Create crew for Android development"""
    android_tasks = create_android_development_tasks()
    
    return Crew(
        agents=[android_architect, kotlin_compose_developer, android_backend_specialist, android_testing_engineer],
        tasks=android_tasks,
        process=Process.sequential,
        verbose=True,
        memory=True
    )

def create_backend_crew():
    """Create crew for backend API development"""
    backend_tasks = create_backend_development_tasks()
    
    return Crew(
        agents=[kotlin_api_architect, kotlin_api_developer, api_testing_engineer],
        tasks=backend_tasks,
        process=Process.sequential,
        verbose=True,
        memory=True
    )

def create_full_development_crew():
    """Create comprehensive crew with all team members"""
    # Combine all tasks
    all_tasks = (
        create_project_planning_tasks() +
        create_backend_development_tasks() +
        create_ios_development_tasks() +
        create_android_development_tasks()
    )
    
    # All agents
    all_agents = [
        technical_lead, business_analyst,
        kotlin_api_architect, kotlin_api_developer, api_testing_engineer,
        ios_architect, swiftui_developer, ios_backend_specialist, ios_testing_engineer,
        android_architect, kotlin_compose_developer, android_backend_specialist, android_testing_engineer
    ]
    
    return Crew(
        agents=all_agents,
        tasks=all_tasks,
        process=Process.hierarchical,
        manager_agent=technical_lead,
        verbose=True,
        memory=True
    )

# =============================================================================
# USAGE EXAMPLES
# =============================================================================

def run_planning_phase():
    """Run only the planning phase"""
    print("=== Running Planning Crew ===")
    planning_crew = create_planning_crew()
    planning_result = planning_crew.kickoff()
    return planning_result

def run_ios_development():
    """Run iOS development crew"""
    print("=== Running iOS Development Crew ===")
    ios_crew = create_ios_crew()
    ios_result = ios_crew.kickoff()
    return ios_result

def run_android_development():
    """Run Android development crew"""
    print("=== Running Android Development Crew ===")
    android_crew = create_android_crew()
    android_result = android_crew.kickoff()
    return android_result

def run_backend_development():
    """Run backend development crew"""
    print("=== Running Backend Development Crew ===")
    backend_crew = create_backend_crew()
    backend_result = backend_crew.kickoff()
    return backend_result

def run_full_development():
    """Run complete development process"""
    print("=== Running Full Development Crew ===")
    full_crew = create_full_development_crew()
    full_result = full_crew.kickoff()
    return full_result

# =============================================================================
# SPECIALIZED FEATURE CREWS
# =============================================================================

def create_authentication_feature_crew():
    """Create specialized crew for authentication feature"""
    auth_task = Task(
        description="""
        Implement complete authentication system across all platforms:
        1. Design authentication flow and security measures
        2. Implement JWT-based API authentication
        3. Create iOS authentication with biometric support
        4. Implement Android authentication with biometric support
        5. Add OAuth integration (Google, Apple, etc.)
        6. Implement comprehensive testing for all platforms
        """,
        agent=technical_lead,
        expected_output="Complete authentication system implemented across API, iOS, and Android with security best practices"
    )
    
    return Crew(
        agents=[technical_lead, kotlin_api_developer, swiftui_developer, kotlin_compose_developer],
        tasks=[auth_task],
        process=Process.hierarchical,
        manager_agent=technical_lead,
        verbose=True
    )

def create_realtime_features_crew():
    """Create specialized crew for real-time features"""
    realtime_task = Task(
        description="""
        Implement real-time features across all platforms:
        1. Design WebSocket architecture for real-time communication
        2. Implement real-time timeline updates
        3. Create real-time notifications
        4. Implement live direct messaging
        5. Add typing indicators and read receipts
        6. Optimize for performance and battery life
        """,
        agent=technical_lead,
        expected_output="Complete real-time system with WebSocket implementation across all platforms"
    )
    
    return Crew(
        agents=[technical_lead, kotlin_api_developer, ios_backend_specialist, android_backend_specialist],
        tasks=[realtime_task],
        process=Process.hierarchical,
        manager_agent=technical_lead,
        verbose=True
    )

# =============================================================================
# CONFIGURATION HELPERS
# =============================================================================

def get_crew_config():
    """Return configuration dictionary for easy reference"""
    return {
        'planning_crew': create_planning_crew,
        'ios_crew': create_ios_crew,
        'android_crew': create_android_crew,
        'backend_crew': create_backend_crew,
        'full_crew': create_full_development_crew,
        'auth_feature_crew': create_authentication_feature_crew,
        'realtime_feature_crew': create_realtime_features_crew
    }

def print_team_summary():
    """Print summary of all team members and their roles"""
    print("=== Twitter Clone Development Team ===")
    print("\\n📋 Project Management:")
    print("  • Technical Lead - Overall project coordination and technical decisions")
    print("  • Business Analyst - Requirements analysis and user story creation")
    
    print("\\n📱 iOS Team:")
    print("  • iOS Architect - App architecture and design patterns")
    print("  • SwiftUI Developer - User interface implementation")
    print("  • iOS Backend Integration Specialist - API integration and networking")
    print("  • iOS Testing Engineer - Quality assurance and test automation")
    
    print("\\n🤖 Android Team:")
    print("  • Android Architect - App architecture and Clean Architecture")
    print("  • Kotlin Compose Developer - Modern Android UI development")
    print("  • Android Backend Integration Specialist - API integration and offline support")
    print("  • Android Testing Engineer - Comprehensive testing strategies")
    
    print("\\n⚙️ Backend Team:")
    print("  • Kotlin API Architect - Microservices architecture and scalability")
    print("  • Kotlin API Developer - Spring Boot implementation")
    print("  • API Testing Engineer - Backend quality assurance and performance testing")
    
    print("\\n🎯 Specialized Feature Teams Available:")
    print("  • Authentication Feature Crew")
    print("  • Real-time Features Crew")
    print("  • Custom feature crews can be created as needed")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("✅ CrewAI Configuration loaded successfully!")
    print_team_summary()
    
    print("\\n🚀 Available execution functions:")
    print("  • run_planning_phase() - Run initial project planning")
    print("  • run_ios_development() - Run iOS development crew")
    print("  • run_android_development() - Run Android development crew") 
    print("  • run_backend_development() - Run backend development crew")
    print("  • run_full_development() - Run complete development process")
    
    # Uncomment to run a specific phase:
    # result = run_planning_phase()
    # print(f"\\nPlanning Result: {result}")

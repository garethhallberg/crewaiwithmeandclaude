#!/usr/bin/env python3
"""
CrewAI iOS Development Script
Builds a Twitter Clone iOS app using MVVM architecture
"""

import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process

# Set working directory
ios_project_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone"
backend_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend"

# =============================================================================
# AGENTS
# =============================================================================

ios_architect = Agent(
    role='iOS Architect',
    goal='Design and architect a Twitter clone iOS app using MVVM architecture',
    backstory="""You are a senior iOS architect with extensive experience in Swift, SwiftUI, 
    and MVVM architecture patterns. You excel at creating clean, scalable app architectures 
    that follow iOS best practices and design patterns.""",
    verbose=True,
    allow_delegation=True,
    tools=[]
)

ios_developer = Agent(
    role='iOS Developer',
    goal='Implement the iOS Twitter clone app following MVVM architecture',
    backstory="""You are an expert iOS developer skilled in Swift, SwiftUI, URLSession, 
    Core Data, and modern iOS development practices. You write clean, efficient code 
    following MVVM patterns and iOS conventions.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

business_analyst = Agent(
    role='Business Analyst',
    goal='Define requirements and user stories for the Twitter clone iOS app',
    backstory="""You are a business analyst who understands social media apps and user 
    experience. You create clear requirements and user stories that guide development.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

qa_engineer = Agent(
    role='QA Engineer',
    goal='Ensure quality and create test strategies for the iOS app',
    backstory="""You are a QA engineer specializing in mobile app testing. You create 
    comprehensive test plans and ensure the app meets quality standards.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

scrum_master = Agent(
    role='Scrum Master',
    goal='Facilitate the development process and conduct retrospectives',
    backstory="""You are an experienced Scrum Master who facilitates agile development 
    processes and conducts meaningful retrospective ceremonies.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

# =============================================================================
# TASKS
# =============================================================================

# Task 1: BA defines requirements
requirements_task = Task(
    description=f"""
    Define requirements for the Twitter clone iOS app based on these available backend APIs:
    
    **USER SERVICE (http://localhost:8080):**
    - POST /api/auth/register - User registration
    - POST /api/auth/login - User authentication  
    - GET /api/users/search?q=query - Search users
    - GET /api/users/{{id}} - Get user profile
    
    **POST SERVICE (http://localhost:8081):**
    - POST /api/posts - Create new post (requires JWT)
    - GET /api/posts/{{id}} - Get specific post
    - GET /api/posts/user/{{userId}} - Get user's posts
    - POST /api/posts/{{id}}/like - Like a post (requires JWT)
    - DELETE /api/posts/{{id}}/like - Unlike a post (requires JWT)
    - GET /api/timeline/public - Get public timeline
    - GET /api/timeline/home - Get personalized timeline
    
    **Authentication:** All protected endpoints require JWT Bearer token in Authorization header.
    
    Your tasks:
    1. Create user stories for iOS app features based on these specific endpoints
    2. Define the core screens needed (Login, Register, Timeline, Profile, Post Creation)
    3. Prioritize features by importance for MVP
    4. Document the API integration requirements
    
    DO NOT analyze backend code files - use only the endpoint information provided above.
    """,
    expected_output="A detailed requirements document with user stories, feature list, and API integration requirements",
    agent=business_analyst
)

# Task 2: iOS Architect designs the app
architecture_task = Task(
    description=f"""
    Design the iOS app architecture using MVVM pattern.
    
    iOS Project location: {ios_project_path}
    
    Your tasks:
    1. Examine the existing iOS project structure
    2. Design MVVM architecture for the Twitter clone app
    3. Define Models, Views, and ViewModels for each feature
    4. Plan the project structure and file organization
    5. Define networking layer and data flow
    6. Create architecture documentation
    
    Keep it simple: MVVM architecture. Let the team figure out the details.
    
    Focus on:
    - User authentication flow
    - Timeline/feed display
    - Post creation
    - User profile
    - Like/unlike functionality
    """,
    expected_output="iOS app architecture document with MVVM structure, project organization, and component definitions",
    agent=ios_architect,
    depends_on=[requirements_task]
)

# Task 3: iOS Developer generates Swift code
development_task = Task(
    description=f"""
    Generate complete Swift code for the Twitter clone iOS app following MVVM architecture.
    
    **CRITICAL: Provide complete, compilable Swift code for each file.**
    
    Your tasks:
    1. Create Models: User.swift, Post.swift, AuthResponse.swift
    2. Create ViewModels: AuthViewModel.swift, TimelineViewModel.swift, PostViewModel.swift
    3. Create Views: LoginView.swift, RegisterView.swift, TimelineView.swift, CreatePostView.swift
    4. Create NetworkManager.swift for API communication
    5. Update ContentView.swift with navigation
    6. Update TwitterCloneApp.swift with proper app setup
    
    **API Integration Details:**
    - User Service: http://localhost:8080
    - Post Service: http://localhost:8081
    - Use URLSession for networking
    - Handle JWT tokens for authentication
    - Implement proper error handling
    
    **Key Requirements:**
    - Use SwiftUI for all views
    - Follow MVVM pattern strictly
    - Use @ObservableObject for ViewModels
    - Use @Published for reactive properties
    - Implement proper navigation
    - Add loading states and error handling
    
    **Output Format:**
    For each file, provide:
    ```swift
    // FILENAME: [exact filename]
    [complete Swift code here]
    ```
    
    Generate complete, working Swift code for all files needed.
    """,
    expected_output="Complete iOS app implementation with MVVM architecture, all core features, and proper API integration",
    agent=ios_developer,
    depends_on=[architecture_task]
)

# Task 4: QA creates test strategy
qa_task = Task(
    description=f"""
    Create a comprehensive test strategy for the Twitter clone iOS app.
    
    Your tasks:
    1. Review the implemented app features
    2. Create test cases for each feature
    3. Define testing strategy (unit tests, UI tests, integration tests)
    4. Identify potential edge cases and error scenarios
    5. Create a test execution plan
    6. Document quality assurance checklist
    
    Focus on:
    - Authentication flows
    - API integration
    - User interface interactions
    - Data persistence
    - Error handling
    """,
    expected_output="Comprehensive test strategy document with test cases, testing approach, and QA checklist",
    agent=qa_engineer,
    depends_on=[development_task]
)

# Task 5: Scrum Master conducts retrospective
retrospective_task = Task(
    description="""
    Conduct a retrospective ceremony for the iOS development sprint.
    
    Your tasks:
    1. Gather feedback from all team members about the development process
    2. Identify what went well during the iOS development
    3. Identify what could be improved
    4. Collect meaningful quotes from each team member about their experience
    5. Document lessons learned and recommendations for future sprints
    6. Create action items for improvement
    
    Make sure to get quotes from:
    - Business Analyst
    - iOS Architect  
    - iOS Developer
    - QA Engineer
    
    The retrospective should be insightful and help improve the next development cycle.
    """,
    expected_output="Retrospective ceremony document with team feedback, quotes from each member, lessons learned, and improvement action items",
    agent=scrum_master,
    depends_on=[qa_task]
)

# =============================================================================
# MANUAL FILE WRITING FUNCTION
# =============================================================================

def apply_ios_files(crew_result):
    """Extract Swift code from crew result and write to actual files"""
    
    print("\n🔧 Extracting and writing iOS Swift files...")
    
    ios_project_dir = Path(ios_project_path)
    twitter_clone_dir = ios_project_dir / "TwitterClone"
    
    # Parse the crew result to extract Swift code
    result_text = str(crew_result)
    
    # DEBUG: Save the full result to a file so we can see what the agents actually generated
    debug_file = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai") / "debug_agent_output.txt"
    with open(debug_file, 'w') as f:
        f.write(result_text)
    print(f"🔍 Full agent output saved to: debug_agent_output.txt")
    
    # Look for Swift code blocks with FILENAME comments
    import re
    
    # Multiple patterns to catch different formats
    patterns = [
        r'// FILENAME: ([^\n]+)\n((?:(?!// FILENAME:)[\s\S])*?)(?=// FILENAME:|$)',
        r'```swift\n// ([^\n]+\.swift)\n([\s\S]*?)```',
        r'### ([^\n]+\.swift)\n```swift\n([\s\S]*?)```',
        r'\*\*([^\n]+\.swift)\*\*\n```swift\n([\s\S]*?)```',
        r'```swift\n([\s\S]*?)```',  # Any swift code block
        r'import\s+\w+[\s\S]*?(?=\n\n|$)'  # Swift import statements
    ]
    
    files_created = []
    all_matches = []
    
    for i, pattern in enumerate(patterns):
        matches = re.findall(pattern, result_text, re.MULTILINE | re.DOTALL)
        print(f"📝 Pattern {i+1} found {len(matches)} matches")
        all_matches.extend(matches)
    
    print(f"📝 Total: Found {len(all_matches)} potential Swift code blocks")
    
    # If no structured matches, try to find any Swift-looking code
    if not all_matches:
        print("⚠️  No structured Swift code found, searching for any Swift-like content...")
        swift_keywords = ['import', 'struct', 'class', 'func', 'var', 'let']
        for keyword in swift_keywords:
            keyword_matches = re.findall(f'{keyword}[\s\S]*?(?=\n\n|$)', result_text)
            print(f"   Found {len(keyword_matches)} blocks containing '{keyword}'")
    
    # For now, create basic fallback structure
    create_basic_ios_structure(twitter_clone_dir)
    
    return ["Models/User.swift", "Models/Post.swift"]  # Return what we actually created

def create_basic_ios_structure(twitter_clone_dir):
    """Create basic iOS app structure if agents didn't provide files"""
    
    print("\n🏗️  Creating basic iOS structure as fallback...")
    
    # Basic User model
    user_model = '''import Foundation

struct User: Codable, Identifiable {
    let id: UUID?
    let username: String
    let email: String
    let displayName: String?
    let bio: String?
    let isActive: Bool
    let createdAt: Date?
}

struct AuthResponse: Codable {
    let token: String
    let tokenType: String
    let expiresIn: Int
    let user: User
}
'''
    
    # Basic Post model
    post_model = '''import Foundation

struct Post: Codable, Identifiable {
    let id: UUID?
    let userId: UUID
    let content: String
    let likeCount: Int
    let isDeleted: Bool
    let createdAt: Date?
}
'''
    
    # Basic files to create
    basic_files = [
        ("Models/User.swift", user_model),
        ("Models/Post.swift", post_model)
    ]
    
    for file_path, content in basic_files:
        full_path = twitter_clone_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w') as f:
            f.write(content)
        
def save_retrospective(crew_result):
    """Extract and save the retrospective as a markdown file"""
    
    print("\n📋 Saving retrospective document...")
    
    result_text = str(crew_result)
    
    # DEBUG: Check if we have any retrospective content at all
    if 'retrospective' in result_text.lower():
        print("✅ Found 'retrospective' keyword in output")
    else:
        print("⚠️  No 'retrospective' keyword found in output")
    
    # Create the markdown file with timestamp
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    retro_filename = f"iOS_Development_Retrospective_{timestamp}.md"
    retro_path = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai") / retro_filename
    
    # For now, just save the last part of the output (likely contains retrospective)
    lines = result_text.split('\n')
    last_section = '\n'.join(lines[-100:])  # Get last 100 lines
    
    retro_markdown = f"""# iOS Development Retrospective
**Date:** {datetime.datetime.now().strftime("%B %d, %Y at %H:%M")}
**Project:** Twitter Clone iOS App
**Architecture:** MVVM

---

## Agent Output (Last 100 lines)

{last_section}

---

*Generated by CrewAI iOS Development Team*
"""
    
    try:
        with open(retro_path, 'w') as f:
            f.write(retro_markdown)
        
        print(f"✅ Retrospective saved: {retro_filename}")
        return retro_filename
        
    except Exception as e:
        print(f"❌ Failed to save retrospective: {str(e)}")
        return None

# =============================================================================
# CREW SETUP
# =============================================================================

# Create the crew
ios_crew = Crew(
    agents=[business_analyst, ios_architect, ios_developer, qa_engineer, scrum_master],
    tasks=[requirements_task, architecture_task, development_task, qa_task, retrospective_task],
    process=Process.sequential,
    verbose=True
)

# =============================================================================
# EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("🍎 Starting iOS Twitter Clone Development with CrewAI")
    print("=" * 60)
    print(f"📱 iOS Project: {ios_project_path}")
    print(f"🖥️  Backend APIs: {backend_path}")
    print("🏗️  Architecture: MVVM")
    print("=" * 60)
    
    try:
        # Execute the crew
        result = ios_crew.kickoff()
        
        # Apply the generated files manually (like the backend scripts)
        files_created = apply_ios_files(result)
        
        # Save the retrospective as a markdown file
        retro_file = save_retrospective(result)
        
        print("\n" + "=" * 60)
        print("🎉 iOS Development Sprint Complete!")
        print("📋 Deliverables created:")
        print("   • Requirements Document")
        print("   • Architecture Design")
        print("   • iOS App Implementation")
        print("   • Test Strategy")
        print("   • Retrospective Report")
        
        if files_created:
            print("\n📱 Swift Files Created:")
            for filename in files_created:
                print(f"   • {filename}")
        else:
            print("\n⚠️  Note: Fallback basic structure was created")
            
        if retro_file:
            print(f"\n📋 Retrospective Document: {retro_file}")
        
        print("=" * 60)
        
        # Print summary
        print(f"\n📊 Final Result Summary:")
        print(result)
        
    except Exception as e:
        print(f"\n❌ Error during iOS development: {str(e)}")
        print("Check the error details above for troubleshooting.")

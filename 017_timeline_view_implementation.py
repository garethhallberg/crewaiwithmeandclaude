#!/usr/bin/env python3
"""
Timeline View Implementation - Get The Agents Working
Build TimelineView and PostRowView following established patterns
"""

import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process

main_app_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterClone"

# =============================================================================
# WORKING AGENTS - NO EXCUSES
# =============================================================================

timeline_view_builder = Agent(
    role='Timeline View Builder (No Nonsense)',
    goal='Build TimelineView that displays posts from TimelineViewModel',
    backstory="""You build SwiftUI Views that work. You study the existing LoginView, 
    RegistrationView, and PostCreationView to understand the patterns, then you apply 
    those same patterns to build TimelineView.
    
    You connect Views to ViewModels properly using @StateObject. You handle loading 
    states, error states, and data display. You don't overthink it - timeline is 
    just a list of posts following the same patterns as existing views.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

post_row_designer = Agent(
    role='Post Row Designer (UI Specialist)',
    goal='Create PostRowView component for displaying individual posts in the timeline',
    backstory="""You design individual UI components for displaying data. You create 
    clean, readable post rows that show the essential information: content, timestamp, 
    like count. You follow the visual design patterns from existing views and keep 
    it simple and functional.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

navigation_connector = Agent(
    role='Navigation Connector (Integration Expert)',
    goal='Connect timeline to existing app navigation so users can actually access it',
    backstory="""You connect new features to existing navigation. You update the 
    AuthenticatedView to navigate to TimelineView when users tap "View Timeline". 
    You follow the same navigation patterns used for PostCreationView - no complex 
    navigation, just working connections.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

api_endpoint_updater = Agent(
    role='API Endpoint Updater (Backend Connector)',
    goal='Add publicTimeline endpoint to APIEndpoint.swift for timeline data fetching',
    backstory="""You update API configurations to support new features. You add the
    publicTimeline case to APIEndpoint.swift following the same patterns as existing
    endpoints. You know the correct endpoint is /api/timeline/public and it uses GET method.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

# =============================================================================
# WORK TASKS - GET IT DONE
# =============================================================================

build_timeline_view_task = Task(
    description="""
    BUILD TIMELINEVIEW FOLLOWING EXISTING PATTERNS
    
    **STUDY THE PATTERNS:**
    Look at LoginView.swift, RegistrationView.swift, PostCreationView.swift
    
    **YOUR MISSION:**
    Build TimelineView.swift that:
    
    1. **Uses Same ViewModel Connection:**
       - @StateObject private var viewModel = TimelineViewModel.createDefault()
       - Same pattern as other views
    
    2. **Displays Posts in List:**
       - Use List(viewModel.posts, id: \\.id) { post in PostRowView(post: post) }
       - Shows timeline data from ViewModel
    
    3. **Handles Loading/Error States:**
       - Same loading spinner pattern as other views
       - Same error alert pattern: .alert("Error", isPresented: $viewModel.showError)
       - Same error handling as PostCreationView
    
    4. **Supports Refresh:**
       - Add .refreshable { await viewModel.loadTimeline() }
       - Load data on appear: .task { await viewModel.loadTimeline() }
    
    5. **Navigation Structure:**
       - NavigationView with .navigationTitle("Timeline")
       - Same structure as other views
    
    **REQUIREMENTS:**
    - Follow EXACT same patterns as existing views
    - Connect to TimelineViewModel properly
    - Handle all states (loading, success, error)
    - Include refresh functionality
    - Keep it simple - it's just a list of posts
    
    **OUTPUT:**
    Complete TimelineView.swift file that works with existing TimelineViewModel
    """,
    expected_output="Complete TimelineView.swift implementation",
    agent=timeline_view_builder
)

create_post_row_task = Task(
    description="""
    CREATE POSTROWVIEW FOR DISPLAYING INDIVIDUAL POSTS
    
    **YOUR MISSION:**
    Build PostRowView.swift that displays a single post nicely:
    
    1. **Post Data Display:**
       - Show post.content (main text)
       - Show post.createdAt (formatted timestamp)
       - Show post.likeCount (number of likes)
    
    2. **Visual Design:**
       - Clean, readable layout
       - Use VStack for vertical arrangement
       - Use HStack for timestamp/likes row
       - Follow same padding/spacing as other views
    
    3. **Text Formatting:**
       - Content: .font(.body)
       - Timestamp: .font(.caption).foregroundColor(.secondary)
       - Likes: .font(.caption).foregroundColor(.secondary)
    
    4. **Layout Structure:**
       ```swift
       VStack(alignment: .leading, spacing: 8) {
           Text(post.content)
               .font(.body)
           
           HStack {
               Text(post.createdAt, style: .relative)
                   .font(.caption)
                   .foregroundColor(.secondary)
               
               Spacer()
               
               Text("♥ \\(post.likeCount)")
                   .font(.caption)
                   .foregroundColor(.secondary)
           }
       }
       .padding(.vertical, 4)
       ```
    
    **REQUIREMENTS:**
    - Accept Post object as parameter
    - Display content, timestamp, like count
    - Use clean, readable formatting
    - Follow visual patterns from existing views
    
    **OUTPUT:**
    Complete PostRowView.swift file for displaying posts
    """,
    expected_output="Complete PostRowView.swift implementation",
    agent=post_row_designer,
    depends_on=[build_timeline_view_task]
)

update_api_endpoints_task = Task(
    description="""
    ADD PUBLICTIMELINE ENDPOINT TO APIENDPOINT.SWIFT
    
    **YOUR MISSION:**
    Update APIEndpoint.swift to support timeline data fetching:
    
    1. **Add New Case:**
       Add `case publicTimeline` to the APIEndpoint enum
    
    2. **Update Path:**
       In the `path` computed property, add:
       ```swift
       case .publicTimeline:
           return "/api/timeline/public"
       ```
    
    3. **Update Method:**
       In the `method` computed property, add:
       ```swift
       case .publicTimeline:
           return .GET
       ```
    
    4. **Update Body:**
       In the `body` computed property, add:
       ```swift
       case .publicTimeline:
           return nil
       ```
    
    **FOLLOW EXISTING PATTERNS:**
    - Look at how .login, .register, .createPost are implemented
    - Add .publicTimeline the same way
    - Keep it simple - it's just a GET request to /api/timeline/public
    
    **OUTPUT:**
    Updated APIEndpoint.swift with publicTimeline support
    """,
    expected_output="Updated APIEndpoint.swift with timeline endpoint",
    agent=api_endpoint_updater,
    depends_on=[create_post_row_task]
)

connect_timeline_navigation_task = Task(
    description="""
    CONNECT TIMELINE TO APP NAVIGATION
    
    **YOUR MISSION:**
    Update the AuthenticatedView in LoginView.swift to navigate to TimelineView:
    
    1. **Add State Variable:**
       Add `@State private var showTimeline = false` 
    
    2. **Update "View Timeline" Button:**
       Change the button action from `print("Timeline tapped")` to:
       ```swift
       Button(action: {
           showTimeline = true
       }) {
           // existing button content
       }
       ```
    
    3. **Add Navigation:**
       Add timeline sheet presentation:
       ```swift
       .sheet(isPresented: $showTimeline) {
           TimelineView()
       }
       ```
    
    **FOLLOW EXISTING PATTERN:**
    - Look at how PostCreationView navigation is implemented
    - Use the same `.sheet(isPresented:)` pattern for TimelineView
    - Connect the button action to show timeline
    
    **SIMPLE INTEGRATION:**
    - Users tap "View Timeline" → TimelineView appears
    - Same pattern as "Create Post" → PostCreationView
    
    **OUTPUT:**
    Updated AuthenticatedView with working timeline navigation
    """,
    expected_output="Updated navigation to connect timeline to app",
    agent=navigation_connector,
    depends_on=[update_api_endpoints_task]
)

# =============================================================================
# FILE EXTRACTION AND CREATION
# =============================================================================

def extract_and_create_timeline_files(crew_result):
    """Extract timeline implementation files from agent output"""
    
    result_text = str(crew_result)
    
    # Save debug output
    debug_file = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai") / "timeline_view_implementation.txt"
    with open(debug_file, 'w') as f:
        f.write(result_text)
    print(f"🔍 Output saved to: timeline_view_implementation.txt")
    
    files_created = []
    
    # Extract Swift code files
    import re
    
    # Extract TimelineView
    timeline_view_patterns = [
        r'```swift\n(.*?struct TimelineView.*?)\n```',
        r'(import SwiftUI.*?struct TimelineView.*?)(?=\n\n|\n```|\nimport)',
    ]
    
    for pattern in timeline_view_patterns:
        matches = re.findall(pattern, result_text, re.DOTALL)
        for match in matches:
            code = match.strip()
            if 'struct TimelineView' in code and len(code) > 400:
                views_dir = Path(main_app_path) / "Views"
                views_dir.mkdir(exist_ok=True)
                with open(views_dir / "TimelineView.swift", 'w') as f:
                    f.write(code)
                files_created.append("TimelineView.swift")
                print(f"✅ Created TimelineView.swift ({len(code)} chars)")
                break
    
    # Extract PostRowView
    post_row_patterns = [
        r'```swift\n(.*?struct PostRowView.*?)\n```',
        r'(import SwiftUI.*?struct PostRowView.*?)(?=\n\n|\n```|\nimport)',
    ]
    
    for pattern in post_row_patterns:
        matches = re.findall(pattern, result_text, re.DOTALL)
        for match in matches:
            code = match.strip()
            if 'struct PostRowView' in code and len(code) > 200:
                views_dir = Path(main_app_path) / "Views"
                views_dir.mkdir(exist_ok=True)
                with open(views_dir / "PostRowView.swift", 'w') as f:
                    f.write(code)
                files_created.append("PostRowView.swift")
                print(f"✅ Created PostRowView.swift ({len(code)} chars)")
                break
    
    # Extract APIEndpoint updates
    api_patterns = [
        r'```swift\n(.*?enum APIEndpoint.*?)\n```',
        r'(import Foundation.*?enum APIEndpoint.*?)(?=\n\n|\n```|\nimport)',
    ]
    
    for pattern in api_patterns:
        matches = re.findall(pattern, result_text, re.DOTALL)
        for match in matches:
            code = match.strip()
            if 'publicTimeline' in code and len(code) > 500:
                networking_dir = Path(main_app_path) / "Networking"
                with open(networking_dir / "APIEndpoint.swift", 'w') as f:
                    f.write(code)
                files_created.append("APIEndpoint.swift (updated)")
                print(f"✅ Updated APIEndpoint.swift ({len(code)} chars)")
                break
    
    # For navigation updates, we'd need to manually check the LoginView.swift changes
    if "showTimeline" in result_text:
        files_created.append("Navigation updates (manual check needed)")
        print("✅ Found navigation updates in output")
    
    return files_created

# =============================================================================
# EXECUTION - GET THE AGENTS WORKING
# =============================================================================

if __name__ == "__main__":
    print("💪 TIMELINE VIEW IMPLEMENTATION - AGENTS GET TO WORK!")
    print("=" * 60)
    print("🎯 Mission: Build TimelineView following existing patterns")
    print("🔨 No excuses, no fancy stuff - just working timeline UI")
    print("=" * 60)
    
    crew = Crew(
        agents=[timeline_view_builder, post_row_designer, api_endpoint_updater, navigation_connector],
        tasks=[build_timeline_view_task, create_post_row_task, update_api_endpoints_task, connect_timeline_navigation_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        result = crew.kickoff()
        
        # Extract and create files
        files_created = extract_and_create_timeline_files(result)
        
        print("\n" + "=" * 60)
        print("🎯 TIMELINE VIEW IMPLEMENTATION RESULTS:")
        if len(files_created) >= 3:
            print("🎉 SUCCESS! Timeline UI components created!")
            print("📋 Files Created/Updated:")
            for filename in files_created:
                print(f"   ✅ {filename}")
            print("\n📱 Ready to test timeline in the app!")
            print("💡 Tap 'View Timeline' from dashboard to test")
        else:
            print("⚠️  Implementation incomplete")
            print(f"📋 Created {len(files_created)} files")
            print("📋 Files Created:")
            for filename in files_created:
                print(f"   ✅ {filename}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n💥 TIMELINE VIEW IMPLEMENTATION FAILED: {str(e)}")

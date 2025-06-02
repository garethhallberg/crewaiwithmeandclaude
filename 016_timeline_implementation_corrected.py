#!/usr/bin/env python3
"""
Timeline Implementation - Corrected Endpoints
Build timeline feature with correct backend endpoints
"""

import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process

main_app_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterClone"

# =============================================================================
# IMPLEMENTATION AGENTS
# =============================================================================

timeline_implementation_lead = Agent(
    role='Timeline Implementation Lead',
    goal='Build complete timeline feature with correct endpoints and patterns',
    backstory="""You build timeline features by following established patterns. You know that:
    
    CORRECT ENDPOINTS (verified in backend):
    - /api/timeline/public - Public timeline with all posts
    - /api/timeline/home - Home timeline (currently same as public)
    - Returns Page<PostDto> with pagination
    
    ESTABLISHED PATTERNS (from existing code):
    - Same MVVM as LoginViewModel, RegistrationViewModel, PostCreationViewModel
    - Same NetworkManagerProtocol usage
    - Same @Published properties and state management
    - Same error handling with NetworkError
    
    You build working timeline features that integrate with existing patterns.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

# =============================================================================
# IMPLEMENTATION TASK
# =============================================================================

build_complete_timeline_task = Task(
    description="""
    BUILD COMPLETE TIMELINE FEATURE WITH CORRECT ENDPOINTS
    
    **BACKEND ENDPOINTS (VERIFIED):**
    - Use `/api/timeline/public` for public timeline
    - Endpoint returns Page<PostDto> with posts array and pagination
    - No authentication required for public timeline
    - Posts are sorted by createdAt descending (newest first)
    
    **IMPLEMENTATION REQUIREMENTS:**
    
    1. **TimelineViewModel.swift**
    Follow LoginViewModel/RegistrationViewModel/PostCreationViewModel patterns:
    ```swift
    @MainActor
    class TimelineViewModel: ObservableObject {
        @Published var posts: [Post] = []
        @Published var isLoading: Bool = false
        @Published var errorMessage: String = ""
        @Published var showError: Bool = false
        
        private let networkManager: NetworkManagerProtocol
        
        init(networkManager: NetworkManagerProtocol) {
            self.networkManager = networkManager
        }
        
        static func createDefault() -> TimelineViewModel {
            return TimelineViewModel(networkManager: NetworkManager.shared)
        }
        
        func loadTimeline() async {
            // Use .publicTimeline endpoint that calls /api/timeline/public
            // Handle Page<PostDto> response
            // Extract posts array from response
            // Same error handling as other ViewModels
        }
    }
    ```
    
    2. **TimelineView.swift**
    Follow LoginView/RegistrationView/PostCreationView patterns:
    ```swift
    struct TimelineView: View {
        @StateObject private var viewModel = TimelineViewModel.createDefault()
        
        var body: some View {
            NavigationView {
                List(viewModel.posts, id: \\.id) { post in
                    PostRowView(post: post)
                }
                .navigationTitle("Timeline")
                .refreshable {
                    await viewModel.loadTimeline()
                }
            }
            .alert("Error", isPresented: $viewModel.showError) {
                Button("OK") { viewModel.clearError() }
            } message: {
                Text(viewModel.errorMessage)
            }
            .task {
                await viewModel.loadTimeline()
            }
        }
    }
    ```
    
    3. **PostRowView.swift**
    Simple post display component:
    ```swift
    struct PostRowView: View {
        let post: Post
        
        var body: some View {
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
        }
    }
    ```
    
    4. **Update APIEndpoint.swift**
    Add timeline endpoint:
    ```swift
    case publicTimeline
    
    // In path:
    case .publicTimeline:
        return "/api/timeline/public"
    
    // In method:
    case .publicTimeline:
        return .GET
    ```
    
    5. **Update AuthenticatedView navigation**
    Connect "View Timeline" button to TimelineView
    
    **KEY REQUIREMENTS:**
    - Use CORRECT endpoint: /api/timeline/public
    - Follow SAME patterns as existing ViewModels/Views
    - Handle Page<PostDto> response properly
    - Include proper error handling
    - Integrate with existing navigation
    
    **OUTPUT ALL FILES:**
    - TimelineViewModel.swift
    - TimelineView.swift  
    - PostRowView.swift
    - Updated APIEndpoint.swift
    - Updated AuthenticatedView navigation
    
    Build complete, working timeline feature following established patterns.
    """,
    expected_output="Complete timeline implementation with all necessary files",
    agent=timeline_implementation_lead
)

# =============================================================================
# FILE CREATION
# =============================================================================

def create_timeline_files(crew_result):
    """Extract and create timeline implementation files"""
    
    result_text = str(crew_result)
    
    # Save debug output
    debug_file = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai") / "timeline_implementation_output.txt"
    with open(debug_file, 'w') as f:
        f.write(result_text)
    print(f"🔍 Implementation output saved to: timeline_implementation_output.txt")
    
    # Extract Swift files
    import re
    files_created = []
    
    # Extract files using various patterns
    swift_patterns = [
        r'```swift\n(.*?class TimelineViewModel.*?)\n```',
        r'```swift\n(.*?struct TimelineView.*?)\n```', 
        r'```swift\n(.*?struct PostRowView.*?)\n```',
        r'```swift\n(.*?enum APIEndpoint.*?)\n```'
    ]
    
    for pattern in swift_patterns:
        matches = re.findall(pattern, result_text, re.DOTALL)
        for match in matches:
            code = match.strip()
            
            # Determine file type and create
            if 'class TimelineViewModel' in code and len(code) > 500:
                viewmodels_dir = Path(main_app_path) / "ViewModels"
                viewmodels_dir.mkdir(exist_ok=True)
                with open(viewmodels_dir / "TimelineViewModel.swift", 'w') as f:
                    f.write(code)
                files_created.append("TimelineViewModel.swift")
                print(f"✅ Created TimelineViewModel.swift ({len(code)} chars)")
                
            elif 'struct TimelineView' in code and len(code) > 400:
                views_dir = Path(main_app_path) / "Views"  
                views_dir.mkdir(exist_ok=True)
                with open(views_dir / "TimelineView.swift", 'w') as f:
                    f.write(code)
                files_created.append("TimelineView.swift")
                print(f"✅ Created TimelineView.swift ({len(code)} chars)")
                
            elif 'struct PostRowView' in code and len(code) > 200:
                views_dir = Path(main_app_path) / "Views"
                views_dir.mkdir(exist_ok=True)
                with open(views_dir / "PostRowView.swift", 'w') as f:
                    f.write(code)
                files_created.append("PostRowView.swift") 
                print(f"✅ Created PostRowView.swift ({len(code)} chars)")
    
    return files_created

# =============================================================================
# EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("🔨 TIMELINE IMPLEMENTATION - CORRECTED ENDPOINTS")
    print("=" * 60)
    print("✅ Using verified backend endpoints: /api/timeline/public")
    print("🎯 Following established MVVM patterns")
    print("=" * 60)
    
    crew = Crew(
        agents=[timeline_implementation_lead],
        tasks=[build_complete_timeline_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        result = crew.kickoff()
        
        # Create timeline files
        files_created = create_timeline_files(result)
        
        print("\n" + "=" * 60)
        print("🎯 TIMELINE IMPLEMENTATION RESULTS:")
        if len(files_created) >= 2:
            print("🎉 SUCCESS! Timeline files created!")
            print("📋 Files Created:")
            for filename in files_created:
                print(f"   ✅ {filename}")
            print("📱 Ready to test timeline feature!")
        else:
            print("⚠️  Implementation incomplete")
            print(f"📋 Created {len(files_created)} files")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n💥 TIMELINE IMPLEMENTATION FAILED: {str(e)}")

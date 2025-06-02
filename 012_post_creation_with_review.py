#!/usr/bin/env python3
"""
Post Creation with Code Review - No Bad Code Allowed
Agents build PostCreationView/ViewModel with a tough evaluator ensuring quality
"""

import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process

main_app_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterClone"

# =============================================================================
# IMPLEMENTATION + REVIEW AGENTS
# =============================================================================

post_viewmodel_developer = Agent(
    role='PostCreationViewModel Developer',
    goal='Build PostCreationViewModel following the exact patterns from LoginViewModel and RegistrationViewModel',
    backstory="""You build ViewModels by studying existing successful patterns. You analyzed
    LoginViewModel and RegistrationViewModel in your discovery phase. Now you implement
    PostCreationViewModel using the same architectural approach, networking patterns,
    and state management techniques.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

post_view_developer = Agent(
    role='PostCreationView Developer', 
    goal='Build PostCreationView following the exact patterns from LoginView and RegistrationView',
    backstory="""You build SwiftUI Views by following established patterns. You analyzed
    LoginView and RegistrationView in your discovery phase. Now you implement
    PostCreationView using the same UI patterns, ViewModel binding, and visual design.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

senior_code_reviewer = Agent(
    role='Senior iOS Code Reviewer (Quality Enforcer)',
    goal='Ruthlessly evaluate implementations against existing patterns and reject substandard work',
    backstory="""You are a senior iOS developer who enforces code quality and architectural consistency.
    You have zero tolerance for implementations that don't follow established patterns.
    
    You know EXACTLY how LoginViewModel and RegistrationViewModel work in this codebase.
    You know EXACTLY how LoginView and RegistrationView are structured.
    
    If the new PostCreation code doesn't follow the same patterns, you REJECT it and demand fixes.
    You check for: proper @Published properties, correct networking usage, proper error handling,
    MVVM binding, UI consistency, and integration with existing systems.
    
    You are the quality gatekeeper - nothing gets through that doesn't meet the established standards.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

# =============================================================================
# IMPLEMENTATION TASKS
# =============================================================================

develop_viewmodel_task = Task(
    description="""
    DEVELOP POSTCREATIONVIEWMODEL FOLLOWING EXISTING PATTERNS
    
    **REQUIREMENTS:**
    Based on your analysis, build PostCreationViewModel.swift that:
    
    1. **Uses same @Published properties pattern** as LoginViewModel/RegistrationViewModel
    2. **Uses same NetworkManagerProtocol** for API calls
    3. **Uses same error handling approach** with NetworkError types
    4. **Uses same validation patterns** for form data
    5. **Uses same loading state management** with isLoading
    6. **Uses same factory method pattern** with createDefault()
    
    **SPECIFIC REQUIREMENTS:**
    - @Published var content: String for post text
    - @Published var isLoading: Bool for loading states
    - @Published var errorMessage: String for errors
    - @Published var showError: Bool for error alerts
    - @Published var isPosted: Bool for success state
    - Computed properties for form validation
    - async func createPost() method
    - Proper error handling following LoginViewModel pattern
    
    **API INTEGRATION:**
    - Use .createPost endpoint you discovered in analysis
    - Follow same networking pattern as login/registration
    - Handle success and error cases properly
    
    Build the complete PostCreationViewModel.swift file.
    """,
    expected_output="Complete PostCreationViewModel.swift implementation",
    agent=post_viewmodel_developer
)

develop_view_task = Task(
    description="""
    DEVELOP POSTCREATIONVIEW FOLLOWING EXISTING PATTERNS
    
    **REQUIREMENTS:**
    Based on your analysis, build PostCreationView.swift that:
    
    1. **Uses same @StateObject binding** as LoginView/RegistrationView
    2. **Uses same form styling** with RoundedBorderTextFieldStyle
    3. **Uses same button patterns** with loading states and disabled states
    4. **Uses same alert patterns** for error handling
    5. **Uses same navigation patterns** for screen flow
    6. **Uses same visual design** as existing screens
    
    **SPECIFIC REQUIREMENTS:**
    - @StateObject private var viewModel = PostCreationViewModel.createDefault()
    - Text input area for post content (TextEditor or TextField)
    - Post button with loading spinner when viewModel.isLoading
    - Character count display
    - Proper form validation feedback
    - Error alert binding to viewModel.showError
    - Navigation handling after successful post
    - Cancel/dismiss functionality
    
    **UI CONSISTENCY:**
    - Same header style as LoginView/RegistrationView
    - Same color scheme and typography
    - Same spacing and padding patterns
    - Same button styling and states
    
    Build the complete PostCreationView.swift file.
    """,
    expected_output="Complete PostCreationView.swift implementation",
    agent=post_view_developer,
    depends_on=[develop_viewmodel_task]
)

code_review_task = Task(
    description="""
    RUTHLESSLY REVIEW THE POSTCREATION IMPLEMENTATIONS
    
    **YOUR MISSION:**
    Evaluate both PostCreationViewModel.swift and PostCreationView.swift against the established patterns.
    
    **CHECKLIST - POSTCREATIONVIEWMODEL:**
    ✅ Uses @Published properties like LoginViewModel/RegistrationViewModel?
    ✅ Uses NetworkManagerProtocol the same way?
    ✅ Has createDefault() factory method?
    ✅ Has proper async func createPost() method?
    ✅ Uses same error handling with NetworkError?
    ✅ Has computed properties for validation?
    ✅ Follows same initialization pattern?
    ✅ Has proper state management for loading/error/success?
    
    **CHECKLIST - POSTCREATIONVIEW:**
    ✅ Uses @StateObject binding like LoginView/RegistrationView?
    ✅ Has proper form input connected to viewModel?
    ✅ Has button with loading state like other views?
    ✅ Has error alert binding like other views?
    ✅ Uses same visual styling and components?
    ✅ Has proper navigation and dismiss functionality?
    ✅ Follows same layout patterns?
    ✅ Has proper form validation display?
    
    **INTEGRATION CHECKS:**
    ✅ Will this integrate properly with existing AuthenticatedView?
    ✅ Does this follow the app's navigation patterns?
    ✅ Will this work with existing NetworkManager setup?
    ✅ Does this handle authentication properly?
    
    **YOUR VERDICT:**
    - If implementations are solid and follow patterns: APPROVE
    - If implementations are missing key features: REJECT with specific feedback
    - If implementations don't follow established patterns: REJECT and demand compliance
    
    **BE RUTHLESS:** Don't accept mediocre code that doesn't match the quality of existing implementations.
    """,
    expected_output="Code review verdict with approval or rejection and specific feedback",
    agent=senior_code_reviewer,
    depends_on=[develop_view_task]
)

# =============================================================================
# FILE CREATION WITH QUALITY CONTROL
# =============================================================================

def apply_reviewed_implementation(crew_result):
    """Only create files if they pass code review"""
    
    result_text = str(crew_result)
    
    # Save full output
    debug_file = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai") / "post_creation_with_review.txt"
    with open(debug_file, 'w') as f:
        f.write(result_text)
    print(f"🔍 Full output saved to: post_creation_with_review.txt")
    
    # Check if code review approved
    if "APPROVE" in result_text or "approved" in result_text.lower():
        print("✅ CODE REVIEW PASSED - Creating files...")
        
        # Extract and create files
        import re
        files_created = []
        
        # Extract PostCreationViewModel
        viewmodel_matches = re.findall(r'```swift\n(.*?class PostCreationViewModel.*?)\n```', result_text, re.DOTALL)
        for match in viewmodel_matches:
            if len(match) > 800:  # Substantial implementation
                viewmodels_dir = Path(main_app_path) / "ViewModels"
                viewmodels_dir.mkdir(exist_ok=True)
                with open(viewmodels_dir / "PostCreationViewModel.swift", 'w') as f:
                    f.write(match)
                files_created.append("PostCreationViewModel.swift")
                print("✅ Created PostCreationViewModel.swift")
                break
        
        # Extract PostCreationView
        view_matches = re.findall(r'```swift\n(.*?struct PostCreationView.*?)\n```', result_text, re.DOTALL)
        for match in view_matches:
            if len(match) > 600:  # Substantial implementation
                views_dir = Path(main_app_path) / "Views"
                views_dir.mkdir(exist_ok=True)
                with open(views_dir / "PostCreationView.swift", 'w') as f:
                    f.write(match)
                files_created.append("PostCreationView.swift")
                print("✅ Created PostCreationView.swift")
                break
        
        return files_created
        
    else:
        print("❌ CODE REVIEW FAILED - No files created!")
        print("📋 Review the feedback in post_creation_with_review.txt")
        print("🔧 Agents need to fix their implementations")
        return []

# =============================================================================
# EXECUTION WITH QUALITY GATE
# =============================================================================

if __name__ == "__main__":
    print("🏗️  POST CREATION WITH CODE REVIEW - QUALITY ENFORCED!")
    print("=" * 70)
    print("💪 Developers: Build following established patterns")
    print("🔍 Reviewer: Enforce quality and consistency") 
    print("=" * 70)
    
    crew = Crew(
        agents=[post_viewmodel_developer, post_view_developer, senior_code_reviewer],
        tasks=[develop_viewmodel_task, develop_view_task, code_review_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        result = crew.kickoff()
        
        # Only create files if review passes
        files_created = apply_reviewed_implementation(result)
        
        print("\n" + "=" * 70)
        print("🎯 IMPLEMENTATION WITH REVIEW RESULTS:")
        if len(files_created) >= 2:
            print("🎉 SUCCESS! Code passed review and files created!")
            print("📋 Files Created:")
            for filename in files_created:
                print(f"   ✅ {filename}")
            print("📱 Ready to test post creation feature")
        elif len(files_created) > 0:
            print("⚠️  Partial success - some files created")
            print("📋 Files Created:")
            for filename in files_created:
                print(f"   ✅ {filename}")
        else:
            print("❌ FAILED CODE REVIEW - No files created")
            print("📋 Check post_creation_with_review.txt for feedback")
            print("🔧 Agents need to improve their implementations")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n💥 EXECUTION FAILED: {str(e)}")

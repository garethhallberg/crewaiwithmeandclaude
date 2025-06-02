#!/usr/bin/env python3
"""
iOS Login ViewModel - MVVM PATTERN IMPLEMENTATION
Create the ViewModel layer that connects LoginView to NetworkManager!
NO DIRECT UI-TO-NETWORK CALLS! PROPER MVVM SEPARATION!
"""

import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process

# Set working directory
ios_project_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone"
main_app_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterClone"

# =============================================================================
# MVVM SPECIALISTS - VIEWMODEL LAYER EXPERTS
# =============================================================================

mvvm_architect = Agent(
    role='Senior MVVM Architect (Pattern Expert)',
    goal='Design clean, testable ViewModel architecture following MVVM best practices',
    backstory="""You are an MVVM expert who creates perfect separation between View and Model layers.
    Your ViewModels are ObservableObject classes that handle all business logic and state management.
    You never let Views talk directly to networking layers - everything goes through ViewModels.
    Your code is clean, testable, and follows all SwiftUI/Combine best practices.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

state_manager = Agent(
    role='State Management Specialist (Reactive Expert)',
    goal='Implement robust state management using @Published properties and Combine',
    backstory="""You specialize in reactive state management with SwiftUI and Combine.
    Your @Published properties trigger UI updates perfectly, and you handle loading states,
    error states, and success states with precision. You know exactly when to use
    @MainActor and how to handle async operations in ViewModels.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

networking_integrator = Agent(
    role='Networking Integration Expert (API Connector)',
    goal='Connect ViewModels to NetworkManager with proper async/await patterns',
    backstory="""You are the bridge between ViewModels and networking layers.
    You handle all async/await networking calls, parse API responses correctly,
    and convert network errors into user-friendly error states.
    Your networking integration is bulletproof and handles all edge cases.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

# =============================================================================
# VIEWMODEL IMPLEMENTATION TASKS
# =============================================================================

viewmodel_architecture_task = Task(
    description="""
    DESIGN THE LOGIN VIEWMODEL ARCHITECTURE
    
    **VIEWMODEL REQUIREMENTS:**
    
    1. **Class Structure:**
       - ObservableObject conformance
       - @MainActor annotation for UI updates
       - Clean initialization
       - Dependency injection ready (NetworkManager)
    
    2. **Published Properties for UI State:**
       - username: String (form input)
       - password: String (form input)
       - isLoading: Bool (loading state)
       - errorMessage: String (error display)
       - showError: Bool (error alert trigger)
       - isLoggedIn: Bool (success state)
    
    3. **Computed Properties:**
       - isFormValid: Bool (enable/disable login button)
       - canSubmit: Bool (form validation + not loading)
    
    4. **Public Methods:**
       - login() async -> performs authentication
       - clearError() -> resets error state
       - reset() -> clears all form data
    
    5. **Private Methods:**
       - validateForm() -> form validation logic
       - handleLoginSuccess() -> success state handling
       - handleLoginError() -> error state handling
    
    **ARCHITECTURE PRINCIPLES:**
    - Single responsibility (login logic only)
    - Testable design (injectable dependencies)
    - Clear separation from UI layer
    - Proper error handling
    - Thread-safe operations
    
    **DELIVERABLE:**
    Complete ViewModel architecture specification with all methods and properties defined.
    """,
    expected_output="Detailed LoginViewModel architecture with complete class design",
    agent=mvvm_architect
)

state_management_task = Task(
    description="""
    IMPLEMENT STATE MANAGEMENT AND REACTIVE PROPERTIES
    
    **STATE MANAGEMENT REQUIREMENTS:**
    
    1. **@Published Properties Implementation:**
       ```swift
       @Published var username: String = ""
       @Published var password: String = ""
       @Published var isLoading: Bool = false
       @Published var errorMessage: String = ""
       @Published var showError: Bool = false
       @Published var isLoggedIn: Bool = false
       ```
    
    2. **Computed Properties:**
       - isFormValid: Check username and password not empty
       - canSubmit: Form valid AND not currently loading
       - loginButtonTitle: Dynamic text based on loading state
    
    3. **State Transitions:**
       - Loading state: Set isLoading = true, clear errors
       - Success state: Set isLoggedIn = true, clear loading
       - Error state: Set errorMessage, showError = true, clear loading
       - Reset state: Clear all fields and states
    
    4. **Form Validation Logic:**
       - Username: Not empty, trimmed whitespace
       - Password: Minimum length requirements
       - Real-time validation updates
    
    5. **Error Handling States:**
       - Network errors
       - Authentication failures
       - Validation errors
       - Server errors
    
    **THREAD SAFETY:**
    - All UI updates on main thread
    - Proper @MainActor usage
    - Safe async operations
    
    **DELIVERABLE:**
    Complete state management implementation with all @Published properties and state transitions.
    """,
    expected_output="Full state management implementation with reactive properties",
    agent=state_manager,
    depends_on=[viewmodel_architecture_task]
)

networking_integration_task = Task(
    description="""
    IMPLEMENT NETWORKING INTEGRATION AND API CALLS
    
    **NETWORKING REQUIREMENTS:**
    
    Create complete LoginViewModel.swift file in: /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterClone/ViewModels/
    
    **API INTEGRATION:**
    
    1. **NetworkManager Integration:**
       - Inject NetworkManager.shared dependency
       - Use existing APIEndpoint.login() method
       - Handle AuthResponse parsing
       - Proper async/await patterns
    
    2. **Login Method Implementation:**
       ```swift
       func login() async {
           guard canSubmit else { return }
           
           await MainActor.run {
               isLoading = true
               clearError()
           }
           
           do {
               let response: AuthResponse = try await networkManager.request(
                   endpoint: .login(username: username, password: password),
                   responseType: AuthResponse.self
               )
               
               await handleLoginSuccess(response)
               
           } catch {
               await handleLoginError(error)
           }
       }
       ```
    
    3. **Response Handling:**
       - Parse AuthResponse correctly
       - Extract JWT token
       - Extract User data
       - Update success state
    
    4. **Error Handling:**
       - NetworkError cases
       - HTTP status codes
       - JSON parsing errors
       - User-friendly error messages
    
    5. **API Response Types:**
       - Use existing AuthResponse model
       - Handle User model structure
       - Token extraction logic
    
    **COMPLETE FILE STRUCTURE:**
    ```swift
    // FILE: LoginViewModel.swift
    import Foundation
    import SwiftUI
    
    @MainActor
    class LoginViewModel: ObservableObject {
        // COMPLETE IMPLEMENTATION HERE
    }
    ```
    
    **INTEGRATION REQUIREMENTS:**
    - Import existing NetworkManager
    - Import existing APIEndpoint
    - Import existing AuthResponse/User models
    - Handle all async/await properly
    - Provide user-friendly error messages
    
    NO PLACEHOLDER METHODS! COMPLETE IMPLEMENTATION REQUIRED!
    """,
    expected_output="Complete LoginViewModel.swift with full networking integration",
    agent=networking_integrator,
    depends_on=[state_management_task]
)

# =============================================================================
# VIEWMODEL FILE CREATION
# =============================================================================

def create_viewmodel_files(crew_result):
    """Extract and create ViewModel files"""
    
    print("\n🏗️  CREATING LOGIN VIEWMODEL!")
    
    viewmodels_dir = Path(main_app_path) / "ViewModels"
    viewmodels_dir.mkdir(exist_ok=True)
    
    result_text = str(crew_result)
    
    # Save debug output
    debug_file = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai") / "login_viewmodel_debug.txt"
    with open(debug_file, 'w') as f:
        f.write(result_text)
    print(f"🔍 Debug output: login_viewmodel_debug.txt")
    
    # Extract Swift ViewModel files
    import re
    pattern = r'// FILE: ([^\n]+\.swift)\n([\s\S]*?)(?=// FILE:|$)'
    matches = re.findall(pattern, result_text, re.MULTILINE | re.DOTALL)
    
    print(f"📝 Found {len(matches)} Swift ViewModel files")
    
    files_created = []
    
    for filename, code_content in matches:
        filename = filename.strip()
        code_content = code_content.strip()
        
        # Clean up code blocks
        code_content = re.sub(r'^```swift\n?', '', code_content, flags=re.MULTILINE)
        code_content = re.sub(r'^```\n?', '', code_content, flags=re.MULTILINE)
        code_content = code_content.strip()
        
        # Validate this is substantial ViewModel code
        if len(code_content) < 400:  # ViewModels should be substantial
            print(f"⚠️  {filename} too short ({len(code_content)} chars) - might be empty")
            continue
            
        # Check for ViewModel components
        required_patterns = ['ObservableObject', '@Published', 'func login']
        missing_patterns = [p for p in required_patterns if p not in code_content]
        
        if missing_patterns:
            print(f"⚠️  {filename} missing: {', '.join(missing_patterns)}")
            continue
        
        file_path = viewmodels_dir / filename
        
        try:
            with open(file_path, 'w') as f:
                f.write(code_content)
            
            print(f"✅ Created: {filename} ({len(code_content)} chars)")
            files_created.append(filename)
            
            # Validate ViewModel features
            features = []
            if '@Published' in code_content:
                published_count = code_content.count('@Published')
                features.append(f'{published_count} @Published properties')
            if 'async' in code_content:
                features.append('Async methods')
            if 'NetworkManager' in code_content:
                features.append('NetworkManager integration')
            if '@MainActor' in code_content:
                features.append('MainActor threading')
            
            if features:
                print(f"   🎯 Features: {', '.join(features)}")
            
        except Exception as e:
            print(f"❌ Failed to create {filename}: {str(e)}")
    
    # Create professional fallback if agents failed
    if len(files_created) == 0:
        print("\n🔥 AGENTS FAILED! Creating professional fallback ViewModel...")
        create_professional_login_viewmodel(viewmodels_dir)
        files_created.append("LoginViewModel.swift")
    
    return files_created

def create_professional_login_viewmodel(viewmodels_dir):
    """Create professional LoginViewModel as fallback"""
    
    login_viewmodel = '''import Foundation
import SwiftUI

@MainActor
class LoginViewModel: ObservableObject {
    // MARK: - Published Properties
    @Published var username: String = ""
    @Published var password: String = ""
    @Published var isLoading: Bool = false
    @Published var errorMessage: String = ""
    @Published var showError: Bool = false
    @Published var isLoggedIn: Bool = false
    
    // MARK: - Dependencies
    private let networkManager: NetworkManager
    
    // MARK: - Computed Properties
    var isFormValid: Bool {
        !username.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty &&
        !password.isEmpty && password.count >= 6
    }
    
    var canSubmit: Bool {
        isFormValid && !isLoading
    }
    
    var loginButtonTitle: String {
        isLoading ? "Signing In..." : "Sign In"
    }
    
    // MARK: - Initialization
    init(networkManager: NetworkManager = NetworkManager.shared) {
        self.networkManager = networkManager
    }
    
    // MARK: - Public Methods
    func login() async {
        guard canSubmit else { return }
        
        isLoading = true
        clearError()
        
        do {
            let response: AuthResponse = try await networkManager.request(
                endpoint: .login(username: username.trimmingCharacters(in: .whitespacesAndNewlines), 
                               password: password),
                responseType: AuthResponse.self
            )
            
            await handleLoginSuccess(response)
            
        } catch {
            await handleLoginError(error)
        }
    }
    
    func clearError() {
        errorMessage = ""
        showError = false
    }
    
    func reset() {
        username = ""
        password = ""
        isLoading = false
        clearError()
        isLoggedIn = false
    }
    
    // MARK: - Private Methods
    private func handleLoginSuccess(_ response: AuthResponse) async {
        isLoading = false
        isLoggedIn = true
        
        // TODO: Next phase - integrate with AuthManager for JWT storage
        print("Login successful! Token: \\(response.token)")
        print("User: \\(response.user.username)")
    }
    
    private func handleLoginError(_ error: Error) async {
        isLoading = false
        
        if let networkError = error as? NetworkError {
            switch networkError {
            case .serverError(let statusCode):
                if statusCode == 401 {
                    errorMessage = "Invalid username or password"
                } else {
                    errorMessage = "Server error. Please try again."
                }
            case .requestFailed:
                errorMessage = "Network connection failed. Check your internet connection."
            case .invalidResponse:
                errorMessage = "Invalid server response. Please try again."
            case .decodingError:
                errorMessage = "Unable to process server response. Please try again."
            default:
                errorMessage = "An unexpected error occurred. Please try again."
            }
        } else {
            errorMessage = "An unexpected error occurred. Please try again."
        }
        
        showError = true
    }
    
    private func validateForm() -> Bool {
        let trimmedUsername = username.trimmingCharacters(in: .whitespacesAndNewlines)
        
        guard !trimmedUsername.isEmpty else {
            errorMessage = "Please enter your username or email"
            showError = true
            return false
        }
        
        guard !password.isEmpty else {
            errorMessage = "Please enter your password"
            showError = true
            return false
        }
        
        guard password.count >= 6 else {
            errorMessage = "Password must be at least 6 characters"
            showError = true
            return false
        }
        
        return true
    }
}
'''
    
    file_path = viewmodels_dir / "LoginViewModel.swift"
    with open(file_path, 'w') as f:
        f.write(login_viewmodel)
    print(f"💪 Created PROFESSIONAL: LoginViewModel.swift ({len(login_viewmodel)} chars)")

# =============================================================================
# EXECUTION - VIEWMODEL FOCUS ONLY
# =============================================================================

if __name__ == "__main__":
    print("🏗️  iOS LOGIN VIEWMODEL - MVVM IMPLEMENTATION!")
    print("=" * 65)
    print("🎯 MISSION: Create ViewModel layer connecting UI to NetworkManager")
    print("=" * 65)
    
    # Create ViewModel-focused crew
    viewmodel_crew = Crew(
        agents=[mvvm_architect, state_manager, networking_integrator],
        tasks=[viewmodel_architecture_task, state_management_task, networking_integration_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        # Execute ViewModel creation
        result = viewmodel_crew.kickoff()
        
        # Create ViewModel files
        files_created = create_viewmodel_files(result)
        
        print("\n" + "=" * 65)
        print("🏗️  LOGIN VIEWMODEL RESULTS:")
        print("📋 ViewModel Files Created:")
        for filename in files_created:
            print(f"   ✅ {filename}")
        print("=" * 65)
        
        if len(files_created) >= 1:
            print("🎉 SUCCESS! Login ViewModel created!")
            print("💡 Next Phase: JWT storage integration with AuthManager")
        else:
            print("⚠️  No ViewModel files created - check agent output")
            
    except Exception as e:
        print(f"\n💥 VIEWMODEL CREATION FAILED: {str(e)}")

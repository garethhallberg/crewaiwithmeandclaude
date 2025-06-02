#!/usr/bin/env python3
"""
iOS Login UI - SWIFTUI SCREEN ONLY
Build a professional login screen with username/password fields!
NO PLACEHOLDER VIEWS! NO EMPTY FORMS! REAL SWIFTUI COMPONENTS!
"""

import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process

# Set working directory
ios_project_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone"
main_app_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterClone"

# =============================================================================
# UI-FOCUSED AGENTS - LOGIN SCREEN SPECIALISTS
# =============================================================================

swiftui_designer = Agent(
    role='Senior SwiftUI Designer (UI Perfectionist)',
    goal='Create a beautiful, professional login screen using SwiftUI best practices',
    backstory="""You are a SwiftUI expert who creates pixel-perfect user interfaces. 
    You know all the latest SwiftUI modifiers, state management patterns, and design principles.
    Your login screens are so polished that users actually want to log in. 
    You never submit placeholder views or empty forms - every component is fully functional.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

form_specialist = Agent(
    role='Form Input Specialist (UX Master)',
    goal='Create intuitive, user-friendly form inputs with proper validation and feedback',
    backstory="""You specialize in creating forms that users love to fill out. 
    You know exactly how to handle text field states, validation, keyboard types, and accessibility.
    Your forms have proper focus management, clear error states, and smooth user interactions.
    You make login forms that actually work on real devices.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

layout_architect = Agent(
    role='Layout Architect (Visual Perfectionist)',
    goal='Design responsive, beautiful layouts that work on all iOS devices',
    backstory="""You are obsessed with perfect layouts that look amazing on every iPhone and iPad.
    You understand spacing, typography, color schemes, and visual hierarchy.
    Your layouts are responsive, accessible, and follow Apple's Human Interface Guidelines.
    Empty screens and placeholder layouts are your worst nightmare.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

# =============================================================================
# SPECIFIC UI TASKS - NO VAGUE REQUIREMENTS
# =============================================================================

login_design_task = Task(
    description="""
    DESIGN THE COMPLETE LOGIN SCREEN SPECIFICATION
    
    **MANDATORY REQUIREMENTS:**
    
    1. **Screen Structure:**
       - App logo/title at top
       - Username text field
       - Password secure text field  
       - Login button
       - "Create Account" link/button
       - Proper spacing and alignment
    
    2. **Visual Design:**
       - Professional color scheme
       - Consistent typography
       - Proper padding and margins
       - Visual hierarchy (title > fields > button)
       - iOS-appropriate styling
    
    3. **Input Field Specifications:**
       - Username: email keyboard type, autocorrect off
       - Password: secure field, proper keyboard
       - Clear field borders and labels
       - Focus states and transitions
    
    4. **Button Design:**
       - Primary action styling for login
       - Disabled state when fields empty
       - Loading state capability
       - Proper touch targets
    
    5. **Layout Requirements:**
       - Responsive design (iPhone/iPad)
       - Safe area handling
       - Keyboard avoidance
       - Portrait/landscape support
    
    **DELIVERABLE:**
    Complete design specification with exact component hierarchy and styling details.
    """,
    expected_output="Detailed login screen design specification with all visual and interaction requirements",
    agent=swiftui_designer
)

form_implementation_task = Task(
    description="""
    IMPLEMENT FORM INPUTS AND STATE MANAGEMENT
    
    **FORM REQUIREMENTS:**
    
    1. **Text Field Implementation:**
       - @State variables for username and password
       - Proper TextField and SecureField usage
       - Custom styling and modifiers
       - Placeholder text and labels
    
    2. **Input Validation:**
       - Real-time field validation
       - Visual feedback for errors
       - Enable/disable login button based on field state
       - Clear validation messages
    
    3. **Keyboard Handling:**
       - Appropriate keyboard types
       - Return key navigation
       - Dismiss keyboard on tap outside
       - Smooth keyboard animations
    
    4. **State Management:**
       - Form submission states
       - Loading indicators
       - Error message display
       - Success feedback
    
    5. **Accessibility:**
       - VoiceOver support
       - Proper labels and hints
       - Focus management
       - Dynamic type support
    
    **TECHNICAL REQUIREMENTS:**
    - Use @State for local form state
    - Implement proper SwiftUI bindings
    - Handle form submission preparation
    - Include form reset functionality
    
    **DELIVERABLE:**
    Complete form implementation with all input handling and state management.
    """,
    expected_output="Fully functional form inputs with proper state management and validation",
    agent=form_specialist,
    depends_on=[login_design_task]
)

layout_implementation_task = Task(
    description="""
    CREATE THE COMPLETE LOGIN SCREEN LAYOUT
    
    **LAYOUT IMPLEMENTATION:**
    
    Create complete SwiftUI view file: LoginView.swift
    
    **FILE LOCATION:** /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterClone/Views/
    
    **MANDATORY COMPONENTS:**
    
    1. **Main Container:**
       - VStack with proper spacing
       - ScrollView for keyboard handling
       - Safe area considerations
       - Background styling
    
    2. **Header Section:**
       - App logo or title
       - Welcome message
       - Proper typography hierarchy
    
    3. **Form Section:**
       - Username TextField with:
         * Email keyboard type
         * Autocorrect disabled
         * Custom border styling
         * Placeholder: "Username or Email"
       - Password SecureField with:
         * Secure text entry
         * Custom border styling  
         * Placeholder: "Password"
    
    4. **Action Section:**
       - Login Button with:
         * Primary button styling
         * Loading state support
         * Disabled state when fields empty
         * Action handler ready
       - "Create Account" link
    
    5. **Error Display:**
       - Alert or text for error messages
       - Clear error state styling
       - Dismissible error handling
    
    **STYLING REQUIREMENTS:**
    - Consistent padding (16pt standard)
    - Rounded corners on inputs (8pt radius)
    - Primary color for buttons
    - Secondary color for links
    - Proper font weights and sizes
    
    **OUTPUT FORMAT:**
    ```swift
    // FILE: LoginView.swift
    import SwiftUI
    
    struct LoginView: View {
        @State private var username: String = ""
        @State private var password: String = ""
        @State private var isLoading: Bool = false
        @State private var errorMessage: String = ""
        @State private var showError: Bool = false
        
        var body: some View {
            // COMPLETE IMPLEMENTATION HERE
        }
    }
    
    struct LoginView_Previews: PreviewProvider {
        static var previews: some View {
            LoginView()
        }
    }
    ```
    
    EVERY COMPONENT MUST BE FULLY IMPLEMENTED! NO PLACEHOLDER VIEWS!
    """,
    expected_output="Complete LoginView.swift file with full implementation",
    agent=layout_architect,
    depends_on=[form_implementation_task]
)

# =============================================================================
# FILE CREATION - UI VIEWS ONLY
# =============================================================================

def create_login_ui_files(crew_result):
    """Extract and create UI files - focus on SwiftUI views only"""
    
    print("\n📱 CREATING LOGIN UI COMPONENTS!")
    
    views_dir = Path(main_app_path) / "Views"
    views_dir.mkdir(exist_ok=True)
    
    result_text = str(crew_result)
    
    # Save debug output
    debug_file = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai") / "login_ui_debug.txt"
    with open(debug_file, 'w') as f:
        f.write(result_text)
    print(f"🔍 Debug output: login_ui_debug.txt")
    
    # Extract Swift UI files
    import re
    pattern = r'// FILE: ([^\n]+\.swift)\n([\s\S]*?)(?=// FILE:|$)'
    matches = re.findall(pattern, result_text, re.MULTILINE | re.DOTALL)
    
    print(f"📝 Found {len(matches)} Swift UI files")
    
    files_created = []
    
    for filename, code_content in matches:
        filename = filename.strip()
        code_content = code_content.strip()
        
        # Clean up code blocks
        code_content = re.sub(r'^```swift\n?', '', code_content, flags=re.MULTILINE)
        code_content = re.sub(r'^```\n?', '', code_content, flags=re.MULTILINE)
        code_content = code_content.strip()
        
        # Validate this is substantial UI code
        if len(code_content) < 300:  # UI views should be substantial
            print(f"⚠️  {filename} too short ({len(code_content)} chars) - might be empty")
            continue
            
        # Check for actual SwiftUI components
        if 'struct' not in code_content or 'View' not in code_content:
            print(f"⚠️  {filename} doesn't contain SwiftUI View - might not be a real UI file")
            continue
        
        file_path = views_dir / filename
        
        try:
            with open(file_path, 'w') as f:
                f.write(code_content)
            
            print(f"✅ Created: {filename} ({len(code_content)} chars)")
            files_created.append(filename)
            
            # Validate UI components
            ui_components = []
            if 'TextField' in code_content:
                ui_components.append('TextField')
            if 'SecureField' in code_content:
                ui_components.append('SecureField')
            if 'Button' in code_content:
                ui_components.append('Button')
            if 'VStack' in code_content or 'HStack' in code_content:
                ui_components.append('Layout')
            
            if ui_components:
                print(f"   🎨 Contains: {', '.join(ui_components)}")
            
        except Exception as e:
            print(f"❌ Failed to create {filename}: {str(e)}")
    
    # Create professional fallback if agents failed
    if len(files_created) == 0:
        print("\n🔥 AGENTS FAILED! Creating professional fallback UI...")
        create_professional_login_ui(views_dir)
        files_created.append("LoginView.swift")
    
    return files_created

def create_professional_login_ui(views_dir):
    """Create professional login UI as fallback"""
    
    login_view = '''import SwiftUI

struct LoginView: View {
    @State private var username: String = ""
    @State private var password: String = ""
    @State private var isLoading: Bool = false
    @State private var errorMessage: String = ""
    @State private var showError: Bool = false
    
    private var isFormValid: Bool {
        !username.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty &&
        !password.isEmpty
    }
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 32) {
                    // Header Section
                    VStack(spacing: 16) {
                        Image(systemName: "bird.fill")
                            .font(.system(size: 60))
                            .foregroundColor(.blue)
                        
                        Text("Twitter Clone")
                            .font(.largeTitle)
                            .fontWeight(.bold)
                        
                        Text("Sign in to continue")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    .padding(.top, 40)
                    
                    // Form Section
                    VStack(spacing: 20) {
                        // Username Field
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Username or Email")
                                .font(.subheadline)
                                .fontWeight(.medium)
                            
                            TextField("Enter your username or email", text: $username)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                                .keyboardType(.emailAddress)
                                .autocorrectionDisabled()
                                .textInputAutocapitalization(.never)
                        }
                        
                        // Password Field
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Password")
                                .font(.subheadline)
                                .fontWeight(.medium)
                            
                            SecureField("Enter your password", text: $password)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                        }
                    }
                    
                    // Action Section
                    VStack(spacing: 16) {
                        Button(action: loginAction) {
                            HStack {
                                if isLoading {
                                    ProgressView()
                                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                                        .scaleEffect(0.8)
                                }
                                Text(isLoading ? "Signing In..." : "Sign In")
                                    .fontWeight(.semibold)
                            }
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(isFormValid ? Color.blue : Color.gray)
                            .foregroundColor(.white)
                            .cornerRadius(8)
                        }
                        .disabled(!isFormValid || isLoading)
                        
                        Button(action: createAccountAction) {
                            Text("Create Account")
                                .fontWeight(.medium)
                                .foregroundColor(.blue)
                        }
                    }
                    
                    Spacer()
                }
                .padding(.horizontal, 24)
            }
            .navigationBarHidden(true)
            .alert("Error", isPresented: $showError) {
                Button("OK") { }
            } message: {
                Text(errorMessage)
            }
        }
    }
    
    private func loginAction() {
        guard isFormValid else { return }
        
        isLoading = true
        errorMessage = ""
        
        // TODO: Implement actual login logic
        // This will be connected to AuthManager in next phase
        
        // Simulate network delay for now
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
            isLoading = false
            // Temporary feedback
            print("Login attempted with username: \\(username)")
        }
    }
    
    private func createAccountAction() {
        // TODO: Navigate to registration screen
        print("Create account tapped")
    }
}

struct LoginView_Previews: PreviewProvider {
    static var previews: some View {
        LoginView()
            .previewDevice("iPhone 14")
        
        LoginView()
            .previewDevice("iPhone SE (3rd generation)")
            .previewDisplayName("iPhone SE")
    }
}
'''
    
    file_path = views_dir / "LoginView.swift"
    with open(file_path, 'w') as f:
        f.write(login_view)
    print(f"💪 Created PROFESSIONAL: LoginView.swift ({len(login_view)} chars)")

# =============================================================================
# EXECUTION - UI FOCUS ONLY
# =============================================================================

if __name__ == "__main__":
    print("📱 iOS LOGIN UI - SWIFTUI SCREEN CREATION!")
    print("=" * 60)
    print("🎨 MISSION: Create beautiful, functional login screen")
    print("=" * 60)
    
    # Create UI-focused crew
    login_ui_crew = Crew(
        agents=[swiftui_designer, form_specialist, layout_architect],
        tasks=[login_design_task, form_implementation_task, layout_implementation_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        # Execute UI creation
        result = login_ui_crew.kickoff()
        
        # Create UI files
        files_created = create_login_ui_files(result)
        
        print("\n" + "=" * 60)
        print("📱 LOGIN UI RESULTS:")
        print("📋 UI Files Created:")
        for filename in files_created:
            print(f"   ✅ {filename}")
        print("=" * 60)
        
        if len(files_created) >= 1:
            print("🎉 SUCCESS! Login UI screen created!")
            print("💡 Next: Connect to authentication logic")
        else:
            print("⚠️  No UI files created - check agent output")
            
    except Exception as e:
        print(f"\n💥 UI CREATION FAILED: {str(e)}")

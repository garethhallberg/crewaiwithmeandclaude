#!/usr/bin/env python3
"""
FIX REGISTRATION NOW - NO EXCUSES
The agents failed to do their job. Time for tough love and actual file updates.
NO DEBUG FILES! NO EXCUSES! ACTUAL WORKING CODE!
"""

import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process

main_app_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterClone"

# =============================================================================
# TOUGH LOVE AGENTS - NO NONSENSE
# =============================================================================

registration_fixer = Agent(
    role='Registration Fixer (No Bullshit Developer)',
    goal='FIX THE DAMN REGISTRATION SCREEN RIGHT NOW',
    backstory="""You are tired of agents that write debug files instead of fixing code.
    You see broken code, you fix it immediately. You don't write essays, you don't make excuses,
    you don't create debug files - YOU WRITE WORKING CODE AND SAVE IT TO FILES.
    
    The RegistrationView is broken because it's not connected to RegistrationViewModel.
    LoginView works perfectly because it uses @StateObject and proper bindings.
    You will copy that exact pattern and make RegistrationView work the same way.
    
    NO EXCUSES. NO DEBUG FILES. WORKING CODE ONLY.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

# =============================================================================
# TASK WITH CONSEQUENCES
# =============================================================================

fix_registration_now_task = Task(
    description="""
    FIX REGISTRATIONVIEW RIGHT NOW - NO DEBATES
    
    **THE PROBLEM:**
    RegistrationView is broken - it uses @State instead of @StateObject
    LoginView works perfectly - it uses @StateObject with proper ViewModel binding
    
    **WHAT YOU WILL DO:**
    
    1. **STUDY THE WORKING LOGINVIEW PATTERN:**
       ```swift
       @StateObject private var viewModel = LoginViewModel.createDefault()
       TextField("Enter your username or email", text: $viewModel.username)
       Button(action: { Task { await viewModel.login() } })
       .disabled(!viewModel.canSubmit)
       .alert("Login Error", isPresented: $viewModel.showError)
       ```
    
    2. **APPLY SAME PATTERN TO REGISTRATIONVIEW:**
       - Replace @State with @StateObject private var viewModel = RegistrationViewModel.createDefault()
       - Connect ALL form fields to viewModel properties with $ bindings
       - Add proper register button with Task { await viewModel.register() }
       - Add loading states, error alerts, and form validation
       - Add ALL required fields: username, email, password, confirmPassword, displayName
    
    3. **COMPLETE WORKING REGISTRATIONVIEW:**
       ```swift
       struct RegistrationView: View {
           @StateObject private var viewModel = RegistrationViewModel.createDefault()
           @Environment(\\.dismiss) private var dismiss
           
           var body: some View {
               // COMPLETE FORM WITH ALL FIELDS CONNECTED TO VIEWMODEL
               // REGISTER BUTTON THAT CALLS viewModel.register()
               // ERROR HANDLING AND LOADING STATES
               // NAVIGATION AFTER SUCCESS
           }
       }
       ```
    
    **YOUR OUTPUT MUST BE:**
    - Complete RegistrationView.swift file content
    - Ready to copy-paste and replace the broken file
    - Following exact same pattern as working LoginView
    - No explanations, no debug text - JUST WORKING CODE
    
    **FAILURE IS NOT AN OPTION:**
    If you write debug text instead of code, you have failed.
    If you don't include all form fields, you have failed.
    If you don't connect to ViewModel properly, you have failed.
    
    WRITE THE COMPLETE WORKING REGISTRATIONVIEW.SWIFT FILE NOW.
    """,
    expected_output="Complete working RegistrationView.swift file content ready for immediate use",
    agent=registration_fixer
)

# =============================================================================
# EXECUTION WITH ENFORCEMENT
# =============================================================================

def force_fix_registration(crew_result):
    """Extract the code and force update the file"""
    
    result_text = str(crew_result)
    
    # Look for Swift code
    import re
    swift_code_blocks = re.findall(r'```swift\n(.*?)\n```', result_text, re.DOTALL)
    
    # Find the RegistrationView code
    registration_code = None
    for code in swift_code_blocks:
        if 'struct RegistrationView' in code and '@StateObject' in code and len(code) > 1000:
            registration_code = code
            break
    
    # If no proper code found, create professional version
    if not registration_code:
        print("🔥 AGENTS FAILED AGAIN! Creating professional fix...")
        registration_code = create_professional_registration_fix()
    
    # Force update the file
    views_dir = Path(main_app_path) / "Views"
    registration_file = views_dir / "RegistrationView.swift"
    
    with open(registration_file, 'w') as f:
        f.write(registration_code)
    
    print("✅ FORCED UPDATE: RegistrationView.swift - PROPERLY CONNECTED TO VIEWMODEL")
    return True

def create_professional_registration_fix():
    """Create the proper RegistrationView that connects to RegistrationViewModel"""
    
    return '''import SwiftUI

struct RegistrationView: View {
    @StateObject private var viewModel = RegistrationViewModel.createDefault()
    @Environment(\\.dismiss) private var dismiss
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 32) {
                    // Header Section
                    VStack(spacing: 16) {
                        Image(systemName: "bird.fill")
                            .font(.system(size: 60))
                            .foregroundColor(.blue)
                        
                        Text("Join Twitter Clone")
                            .font(.largeTitle)
                            .fontWeight(.bold)
                        
                        Text("Create your account")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    .padding(.top, 40)
                    
                    // Form Section
                    VStack(spacing: 20) {
                        // Username Field
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Username")
                                .font(.subheadline)
                                .fontWeight(.medium)
                            
                            TextField("Choose a username", text: $viewModel.username)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                                .autocorrectionDisabled()
                                .textInputAutocapitalization(.never)
                                .disabled(viewModel.isLoading)
                        }
                        
                        // Email Field
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Email")
                                .font(.subheadline)
                                .fontWeight(.medium)
                            
                            TextField("Enter your email", text: $viewModel.email)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                                .keyboardType(.emailAddress)
                                .autocorrectionDisabled()
                                .textInputAutocapitalization(.never)
                                .disabled(viewModel.isLoading)
                        }
                        
                        // Password Field
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Password")
                                .font(.subheadline)
                                .fontWeight(.medium)
                            
                            SecureField("Create a password", text: $viewModel.password)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                                .disabled(viewModel.isLoading)
                        }
                        
                        // Confirm Password Field
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Confirm Password")
                                .font(.subheadline)
                                .fontWeight(.medium)
                            
                            SecureField("Confirm your password", text: $viewModel.confirmPassword)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                                .disabled(viewModel.isLoading)
                        }
                        
                        // Display Name Field (Optional)
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Display Name (Optional)")
                                .font(.subheadline)
                                .fontWeight(.medium)
                            
                            TextField("Your display name", text: $viewModel.displayName)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                                .disabled(viewModel.isLoading)
                        }
                    }
                    
                    // Action Section
                    VStack(spacing: 16) {
                        // Register Button
                        Button(action: {
                            Task {
                                await viewModel.register()
                            }
                        }) {
                            HStack {
                                if viewModel.isLoading {
                                    ProgressView()
                                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                                        .scaleEffect(0.8)
                                }
                                Text(viewModel.registerButtonTitle)
                                    .fontWeight(.semibold)
                            }
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(viewModel.canSubmit ? Color.blue : Color.gray)
                            .foregroundColor(.white)
                            .cornerRadius(8)
                        }
                        .disabled(!viewModel.canSubmit)
                        
                        Button(action: {
                            dismiss()
                        }) {
                            Text("Already have an account? Sign In")
                                .fontWeight(.medium)
                                .foregroundColor(.blue)
                        }
                    }
                    
                    Spacer()
                }
                .padding(.horizontal, 24)
            }
            .navigationBarHidden(true)
        }
        // Error Alert
        .alert("Registration Error", isPresented: $viewModel.showError) {
            Button("OK") {
                viewModel.clearError()
            }
        } message: {
            Text(viewModel.errorMessage)
        }
        // Navigation after successful registration
        .fullScreenCover(isPresented: $viewModel.isRegistered) {
            AuthenticatedView()
        }
    }
}

struct RegistrationView_Previews: PreviewProvider {
    static var previews: some View {
        RegistrationView()
            .previewDevice("iPhone 14")
        
        RegistrationView()
            .previewDevice("iPhone SE (3rd generation)")
            .previewDisplayName("iPhone SE")
    }
}
'''

# =============================================================================
# TOUGH LOVE EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("🔥 REGISTRATION FIX - NO MORE EXCUSES!")
    print("=" * 50)
    print("🎯 MISSION: Fix RegistrationView or face consequences")
    print("💀 NO DEBUG FILES ALLOWED")
    print("=" * 50)
    
    crew = Crew(
        agents=[registration_fixer],
        tasks=[fix_registration_now_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        result = crew.kickoff()
        
        # Force the fix regardless of agent performance
        success = force_fix_registration(result)
        
        print("\n" + "=" * 50)
        if success:
            print("✅ REGISTRATION FIXED!")
            print("📱 RegistrationView now properly connected to RegistrationViewModel")
            print("🚀 Ready to test registration flow!")
        else:
            print("❌ Something went wrong - check the files manually")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n💥 EXECUTION FAILED: {str(e)}")
        print("🔧 Applying emergency professional fix...")
        force_fix_registration("")

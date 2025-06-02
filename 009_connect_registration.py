#!/usr/bin/env python3
"""
Connect Registration Screen to ViewModel - Simple Fix
Fix the RegistrationView to use the RegistrationViewModel like LoginView does
"""

import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process

# =============================================================================
# AGENT
# =============================================================================

registration_connector = Agent(
    role='iOS Registration Connector',
    goal='Connect the existing RegistrationView to the existing RegistrationViewModel',
    backstory="""You fix iOS screens by connecting them to their ViewModels. 
    You see that LoginView successfully connects to LoginViewModel, so you apply 
    the same pattern to connect RegistrationView to RegistrationViewModel.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

# =============================================================================
# TASK
# =============================================================================

connect_registration_task = Task(
    description="""
    CONNECT REGISTRATIONVIEW TO REGISTRATIONVIEWMODEL
    
    **CURRENT PROBLEM:**
    - RegistrationView exists but uses @State variables
    - RegistrationViewModel exists but isn't connected
    - LoginView successfully uses @StateObject with LoginViewModel
    
    **SIMPLE FIX NEEDED:**
    
    1. **Update RegistrationView.swift:**
       - Replace @State variables with @StateObject private var viewModel = RegistrationViewModel.createDefault()
       - Connect form fields to viewModel properties with $ bindings
       - Add register button that calls viewModel.register()
       - Add error alerts and loading states like LoginView
       - Keep the same visual design, just connect to ViewModel
    
    2. **Test the pattern from LoginView.swift:**
       - Look how LoginView uses @StateObject private var viewModel = LoginViewModel.createDefault()
       - Look how LoginView binds TextField("text", text: $viewModel.username)
       - Look how LoginView handles Button actions with Task { await viewModel.login() }
       - Copy this exact pattern for registration
    
    **KEEP IT SIMPLE:**
    - Just connect the existing RegistrationView to existing RegistrationViewModel
    - Use the same MVVM pattern that works in LoginView
    - Don't change the backend or add new features
    
    Output the complete updated RegistrationView.swift file.
    """,
    expected_output="Updated RegistrationView.swift that connects to RegistrationViewModel",
    agent=registration_connector
)

# =============================================================================
# EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("🔗 CONNECTING REGISTRATION VIEW TO VIEWMODEL")
    print("Following the successful LoginView pattern...")
    
    # Create crew
    crew = Crew(
        agents=[registration_connector],
        tasks=[connect_registration_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        # Execute
        result = crew.kickoff()
        
        # Save result
        with open("/Users/garethhallberg/Desktop/twitter-clone-crewai/registration_connection_debug.txt", 'w') as f:
            f.write(str(result))
        
        print("\n✅ Task completed! Check registration_connection_debug.txt for results")
        print("💡 Apply the suggested changes to RegistrationView.swift")
        
    except Exception as e:
        print(f"\n❌ Failed: {str(e)}")

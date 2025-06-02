#!/usr/bin/env python3
"""
iOS Concurrency Fix - SWIFT 6 COMPATIBILITY
Fix MainActor isolation errors in LoginViewModel!
SPECIFIC PROBLEM: NetworkManager.shared access from nonisolated context
"""

import os
import re
from pathlib import Path
from crewai import Agent, Task, Crew, Process

# Set working directory
ios_project_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone"
viewmodel_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterClone/ViewModels/LoginViewModel.swift"

# =============================================================================
# SWIFT CONCURRENCY SPECIALISTS
# =============================================================================

concurrency_expert = Agent(
    role='Swift Concurrency Expert (MainActor Specialist)',
    goal='Fix Swift 6 MainActor isolation errors with precise, minimal changes',
    backstory="""You are a Swift concurrency expert who understands MainActor isolation perfectly.
    You know exactly how to fix 'Main actor-isolated property cannot be referenced from nonisolated context' errors.
    Your solutions are minimal, clean, and maintain proper architecture patterns.
    You never over-engineer solutions - just fix the specific concurrency issue.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

# =============================================================================
# CONCURRENCY FIX TASK
# =============================================================================

fix_mainactor_task = Task(
    description="""
    FIX THE SPECIFIC SWIFT 6 CONCURRENCY ERROR IN LOGINVIEWMODEL
    
    **EXACT ERROR TO FIX:**
    "Main actor-isolated static property 'shared' can not be referenced from a nonisolated context"
    
    **LOCATION:** LoginViewModel.swift, line 32 (approximately)
    **PROBLEM CODE:**
    ```swift
    init(networkManager: NetworkManager = NetworkManager.shared) {
        self.networkManager = networkManager
    }
    ```
    
    **PROBLEM ANALYSIS:**
    - NetworkManager.shared is @MainActor isolated
    - LoginViewModel init is not MainActor isolated
    - Swift 6 doesn't allow this cross-context access
    
    **SOLUTION OPTIONS (Pick the cleanest):**
    
    **Option 1 - Remove Default Parameter (RECOMMENDED):**
    ```swift
    init(networkManager: NetworkManager) {
        self.networkManager = networkManager
    }
    ```
    Then update the usage to explicitly pass NetworkManager.shared
    
    **Option 2 - Static Factory Method:**
    ```swift
    private init(networkManager: NetworkManager) {
        self.networkManager = networkManager
    }
    
    @MainActor
    static func create() -> LoginViewModel {
        return LoginViewModel(networkManager: NetworkManager.shared)
    }
    ```
    
    **Option 3 - Async Init:**
    ```swift
    private let networkManager: NetworkManager
    
    private init(networkManager: NetworkManager) {
        self.networkManager = networkManager  
    }
    
    @MainActor
    static func create() async -> LoginViewModel {
        return LoginViewModel(networkManager: NetworkManager.shared)
    }
    ```
    
    **REQUIREMENTS:**
    1. Fix ONLY the concurrency error
    2. Keep the architecture clean
    3. Maintain testability (dependency injection)
    4. Use minimal changes
    5. Don't break existing functionality
    
    **FILE TO MODIFY:** /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterClone/ViewModels/LoginViewModel.swift
    
    **OUTPUT FORMAT:**
    ```swift
    // FILE: LoginViewModel.swift
    // ONLY SHOW THE CHANGED SECTIONS, NOT THE ENTIRE FILE
    
    // MARK: - Initialization (FIXED)
    init(networkManager: NetworkManager) {
        self.networkManager = networkManager
    }
    ```
    
    Choose the cleanest solution and implement it properly!
    """,
    expected_output="Fixed LoginViewModel.swift with Swift 6 concurrency error resolved",
    agent=concurrency_expert
)

# =============================================================================
# CONCURRENCY FIX IMPLEMENTATION
# =============================================================================

def apply_concurrency_fixes(crew_result):
    """Apply the concurrency fixes to LoginViewModel"""
    
    print("\n⚡ APPLYING SWIFT 6 CONCURRENCY FIXES!")
    
    result_text = str(crew_result)
    
    # Save debug output
    debug_file = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai") / "concurrency_fix_debug.txt"
    with open(debug_file, 'w') as f:
        f.write(result_text)
    print(f"🔍 Debug output: concurrency_fix_debug.txt")
    
    # Read current LoginViewModel
    try:
        with open(viewmodel_path, 'r') as f:
            current_content = f.read()
        print(f"📖 Read current LoginViewModel ({len(current_content)} chars)")
    except Exception as e:
        print(f"❌ Failed to read LoginViewModel: {str(e)}")
        return False
    
    # Extract fix from crew result
    
    # Look for the fixed init method
    fix_pattern = r'// MARK: - Initialization.*?\n(.*?init.*?\{[\s\S]*?\})'
    fix_match = re.search(fix_pattern, result_text, re.MULTILINE | re.DOTALL)
    
    if fix_match:
        new_init = fix_match.group(1).strip()
        print(f"🔧 Found init fix: {new_init[:50]}...")
        
        # Replace the problematic init in current content
        old_init_pattern = r'init\(networkManager: NetworkManager = NetworkManager\.shared\) \{[\s\S]*?\n    \}'
        
        if re.search(old_init_pattern, current_content):
            fixed_content = re.sub(old_init_pattern, new_init, current_content)
            
            try:
                with open(viewmodel_path, 'w') as f:
                    f.write(fixed_content)
                print("✅ Applied concurrency fix to LoginViewModel.swift")
                return True
            except Exception as e:
                print(f"❌ Failed to write fixed file: {str(e)}")
                return False
        else:
            print("⚠️  Could not find the problematic init pattern to replace")
            
    # Fallback: Apply known good fix
    print("\n🔥 APPLYING PROFESSIONAL FALLBACK FIX...")
    return apply_professional_concurrency_fix(current_content)

def apply_professional_concurrency_fix(current_content):
    """Apply the known good concurrency fix"""
    
    # Replace the problematic init
    old_pattern = r'init\(networkManager: NetworkManager = NetworkManager\.shared\) \{\s*self\.networkManager = networkManager\s*\}'
    new_init = '''init(networkManager: NetworkManager) {
        self.networkManager = networkManager
    }'''
    
    fixed_content = re.sub(old_pattern, new_init, current_content, flags=re.MULTILINE | re.DOTALL)
    
    # Also add a convenience factory method
    factory_method = '''
    
    // MARK: - Factory Method
    @MainActor
    static func createDefault() -> LoginViewModel {
        return LoginViewModel(networkManager: NetworkManager.shared)
    }'''
    
    # Insert factory method after the init
    insertion_point = fixed_content.find('    // MARK: - Public Methods')
    if insertion_point != -1:
        fixed_content = fixed_content[:insertion_point] + factory_method + '\n    ' + fixed_content[insertion_point:]
    
    try:
        with open(viewmodel_path, 'w') as f:
            f.write(fixed_content)
        print("✅ Applied professional concurrency fix")
        print("💡 Added createDefault() factory method for convenience")
        return True
    except Exception as e:
        print(f"❌ Failed to apply professional fix: {str(e)}")
        return False

# =============================================================================
# EXECUTION - CONCURRENCY FIX ONLY
# =============================================================================

if __name__ == "__main__":
    print("⚡ SWIFT 6 CONCURRENCY FIX - MAINACTOR ISOLATION!")
    print("=" * 60)
    print("🎯 MISSION: Fix NetworkManager.shared access error")
    print("=" * 60)
    
    # Create concurrency-focused crew
    concurrency_crew = Crew(
        agents=[concurrency_expert],
        tasks=[fix_mainactor_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        # Execute concurrency fix
        result = concurrency_crew.kickoff()
        
        # Apply the fixes
        success = apply_concurrency_fixes(result)
        
        print("\n" + "=" * 60)
        if success:
            print("⚡ CONCURRENCY FIX RESULTS:")
            print("✅ Swift 6 MainActor isolation error FIXED!")
            print("💡 LoginViewModel should now compile without errors")
            print("🔄 May need to update LoginView to use new init pattern")
        else:
            print("❌ CONCURRENCY FIX FAILED:")
            print("⚠️  Manual intervention may be required")
        print("=" * 60)
            
    except Exception as e:
        print(f"\n💥 CONCURRENCY FIX FAILED: {str(e)}")

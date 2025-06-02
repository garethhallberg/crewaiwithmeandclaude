#!/usr/bin/env python3
"""
iOS Mock Injection Fix - PROTOCOL-BASED DEPENDENCY INJECTION
Fix MockNetworkManager casting issue with proper architecture patterns!
SPECIFIC PROBLEM: Cannot cast MockNetworkManager to NetworkManager
SOLUTION: Protocol-based dependency injection
"""

import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process

# Set working directory
ios_project_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone"
main_app_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterClone"
test_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterCloneTests"

# =============================================================================
# DEPENDENCY INJECTION SPECIALISTS
# =============================================================================

protocol_architect = Agent(
    role='Protocol Architecture Expert (Dependency Injection Master)',
    goal='Design clean protocol-based dependency injection for testable architecture',
    backstory="""You are an expert in Swift protocol-oriented programming and dependency injection.
    You know exactly how to create protocols that enable mock injection for testing.
    Your protocol designs are clean, minimal, and enable perfect test isolation.
    You understand the difference between concrete types and protocol abstractions.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

# =============================================================================
# DEPENDENCY INJECTION FIX TASK
# =============================================================================

protocol_injection_task = Task(
    description="""
    FIX THE MOCK INJECTION ISSUE WITH PROTOCOL-BASED DEPENDENCY INJECTION
    
    **EXACT ERROR TO FIX:**
    "Cast from 'MockNetworkManager?' to unrelated type 'NetworkManager' always fails"
    
    **LOCATION:** LoginViewModelTests.swift, line 13
    **PROBLEM CODE:**
    ```swift
    viewModel = LoginViewModel(networkManager: mockNetworkManager as! NetworkManager)
    ```
    
    **ROOT CAUSE ANALYSIS:**
    - LoginViewModel expects concrete `NetworkManager` type
    - MockNetworkManager is unrelated class, cannot be cast to NetworkManager
    - Need protocol abstraction to enable dependency injection
    - Both real and mock should conform to same protocol
    
    **SOLUTION ARCHITECTURE:**
    
    **Step 1: Create NetworkManagerProtocol**
    Create file: /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterClone/Networking/NetworkManagerProtocol.swift
    
    ```swift
    // FILE: NetworkManagerProtocol.swift
    import Foundation
    
    protocol NetworkManagerProtocol {
        func request<T: Codable>(
            endpoint: APIEndpoint,
            responseType: T.Type,
            token: String?
        ) async throws -> T
    }
    ```
    
    **Step 2: Make NetworkManager conform to protocol**
    Update NetworkManager.swift to add protocol conformance:
    ```swift
    extension NetworkManager: NetworkManagerProtocol {
        // Already has the required method, just add conformance
    }
    ```
    
    **Step 3: Update LoginViewModel to use protocol**
    Change LoginViewModel dependency from concrete type to protocol:
    ```swift
    private let networkManager: NetworkManagerProtocol  // Changed from NetworkManager
    
    init(networkManager: NetworkManagerProtocol) {      // Changed parameter type
        self.networkManager = networkManager
    }
    ```
    
    **Step 4: Make MockNetworkManager conform to protocol**
    Update MockNetworkManager.swift:
    ```swift
    class MockNetworkManager: NetworkManagerProtocol {
        // Already has the required method, just add conformance
    }
    ```
    
    **Step 5: Fix test setup**
    Update LoginViewModelTests.swift:
    ```swift
    viewModel = LoginViewModel(networkManager: mockNetworkManager)  // No casting needed!
    ```
    
    **REQUIREMENTS:**
    
    1. **Minimal Protocol**: Only include methods that LoginViewModel actually uses
    2. **Clean Conformance**: No extra methods or properties in protocol
    3. **Backward Compatibility**: Don't break existing NetworkManager usage
    4. **Test Isolation**: MockNetworkManager should work perfectly with protocol
    5. **No Breaking Changes**: Existing code should continue working
    
    **FILES TO MODIFY:**
    1. CREATE: NetworkManagerProtocol.swift (new file)
    2. UPDATE: NetworkManager.swift (add conformance)
    3. UPDATE: LoginViewModel.swift (use protocol type)
    4. UPDATE: MockNetworkManager.swift (add conformance)
    5. UPDATE: LoginViewModelTests.swift (remove casting)
    
    **OUTPUT FORMAT - Show exact changes for each file:**
    ```swift
    // FILE: NetworkManagerProtocol.swift
    import Foundation
    
    protocol NetworkManagerProtocol {
        // COMPLETE PROTOCOL DEFINITION
    }
    ```
    
    ```swift
    // FILE: NetworkManager.swift - ADD THIS EXTENSION
    extension NetworkManager: NetworkManagerProtocol {
        // Protocol conformance (method already exists)
    }
    ```
    
    ```swift
    // FILE: LoginViewModel.swift - CHANGE THESE LINES
    private let networkManager: NetworkManagerProtocol  // Changed type
    
    init(networkManager: NetworkManagerProtocol) {      // Changed parameter
        self.networkManager = networkManager
    }
    ```
    
    Show ALL required changes for complete solution!
    """,
    expected_output="Complete protocol-based dependency injection solution with all file changes",
    agent=protocol_architect
)

# =============================================================================
# DEPENDENCY INJECTION IMPLEMENTATION
# =============================================================================

def apply_protocol_injection_fixes(crew_result):
    """Apply the protocol-based dependency injection fixes"""
    
    print("\n🔌 APPLYING PROTOCOL-BASED DEPENDENCY INJECTION FIXES!")
    
    result_text = str(crew_result)
    
    # Save debug output
    debug_file = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai") / "protocol_injection_debug.txt"
    with open(debug_file, 'w') as f:
        f.write(result_text)
    print(f"🔍 Debug output: protocol_injection_debug.txt")
    
    # Extract file changes from crew result
    import re
    file_pattern = r'// FILE: ([^\n]+\.swift)[\s\S]*?\n([\s\S]*?)(?=// FILE:|$)'
    file_matches = re.findall(file_pattern, result_text, re.MULTILINE | re.DOTALL)
    
    print(f"📝 Found {len(file_matches)} file modifications")
    
    changes_applied = []
    
    for filename, content in file_matches:
        filename = filename.strip()
        content = content.strip()
        
        # Clean up content
        content = re.sub(r'^```swift\n?', '', content, flags=re.MULTILINE)
        content = re.sub(r'^```\n?', '', content, flags=re.MULTILINE)
        content = content.strip()
        
        if len(content) < 50:  # Skip empty or minimal content
            continue
            
        if filename == "NetworkManagerProtocol.swift":
            success = create_network_manager_protocol(content)
            if success:
                changes_applied.append(filename)
        elif filename == "NetworkManager.swift":
            success = update_network_manager_conformance(content)
            if success:
                changes_applied.append(filename)
        elif filename == "LoginViewModel.swift":
            success = update_login_viewmodel_protocol(content)
            if success:
                changes_applied.append(filename)
        elif filename == "MockNetworkManager.swift":
            success = update_mock_network_manager_conformance(content)
            if success:
                changes_applied.append(filename)
        elif filename == "LoginViewModelTests.swift":
            success = fix_test_setup(content)
            if success:
                changes_applied.append(filename)
    
    # Apply professional fallback if agents didn't provide complete solution
    if len(changes_applied) < 3:
        print("\n🔥 APPLYING PROFESSIONAL FALLBACK SOLUTION...")
        apply_professional_protocol_injection()
        changes_applied = ["NetworkManagerProtocol.swift", "NetworkManager.swift", "LoginViewModel.swift", "MockNetworkManager.swift", "LoginViewModelTests.swift"]
    
    return changes_applied

def create_network_manager_protocol(content):
    """Create the NetworkManagerProtocol file"""
    networking_dir = Path(main_app_path) / "Networking"
    protocol_file = networking_dir / "NetworkManagerProtocol.swift"
    
    try:
        with open(protocol_file, 'w') as f:
            f.write(content)
        print(f"✅ Created: NetworkManagerProtocol.swift")
        return True
    except Exception as e:
        print(f"❌ Failed to create protocol: {str(e)}")
        return False

def update_network_manager_conformance(extension_content):
    """Add protocol conformance to NetworkManager"""
    network_manager_file = Path(main_app_path) / "Networking" / "NetworkManager.swift"
    
    try:
        with open(network_manager_file, 'r') as f:
            current_content = f.read()
        
        # Add the conformance extension
        updated_content = current_content + "\n\n" + extension_content
        
        with open(network_manager_file, 'w') as f:
            f.write(updated_content)
        
        print(f"✅ Updated: NetworkManager.swift with protocol conformance")
        return True
    except Exception as e:
        print(f"❌ Failed to update NetworkManager: {str(e)}")
        return False

def update_login_viewmodel_protocol(changes):
    """Update LoginViewModel to use protocol"""
    viewmodel_file = Path(main_app_path) / "ViewModels" / "LoginViewModel.swift"
    
    try:
        with open(viewmodel_file, 'r') as f:
            current_content = f.read()
        
        # Replace NetworkManager with NetworkManagerProtocol
        updated_content = current_content.replace(
            "private let networkManager: NetworkManager",
            "private let networkManager: NetworkManagerProtocol"
        ).replace(
            "init(networkManager: NetworkManager)",
            "init(networkManager: NetworkManagerProtocol)"
        )
        
        with open(viewmodel_file, 'w') as f:
            f.write(updated_content)
        
        print(f"✅ Updated: LoginViewModel.swift to use protocol")
        return True
    except Exception as e:
        print(f"❌ Failed to update LoginViewModel: {str(e)}")
        return False

def update_mock_network_manager_conformance(content):
    """Update MockNetworkManager to conform to protocol"""
    mock_file = Path(test_path) / "MockNetworkManager.swift"
    
    try:
        with open(mock_file, 'r') as f:
            current_content = f.read()
        
        # Add protocol conformance
        updated_content = current_content.replace(
            "class MockNetworkManager {",
            "class MockNetworkManager: NetworkManagerProtocol {"
        )
        
        with open(mock_file, 'w') as f:
            f.write(updated_content)
        
        print(f"✅ Updated: MockNetworkManager.swift with protocol conformance")
        return True
    except Exception as e:
        print(f"❌ Failed to update MockNetworkManager: {str(e)}")
        return False

def fix_test_setup(content):
    """Fix the test setup to remove casting"""
    test_file = Path(test_path) / "LoginViewModelTests.swift"
    
    try:
        with open(test_file, 'r') as f:
            current_content = f.read()
        
        # Remove the problematic casting
        updated_content = current_content.replace(
            "viewModel = LoginViewModel(networkManager: mockNetworkManager as! NetworkManager)",
            "viewModel = LoginViewModel(networkManager: mockNetworkManager)"
        )
        
        with open(test_file, 'w') as f:
            f.write(updated_content)
        
        print(f"✅ Updated: LoginViewModelTests.swift removed casting")
        return True
    except Exception as e:
        print(f"❌ Failed to fix test setup: {str(e)}")
        return False

def apply_professional_protocol_injection():
    """Apply professional protocol-based dependency injection solution"""
    
    # 1. Create NetworkManagerProtocol
    protocol_content = '''import Foundation

protocol NetworkManagerProtocol {
    func request<T: Codable>(
        endpoint: APIEndpoint,
        responseType: T.Type,
        token: String?
    ) async throws -> T
}
'''
    
    networking_dir = Path(main_app_path) / "Networking"
    protocol_file = networking_dir / "NetworkManagerProtocol.swift"
    with open(protocol_file, 'w') as f:
        f.write(protocol_content)
    print("💪 Created: NetworkManagerProtocol.swift")
    
    # 2. Add conformance to NetworkManager
    network_manager_file = networking_dir / "NetworkManager.swift"
    with open(network_manager_file, 'r') as f:
        current_content = f.read()
    
    conformance_extension = "\n\n// MARK: - Protocol Conformance\nextension NetworkManager: NetworkManagerProtocol {\n    // Already implements required methods\n}\n"
    updated_content = current_content + conformance_extension
    
    with open(network_manager_file, 'w') as f:
        f.write(updated_content)
    print("💪 Updated: NetworkManager.swift with protocol conformance")
    
    # 3. Update LoginViewModel
    viewmodel_file = Path(main_app_path) / "ViewModels" / "LoginViewModel.swift"
    with open(viewmodel_file, 'r') as f:
        current_content = f.read()
    
    updated_content = current_content.replace(
        "private let networkManager: NetworkManager",
        "private let networkManager: NetworkManagerProtocol"
    ).replace(
        "init(networkManager: NetworkManager)",
        "init(networkManager: NetworkManagerProtocol)"
    )
    
    with open(viewmodel_file, 'w') as f:
        f.write(updated_content)
    print("💪 Updated: LoginViewModel.swift to use protocol")
    
    # 4. Update MockNetworkManager
    mock_file = Path(test_path) / "MockNetworkManager.swift"
    with open(mock_file, 'r') as f:
        current_content = f.read()
    
    updated_content = current_content.replace(
        "class MockNetworkManager {",
        "class MockNetworkManager: NetworkManagerProtocol {"
    )
    
    with open(mock_file, 'w') as f:
        f.write(updated_content)
    print("💪 Updated: MockNetworkManager.swift with protocol conformance")
    
    # 5. Fix test setup
    test_file = Path(test_path) / "LoginViewModelTests.swift"
    with open(test_file, 'r') as f:
        current_content = f.read()
    
    updated_content = current_content.replace(
        "viewModel = LoginViewModel(networkManager: mockNetworkManager as! NetworkManager)",
        "viewModel = LoginViewModel(networkManager: mockNetworkManager)"
    )
    
    with open(test_file, 'w') as f:
        f.write(updated_content)
    print("💪 Fixed: LoginViewModelTests.swift removed casting")

# =============================================================================
# EXECUTION - PROTOCOL INJECTION FIX
# =============================================================================

if __name__ == "__main__":
    print("🔌 PROTOCOL-BASED DEPENDENCY INJECTION FIX!")
    print("=" * 65)
    print("🎯 MISSION: Fix MockNetworkManager casting with protocol abstraction")
    print("=" * 65)
    
    # Create protocol injection crew
    protocol_crew = Crew(
        agents=[protocol_architect],
        tasks=[protocol_injection_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        # Execute protocol injection fix
        result = protocol_crew.kickoff()
        
        # Apply the fixes
        changes_applied = apply_protocol_injection_fixes(result)
        
        print("\n" + "=" * 65)
        print("🔌 PROTOCOL INJECTION RESULTS:")
        print("📋 Files Modified:")
        for filename in changes_applied:
            print(f"   ✅ {filename}")
        print("=" * 65)
        
        if len(changes_applied) >= 3:
            print("🎉 SUCCESS! Protocol-based dependency injection implemented!")
            print("💡 LoginViewModelTests should now compile without casting errors")
            print("🔄 Both real and mock NetworkManager use same protocol")
        else:
            print("⚠️  Partial fix applied - check individual file updates")
            
    except Exception as e:
        print(f"\n💥 PROTOCOL INJECTION FIX FAILED: {str(e)}")

#!/usr/bin/env python3
"""
iOS LoginViewModel Unit Tests - COMPREHENSIVE TEST COVERAGE
Write thorough unit tests for LoginViewModel class!
NO EMPTY TEST METHODS! NO PLACEHOLDER TESTS! REAL VALIDATION!
"""

import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process

# Set working directory
ios_project_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone"
test_output_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterCloneTests"

# =============================================================================
# VIEWMODEL TESTING SPECIALISTS
# =============================================================================

viewmodel_test_architect = Agent(
    role='ViewModel Test Architect (Testing Strategy Expert)',
    goal='Design comprehensive test strategy for LoginViewModel covering all scenarios',
    backstory="""You are a testing expert who specializes in ViewModel unit testing.
    You understand MVVM patterns, @Published property testing, async method testing,
    and mock dependency injection. Your test strategies cover every possible state,
    edge case, and user interaction scenario.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

async_testing_specialist = Agent(
    role='Async Testing Specialist (Concurrency Expert)',
    goal='Write bulletproof async tests for login methods and state management',
    backstory="""You specialize in testing async Swift methods, @MainActor classes,
    and @Published property changes. You know exactly how to test async functions,
    handle expectations for property updates, and validate state transitions.
    Your async tests never have race conditions or flaky behavior.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

mock_networking_expert = Agent(
    role='Mock Networking Expert (Dependency Injection Master)',
    goal='Create perfect mock NetworkManager for isolated ViewModel testing',
    backstory="""You create mock objects that enable perfect isolation testing.
    Your NetworkManager mocks can simulate success responses, various error conditions,
    network timeouts, and invalid data. Your mocks are so realistic that ViewModels
    can't tell the difference from real networking calls.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

# =============================================================================
# VIEWMODEL TESTING TASKS
# =============================================================================

test_strategy_task = Task(
    description="""
    DESIGN COMPREHENSIVE LOGINVIEWMODEL TEST STRATEGY
    
    **TESTING SCENARIOS TO COVER:**
    
    1. **Initialization Tests:**
       - ViewModel initializes with correct default state
       - Dependency injection works properly
       - All @Published properties have expected initial values
    
    2. **Form Validation Tests:**
       - isFormValid computed property logic
       - canSubmit computed property logic
       - Empty username handling
       - Empty password handling
       - Password minimum length validation
       - Username whitespace trimming
    
    3. **Login Success Tests:**
       - Successful authentication flow
       - State transitions during login (loading → success)
       - AuthResponse parsing and handling
       - Success state property updates
       - JWT token extraction (for future integration)
    
    4. **Login Error Tests:**
       - Network connection failures
       - HTTP 401 (invalid credentials)
       - HTTP 500 (server errors)
       - JSON parsing errors
       - Invalid response handling
       - User-friendly error message generation
    
    5. **State Management Tests:**
       - @Published property change notifications
       - Loading state management
       - Error state handling and clearing
       - Form reset functionality
       - Async state transition validation
    
    6. **Edge Case Tests:**
       - Multiple rapid login attempts
       - Login during loading state
       - Form validation during network calls
       - Error handling during success
    
    **MOCK REQUIREMENTS:**
    - MockNetworkManager with configurable responses
    - Success response simulation (AuthResponse)
    - Error response simulation (NetworkError cases)
    - Async operation control
    
    **DELIVERABLE:**
    Complete test specification with exact test method names and scenarios.
    """,
    expected_output="Detailed LoginViewModel test strategy with all scenarios and mock requirements",
    agent=viewmodel_test_architect
)

mock_implementation_task = Task(
    description="""
    CREATE MOCK NETWORKMANAGER FOR VIEWMODEL TESTING
    
    **MOCK NETWORKMANAGER REQUIREMENTS:**
    
    Create MockNetworkManager.swift for testing LoginViewModel in isolation.
    
    **FILE LOCATION:** /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterCloneTests/
    
    **MOCK CAPABILITIES:**
    
    1. **Success Response Simulation:**
       - Return configurable AuthResponse
       - Simulate successful login with valid JWT
       - Return proper User data structure
    
    2. **Error Response Simulation:**
       - NetworkError.serverError(401) for invalid credentials
       - NetworkError.serverError(500) for server errors
       - NetworkError.requestFailed for network issues
       - NetworkError.decodingError for JSON problems
       - NetworkError.invalidResponse for malformed responses
    
    3. **Async Control:**
       - Configurable delay simulation
       - Immediate response capability
       - Timeout simulation
    
    4. **Request Validation:**
       - Capture last endpoint called
       - Validate request parameters
       - Track method call count
    
    **IMPLEMENTATION STRUCTURE:**
    ```swift
    // FILE: MockNetworkManager.swift
    import Foundation
    @testable import TwitterClone
    
    class MockNetworkManager {
        // Configuration properties
        var shouldSucceed: Bool = true
        var mockAuthResponse: AuthResponse?
        var mockError: NetworkError?
        var responseDelay: TimeInterval = 0
        
        // Tracking properties
        var lastEndpoint: APIEndpoint?
        var callCount: Int = 0
        
        func request<T: Codable>(
            endpoint: APIEndpoint,
            responseType: T.Type,
            token: String? = nil
        ) async throws -> T {
            // COMPLETE IMPLEMENTATION
        }
    }
    ```
    
    **MOCK BEHAVIOR:**
    - If shouldSucceed = true: return mockAuthResponse
    - If shouldSucceed = false: throw mockError
    - Always track endpoint and increment callCount
    - Apply responseDelay if configured
    
    NO EMPTY METHODS! COMPLETE MOCK IMPLEMENTATION REQUIRED!
    """,
    expected_output="Complete MockNetworkManager.swift for ViewModel testing",
    agent=mock_networking_expert,
    depends_on=[test_strategy_task]
)

viewmodel_tests_implementation = Task(
    description="""
    IMPLEMENT COMPREHENSIVE LOGINVIEWMODEL UNIT TESTS
    
    **TEST FILE TO CREATE:** /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterCloneTests/LoginViewModelTests.swift
    
    **MANDATORY TEST METHODS:**
    
    1. **Initialization Tests:**
       - testInitialization()
       - testInitialState()
       - testDependencyInjection()
    
    2. **Form Validation Tests:**
       - testIsFormValidWithValidInput()
       - testIsFormValidWithEmptyUsername()
       - testIsFormValidWithEmptyPassword()
       - testIsFormValidWithShortPassword()
       - testCanSubmitWhenFormValidAndNotLoading()
       - testCannotSubmitWhenLoading()
    
    3. **Login Success Tests:**
       - testLoginSuccess()
       - testLoginSuccessStateTransitions()
       - testLoginSuccessUpdatesProperties()
    
    4. **Login Error Tests:**
       - testLoginWithInvalidCredentials()
       - testLoginWithNetworkError()
       - testLoginWithServerError()
       - testLoginWithDecodingError()
       - testErrorMessageGeneration()
    
    5. **State Management Tests:**
       - testLoadingStateManagement()
       - testErrorStateManagement()
       - testClearErrorFunctionality()
       - testResetFunctionality()
    
    6. **Async Testing:**
       - testAsyncLoginExecution()
       - testConcurrentLoginPrevention()
    
    **TEST IMPLEMENTATION REQUIREMENTS:**
    
    Each test MUST have:
    - Proper setUp() with MockNetworkManager
    - Clear arrange/act/assert structure
    - Async/await for login method testing
    - @Published property change validation
    - Meaningful assertions with proper error messages
    
    **ASYNC TESTING PATTERN:**
    ```swift
    func testLoginSuccess() async {
        // Arrange
        mockNetworkManager.shouldSucceed = true
        mockNetworkManager.mockAuthResponse = AuthResponse(...)
        viewModel.username = "testuser"
        viewModel.password = "testpass123"
        
        // Act
        await viewModel.login()
        
        // Assert
        XCTAssertTrue(viewModel.isLoggedIn)
        XCTAssertFalse(viewModel.isLoading)
        XCTAssertEqual(mockNetworkManager.callCount, 1)
    }
    ```
    
    **OUTPUT FORMAT:**
    ```swift
    // FILE: LoginViewModelTests.swift
    import XCTest
    import Combine
    @testable import TwitterClone
    
    @MainActor
    final class LoginViewModelTests: XCTestCase {
        var viewModel: LoginViewModel!
        var mockNetworkManager: MockNetworkManager!
        
        override func setUp() {
            super.setUp()
            // COMPLETE SETUP
        }
        
        // ALL TEST METHODS WITH COMPLETE IMPLEMENTATION
    }
    ```
    
    EVERY TEST METHOD MUST HAVE REAL IMPLEMENTATION! NO EMPTY BODIES!
    """,
    expected_output="Complete LoginViewModelTests.swift with all test methods implemented",
    agent=async_testing_specialist,
    depends_on=[mock_implementation_task]
)

# =============================================================================
# VIEWMODEL TEST FILE CREATION
# =============================================================================

def create_viewmodel_test_files(crew_result):
    """Extract and create ViewModel test files"""
    
    print("\n🧪 CREATING LOGINVIEWMODEL TEST SUITE!")
    
    tests_dir = Path(test_output_path)
    tests_dir.mkdir(parents=True, exist_ok=True)
    
    result_text = str(crew_result)
    
    # Save debug output
    debug_file = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai") / "viewmodel_tests_debug.txt"
    with open(debug_file, 'w') as f:
        f.write(result_text)
    print(f"🔍 Debug output: viewmodel_tests_debug.txt")
    
    # Extract Swift test files
    import re
    pattern = r'// FILE: ([^\n]+\.swift)\n([\s\S]*?)(?=// FILE:|$)'
    matches = re.findall(pattern, result_text, re.MULTILINE | re.DOTALL)
    
    print(f"📝 Found {len(matches)} Swift test files")
    
    files_created = []
    
    for filename, code_content in matches:
        filename = filename.strip()
        code_content = code_content.strip()
        
        # Clean up code blocks
        code_content = re.sub(r'^```swift\n?', '', code_content, flags=re.MULTILINE)
        code_content = re.sub(r'^```\n?', '', code_content, flags=re.MULTILINE)
        code_content = code_content.strip()
        
        # Validate this is substantial test code
        if len(code_content) < 300:
            print(f"⚠️  {filename} too short ({len(code_content)} chars) - might be empty")
            continue
            
        # Check for required test components
        required_patterns = ['XCTest', 'func test', '@testable import TwitterClone']
        missing_patterns = [p for p in required_patterns if p not in code_content]
        
        if missing_patterns and 'Mock' not in filename:
            print(f"⚠️  {filename} missing: {', '.join(missing_patterns)}")
            continue
        
        file_path = tests_dir / filename
        
        try:
            with open(file_path, 'w') as f:
                f.write(code_content)
            
            print(f"✅ Created: {filename} ({len(code_content)} chars)")
            files_created.append(filename)
            
            # Validate test features
            if 'Tests.swift' in filename:
                test_methods = len(re.findall(r'func test\w+\(', code_content))
                if test_methods > 0:
                    print(f"   🧪 Contains {test_methods} test methods")
            elif 'Mock' in filename:
                print(f"   🎭 Mock implementation")
            
        except Exception as e:
            print(f"❌ Failed to create {filename}: {str(e)}")
    
    # Create professional fallback if agents failed
    if len(files_created) < 2:
        print("\n🔥 AGENTS FAILED! Creating professional fallback tests...")
        create_professional_viewmodel_tests(tests_dir)
        files_created.extend(["LoginViewModelTests.swift", "MockNetworkManager.swift"])
    
    return files_created

def create_professional_viewmodel_tests(tests_dir):
    """Create professional ViewModel tests as fallback"""
    
    # Professional MockNetworkManager
    mock_network_manager = '''import Foundation
@testable import TwitterClone

class MockNetworkManager {
    // Configuration
    var shouldSucceed: Bool = true
    var mockAuthResponse: AuthResponse?
    var mockError: NetworkError?
    var responseDelay: TimeInterval = 0
    
    // Tracking
    var lastEndpoint: APIEndpoint?
    var callCount: Int = 0
    var lastToken: String?
    
    func request<T: Codable>(
        endpoint: APIEndpoint,
        responseType: T.Type,
        token: String? = nil
    ) async throws -> T {
        
        // Track the call
        lastEndpoint = endpoint
        lastToken = token
        callCount += 1
        
        // Apply delay if configured
        if responseDelay > 0 {
            try await Task.sleep(nanoseconds: UInt64(responseDelay * 1_000_000_000))
        }
        
        // Return success or throw error
        if shouldSucceed {
            guard let response = mockAuthResponse else {
                throw NetworkError.noData
            }
            return response as! T
        } else {
            throw mockError ?? NetworkError.requestFailed(NSError(domain: "MockError", code: -1))
        }
    }
    
    func reset() {
        shouldSucceed = true
        mockAuthResponse = nil
        mockError = nil
        responseDelay = 0
        lastEndpoint = nil
        callCount = 0
        lastToken = nil
    }
}
'''
    
    # Professional LoginViewModelTests
    viewmodel_tests = '''import XCTest
import Combine
@testable import TwitterClone

@MainActor
final class LoginViewModelTests: XCTestCase {
    var viewModel: LoginViewModel!
    var mockNetworkManager: MockNetworkManager!
    
    override func setUp() {
        super.setUp()
        mockNetworkManager = MockNetworkManager()
        viewModel = LoginViewModel(networkManager: mockNetworkManager as! NetworkManager)
    }
    
    override func tearDown() {
        viewModel = nil
        mockNetworkManager = nil
        super.tearDown()
    }
    
    // MARK: - Initialization Tests
    
    func testInitialization() {
        XCTAssertEqual(viewModel.username, "")
        XCTAssertEqual(viewModel.password, "")
        XCTAssertFalse(viewModel.isLoading)
        XCTAssertEqual(viewModel.errorMessage, "")
        XCTAssertFalse(viewModel.showError)
        XCTAssertFalse(viewModel.isLoggedIn)
    }
    
    func testInitialState() {
        XCTAssertFalse(viewModel.isFormValid)
        XCTAssertFalse(viewModel.canSubmit)
        XCTAssertEqual(viewModel.loginButtonTitle, "Sign In")
    }
    
    // MARK: - Form Validation Tests
    
    func testIsFormValidWithValidInput() {
        viewModel.username = "testuser"
        viewModel.password = "password123"
        
        XCTAssertTrue(viewModel.isFormValid)
        XCTAssertTrue(viewModel.canSubmit)
    }
    
    func testIsFormValidWithEmptyUsername() {
        viewModel.username = ""
        viewModel.password = "password123"
        
        XCTAssertFalse(viewModel.isFormValid)
        XCTAssertFalse(viewModel.canSubmit)
    }
    
    func testIsFormValidWithEmptyPassword() {
        viewModel.username = "testuser"
        viewModel.password = ""
        
        XCTAssertFalse(viewModel.isFormValid)
        XCTAssertFalse(viewModel.canSubmit)
    }
    
    func testIsFormValidWithShortPassword() {
        viewModel.username = "testuser"
        viewModel.password = "12345"  // Less than 6 characters
        
        XCTAssertFalse(viewModel.isFormValid)
        XCTAssertFalse(viewModel.canSubmit)
    }
    
    func testCannotSubmitWhenLoading() {
        viewModel.username = "testuser"
        viewModel.password = "password123"
        viewModel.isLoading = true
        
        XCTAssertTrue(viewModel.isFormValid)
        XCTAssertFalse(viewModel.canSubmit)
    }
    
    // MARK: - Login Success Tests
    
    func testLoginSuccess() async {
        // Arrange
        let testUser = User(
            id: UUID(),
            username: "testuser",
            email: "test@example.com",
            displayName: "Test User",
            bio: nil,
            isActive: true,
            createdAt: Date()
        )
        let testResponse = AuthResponse(
            token: "test-jwt-token",
            tokenType: "Bearer",
            expiresIn: 3600,
            user: testUser
        )
        
        mockNetworkManager.shouldSucceed = true
        mockNetworkManager.mockAuthResponse = testResponse
        
        viewModel.username = "testuser"
        viewModel.password = "password123"
        
        // Act
        await viewModel.login()
        
        // Assert
        XCTAssertTrue(viewModel.isLoggedIn)
        XCTAssertFalse(viewModel.isLoading)
        XCTAssertFalse(viewModel.showError)
        XCTAssertEqual(mockNetworkManager.callCount, 1)
    }
    
    // MARK: - Login Error Tests
    
    func testLoginWithInvalidCredentials() async {
        // Arrange
        mockNetworkManager.shouldSucceed = false
        mockNetworkManager.mockError = NetworkError.serverError(401)
        
        viewModel.username = "testuser"
        viewModel.password = "wrongpassword"
        
        // Act
        await viewModel.login()
        
        // Assert
        XCTAssertFalse(viewModel.isLoggedIn)
        XCTAssertFalse(viewModel.isLoading)
        XCTAssertTrue(viewModel.showError)
        XCTAssertEqual(viewModel.errorMessage, "Invalid username or password")
    }
    
    func testLoginWithNetworkError() async {
        // Arrange
        mockNetworkManager.shouldSucceed = false
        mockNetworkManager.mockError = NetworkError.requestFailed(NSError(domain: "Network", code: -1009))
        
        viewModel.username = "testuser"
        viewModel.password = "password123"
        
        // Act
        await viewModel.login()
        
        // Assert
        XCTAssertFalse(viewModel.isLoggedIn)
        XCTAssertFalse(viewModel.isLoading)
        XCTAssertTrue(viewModel.showError)
        XCTAssertTrue(viewModel.errorMessage.contains("Network connection failed"))
    }
    
    // MARK: - State Management Tests
    
    func testClearErrorFunctionality() {
        // Arrange
        viewModel.errorMessage = "Test error"
        viewModel.showError = true
        
        // Act
        viewModel.clearError()
        
        // Assert
        XCTAssertEqual(viewModel.errorMessage, "")
        XCTAssertFalse(viewModel.showError)
    }
    
    func testResetFunctionality() {
        // Arrange
        viewModel.username = "testuser"
        viewModel.password = "password123"
        viewModel.isLoading = true
        viewModel.errorMessage = "Test error"
        viewModel.showError = true
        viewModel.isLoggedIn = true
        
        // Act
        viewModel.reset()
        
        // Assert
        XCTAssertEqual(viewModel.username, "")
        XCTAssertEqual(viewModel.password, "")
        XCTAssertFalse(viewModel.isLoading)
        XCTAssertEqual(viewModel.errorMessage, "")
        XCTAssertFalse(viewModel.showError)
        XCTAssertFalse(viewModel.isLoggedIn)
    }
    
    func testLoginButtonTitle() {
        XCTAssertEqual(viewModel.loginButtonTitle, "Sign In")
        
        viewModel.isLoading = true
        XCTAssertEqual(viewModel.loginButtonTitle, "Signing In...")
    }
}
'''
    
    # Write professional test files
    test_files = [
        ("MockNetworkManager.swift", mock_network_manager),
        ("LoginViewModelTests.swift", viewmodel_tests)
    ]
    
    for filename, content in test_files:
        file_path = tests_dir / filename
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"💪 Created PROFESSIONAL: {filename} ({len(content)} chars)")

# =============================================================================
# EXECUTION - VIEWMODEL TESTING FOCUS
# =============================================================================

if __name__ == "__main__":
    print("🧪 LOGINVIEWMODEL UNIT TESTS - COMPREHENSIVE TESTING!")
    print("=" * 70)
    print("🎯 MISSION: Create thorough unit tests for LoginViewModel")
    print("=" * 70)
    
    # Create ViewModel testing crew
    viewmodel_testing_crew = Crew(
        agents=[viewmodel_test_architect, mock_networking_expert, async_testing_specialist],
        tasks=[test_strategy_task, mock_implementation_task, viewmodel_tests_implementation],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        # Execute ViewModel testing
        result = viewmodel_testing_crew.kickoff()
        
        # Create test files
        files_created = create_viewmodel_test_files(result)
        
        print("\n" + "=" * 70)
        print("🧪 VIEWMODEL TESTING RESULTS:")
        print("📋 Test Files Created:")
        for filename in files_created:
            print(f"   ✅ {filename}")
        print("=" * 70)
        
        if len(files_created) >= 2:
            print("🎉 SUCCESS! Comprehensive ViewModel test suite created!")
            print("💡 Run tests in Xcode to validate LoginViewModel behavior")
        else:
            print("⚠️  Limited test files created - check agent output")
            
    except Exception as e:
        print(f"\n💥 VIEWMODEL TESTING FAILED: {str(e)}")

#!/usr/bin/env python3
"""
iOS Networking Tests - EXTREME FOCUS Edition
ONE JOB: Write comprehensive unit tests that actually test things!
NO EMPTY TEST METHODS! NO PLACEHOLDER TESTS!
"""

import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process

# Set working directory
ios_project_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone"
test_output_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterCloneTests"

# =============================================================================
# TESTING-OBSESSED AGENTS - ONLY ONE MISSION
# =============================================================================

test_architect = Agent(
    role='Senior Test Architect (Testing Evangelist)',
    goal='Design a bulletproof testing strategy for iOS networking layer',
    backstory="""You are a testing fanatic with 20+ years writing unit tests. 
    You believe untested code is broken code. You design test suites that catch 
    every possible edge case, error condition, and failure scenario. 
    You write test plans so detailed that junior developers can implement them blindfolded.
    Empty test files are your personal enemy.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

mock_specialist = Agent(
    role='Mocking Specialist (Mock Master)',
    goal='Create comprehensive mock objects that enable isolated unit testing',
    backstory="""You are the master of mocking frameworks. You create mock objects 
    that perfectly simulate real dependencies without any external calls. 
    Your mocks are so realistic they fool the code under test completely.
    You mock URLSession, Keychain, UserDefaults, and any external dependency.
    Your mocks support both success and failure scenarios with configurable responses.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

test_implementer = Agent(
    role='Test Implementation Machine (Code Generator)',
    goal='Write COMPLETE, FUNCTIONAL test methods that actually validate behavior',
    backstory="""You are a test-writing machine. Every test method you write has:
    - Clear arrange/act/assert structure
    - Meaningful test names that describe what is being tested
    - Complete setup and teardown
    - Proper assertions that validate expected behavior
    - Error case testing alongside happy path testing
    You NEVER write empty test methods or TODO comments in tests.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

# =============================================================================
# LASER-FOCUSED TESTING TASKS
# =============================================================================

test_strategy_task = Task(
    description="""
    DESIGN A COMPREHENSIVE TESTING STRATEGY for the iOS networking layer.
    
    **WHAT NEEDS TESTING (BE SPECIFIC):**
    
    1. **NetworkManager Tests:**
       - Successful API request handling
       - HTTP error status codes (400, 401, 403, 404, 500, etc.)
       - Network timeout scenarios
       - Invalid URL handling
       - JSON parsing success and failure
       - Authentication token injection
       - Request building with different endpoints
       - Response validation
    
    2. **APIEndpoint Tests:**
       - URL construction for all endpoint types
       - HTTP method assignment
       - Request body generation
       - Base URL selection logic
       - Parameter encoding
    
    3. **AuthManager Tests:**
       - JWT token storage in Keychain
       - Token retrieval from Keychain
       - Token deletion from Keychain
       - User data persistence in UserDefaults
       - Authentication state management
       - Login/logout flow testing
       - Token refresh scenarios
    
    **MOCK REQUIREMENTS:**
    - MockURLSession with configurable responses
    - MockKeychain for secure storage testing
    - MockUserDefaults for preferences testing
    - MockNetworkError generation
    
    **OUTPUT REQUIRED:**
    Detailed test specification with exact test method names and what each tests.
    """,
    expected_output="Complete testing strategy with specific test cases for each component",
    agent=test_architect
)

mock_creation_task = Task(
    description="""
    CREATE COMPREHENSIVE MOCK OBJECTS for isolated unit testing.
    
    **MANDATORY MOCK FILES TO CREATE:**
    
    1. **MockURLSession.swift** - MUST include:
       - URLSessionProtocol conformance
       - Configurable response data
       - Configurable HTTP status codes
       - Configurable error responses
       - Request validation capabilities
       - Async/await support for data(for:) method
    
    2. **MockKeychain.swift** - MUST include:
       - All Security framework operations
       - In-memory storage for testing
       - Success/failure simulation
       - Data corruption scenarios
    
    3. **TestHelpers.swift** - MUST include:
       - Sample data generation (User, Post, etc.)
       - Common test setup methods
       - Assertion helpers
       - Mock response builders
    
    **MOCK QUALITY REQUIREMENTS:**
    - Each mock must support both success and failure scenarios
    - Mocks must be completely isolated (no real network/storage calls)
    - Mocks must be easily configurable in test setup
    - Include comprehensive documentation for each mock method
    
    **OUTPUT FORMAT:**
    ```swift
    // FILE: MockURLSession.swift
    import Foundation
    @testable import TwitterClone
    
    protocol URLSessionProtocol {
        func data(for request: URLRequest) async throws -> (Data, URLResponse)
    }
    
    extension URLSession: URLSessionProtocol {}
    
    class MockURLSession: URLSessionProtocol {
        // COMPLETE IMPLEMENTATION HERE
    }
    ```
    
    NO EMPTY PROTOCOL STUBS! Every mock must be fully functional!
    """,
    expected_output="3 complete mock files with full implementations",
    agent=mock_specialist,
    depends_on=[test_strategy_task]
)

test_implementation_task = Task(
    description="""
    WRITE COMPLETE UNIT TESTS - Every test must actually test something!
    
    **FILES TO CREATE IN:** /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterCloneTests/
    
    **MANDATORY TEST FILES:**
    
    1. **NetworkManagerTests.swift** - MUST include these specific tests:
       - testSuccessfulAPIRequest()
       - testNetworkFailure()
       - testHTTPErrorStatuses() 
       - testInvalidURL()
       - testJSONParsingSuccess()
       - testJSONParsingFailure()
       - testAuthenticationTokenInjection()
       - testRequestTimeout()
       - testGenericRequestHandling()
    
    2. **APIEndpointTests.swift** - MUST include:
       - testLoginEndpointConstruction()
       - testRegisterEndpointConstruction()
       - testTimelineEndpointConstruction()
       - testPostCreationEndpointConstruction()
       - testLikeUnlikeEndpointConstruction()
       - testHTTPMethodAssignment()
       - testRequestBodyGeneration()
       - testBaseURLSelection()
    
    3. **AuthManagerTests.swift** - MUST include:
       - testTokenSaveToKeychain()
       - testTokenRetrievalFromKeychain()
       - testTokenDeletionFromKeychain()
       - testUserDataPersistence()
       - testLoginFlow()
       - testLogoutFlow()
       - testAuthenticationStateChanges()
       - testKeychainErrorHandling()
    
    **TEST METHOD REQUIREMENTS:**
    Each test method MUST have:
    - Descriptive name explaining what it tests
    - Arrange section (setup test data)
    - Act section (execute the code being tested)
    - Assert section (verify expected results)
    - Proper mock configuration
    - Both success and failure case testing where applicable
    
    **OUTPUT FORMAT:**
    ```swift
    // FILE: NetworkManagerTests.swift
    import XCTest
    @testable import TwitterClone
    
    final class NetworkManagerTests: XCTestCase {
        var networkManager: NetworkManager!
        var mockURLSession: MockURLSession!
        
        override func setUp() {
            super.setUp()
            // COMPLETE SETUP HERE
        }
        
        func testSuccessfulAPIRequest() async {
            // Arrange
            // COMPLETE IMPLEMENTATION
            
            // Act
            // COMPLETE IMPLEMENTATION
            
            // Assert
            // COMPLETE IMPLEMENTATION
        }
    }
    ```
    
    NO EMPTY TEST BODIES! Every test must have real implementation!
    """,
    expected_output="Complete unit test suite with fully implemented test methods",
    agent=test_implementer,
    depends_on=[mock_creation_task]
)

# =============================================================================
# AGGRESSIVE FILE CREATION - TESTS ONLY
# =============================================================================

def create_test_files_aggressively(crew_result):
    """Extract and create test files - focus on quality over quantity"""
    
    print("\n🧪 CREATING COMPREHENSIVE TEST SUITE!")
    
    tests_dir = Path(test_output_path)
    tests_dir.mkdir(parents=True, exist_ok=True)
    
    result_text = str(crew_result)
    
    # Save debug output
    debug_file = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai") / "focused_testing_debug.txt"
    with open(debug_file, 'w') as f:
        f.write(result_text)
    print(f"🔍 Debug output: focused_testing_debug.txt")
    
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
        if len(code_content) < 200:  # Tests should be substantial
            print(f"⚠️  {filename} too short ({len(code_content)} chars) - skipping")
            continue
            
        # Check for actual test methods
        if 'func test' not in code_content and 'Mock' not in filename:
            print(f"⚠️  {filename} doesn't contain test methods - might not be a real test file")
            continue
        
        file_path = tests_dir / filename
        
        try:
            with open(file_path, 'w') as f:
                f.write(code_content)
            
            print(f"✅ Created: {filename} ({len(code_content)} chars)")
            files_created.append(filename)
            
            # Validate test quality
            test_methods = len(re.findall(r'func test\w+\(', code_content))
            if test_methods > 0:
                print(f"   📊 Contains {test_methods} test methods")
            
        except Exception as e:
            print(f"❌ Failed to create {filename}: {str(e)}")
    
    # Create fallback test files if agents failed
    if len(files_created) < 3:
        print("\n🔥 AGENTS FAILED! Creating professional fallback tests...")
        create_professional_test_fallbacks(tests_dir)
        files_created.extend(["NetworkManagerTests.swift", "MockURLSession.swift", "AuthManagerTests.swift"])
    
    return files_created

def create_professional_test_fallbacks(tests_dir):
    """Create professional-grade test files as fallback"""
    
    # Professional NetworkManagerTests
    network_manager_tests = '''import XCTest
@testable import TwitterClone

final class NetworkManagerTests: XCTestCase {
    var networkManager: NetworkManager!
    var mockURLSession: MockURLSession!
    
    override func setUp() {
        super.setUp()
        mockURLSession = MockURLSession()
        networkManager = NetworkManager(session: mockURLSession)
    }
    
    override func tearDown() {
        networkManager = nil
        mockURLSession = nil
        super.tearDown()
    }
    
    func testSuccessfulAPIRequest() async throws {
        // Arrange
        let expectedUser = User(id: "123", username: "testuser", email: "test@example.com")
        let responseData = try JSONEncoder().encode(expectedUser)
        mockURLSession.mockData = responseData
        mockURLSession.mockResponse = HTTPURLResponse(
            url: URL(string: "http://localhost:8080/api/auth/login")!,
            statusCode: 200,
            httpVersion: nil,
            headerFields: nil
        )
        
        // Act
        let result: User = try await networkManager.request(
            endpoint: .login(username: "testuser", password: "password"),
            responseType: User.self
        )
        
        // Assert
        XCTAssertEqual(result.username, "testuser")
        XCTAssertEqual(result.email, "test@example.com")
        XCTAssertEqual(mockURLSession.lastRequest?.httpMethod, "POST")
    }
    
    func testNetworkFailure() async {
        // Arrange
        mockURLSession.mockError = URLError(.notConnectedToInternet)
        
        // Act & Assert
        do {
            let _: User = try await networkManager.request(
                endpoint: .login(username: "test", password: "test"),
                responseType: User.self
            )
            XCTFail("Expected network error")
        } catch {
            XCTAssertTrue(error is NetworkError)
        }
    }
    
    func testHTTPErrorStatuses() async {
        // Arrange
        mockURLSession.mockResponse = HTTPURLResponse(
            url: URL(string: "http://localhost:8080/api/auth/login")!,
            statusCode: 401,
            httpVersion: nil,
            headerFields: nil
        )
        mockURLSession.mockData = Data()
        
        // Act & Assert
        do {
            let _: User = try await networkManager.request(
                endpoint: .login(username: "test", password: "test"),
                responseType: User.self
            )
            XCTFail("Expected HTTP error")
        } catch NetworkError.serverError(let statusCode) {
            XCTAssertEqual(statusCode, 401)
        } catch {
            XCTFail("Unexpected error type: \\(error)")
        }
    }
    
    func testAuthenticationTokenInjection() async throws {
        // Arrange
        let token = "test-jwt-token"
        mockURLSession.mockData = "{}".data(using: .utf8)!
        mockURLSession.mockResponse = HTTPURLResponse(
            url: URL(string: "http://localhost:8081/api/posts")!,
            statusCode: 200,
            httpVersion: nil,
            headerFields: nil
        )
        
        // Act
        let _: [String: String] = try await networkManager.request(
            endpoint: .createPost(content: "Test post"),
            responseType: [String: String].self,
            token: token
        )
        
        // Assert
        let authHeader = mockURLSession.lastRequest?.value(forHTTPHeaderField: "Authorization")
        XCTAssertEqual(authHeader, "Bearer \\(token)")
    }
}
'''
    
    # Professional MockURLSession
    mock_url_session = '''import Foundation
@testable import TwitterClone

protocol URLSessionProtocol {
    func data(for request: URLRequest) async throws -> (Data, URLResponse)
}

extension URLSession: URLSessionProtocol {}

class MockURLSession: URLSessionProtocol {
    var mockData: Data?
    var mockResponse: URLResponse?
    var mockError: Error?
    var lastRequest: URLRequest?
    
    func data(for request: URLRequest) async throws -> (Data, URLResponse) {
        lastRequest = request
        
        if let error = mockError {
            throw error
        }
        
        guard let data = mockData,
              let response = mockResponse else {
            throw URLError(.badServerResponse)
        }
        
        return (data, response)
    }
    
    func reset() {
        mockData = nil
        mockResponse = nil
        mockError = nil
        lastRequest = nil
    }
}
'''
    
    # Professional AuthManagerTests
    auth_manager_tests = '''import XCTest
@testable import TwitterClone

final class AuthManagerTests: XCTestCase {
    var authManager: AuthManager!
    
    override func setUp() {
        super.setUp()
        authManager = AuthManager()
        // Clear any existing test data
        authManager.logout()
    }
    
    override func tearDown() {
        authManager.logout()
        authManager = nil
        super.tearDown()
    }
    
    func testTokenSaveAndRetrieval() {
        // Arrange
        let testToken = "test-jwt-token-12345"
        
        // Act
        authManager.saveToken(testToken)
        let retrievedToken = authManager.getToken()
        
        // Assert
        XCTAssertEqual(retrievedToken, testToken)
    }
    
    func testLoginFlow() {
        // Arrange
        let testUser = User(id: "123", username: "testuser", email: "test@example.com")
        let testToken = "test-jwt-token"
        
        // Act
        authManager.login(user: testUser, token: testToken)
        
        // Assert
        XCTAssertTrue(authManager.isAuthenticated)
        XCTAssertEqual(authManager.currentUser?.username, "testuser")
        XCTAssertEqual(authManager.getToken(), testToken)
    }
    
    func testLogoutFlow() {
        // Arrange
        let testUser = User(id: "123", username: "testuser", email: "test@example.com")
        let testToken = "test-jwt-token"
        authManager.login(user: testUser, token: testToken)
        
        // Act
        authManager.logout()
        
        // Assert
        XCTAssertFalse(authManager.isAuthenticated)
        XCTAssertNil(authManager.currentUser)
        XCTAssertNil(authManager.getToken())
    }
    
    func testTokenDeletion() {
        // Arrange
        let testToken = "test-jwt-token"
        authManager.saveToken(testToken)
        
        // Act
        authManager.logout()
        
        // Assert
        XCTAssertNil(authManager.getToken())
    }
    
    func testUserDataPersistence() {
        // Arrange
        let testUser = User(id: "123", username: "testuser", email: "test@example.com")
        let testToken = "test-jwt-token"
        
        // Act
        authManager.login(user: testUser, token: testToken)
        
        // Create new AuthManager instance to test persistence
        let newAuthManager = AuthManager()
        
        // Assert
        XCTAssertTrue(newAuthManager.isAuthenticated)
        XCTAssertEqual(newAuthManager.currentUser?.username, "testuser")
    }
}
'''
    
    # Write professional test files
    test_files = [
        ("NetworkManagerTests.swift", network_manager_tests),
        ("MockURLSession.swift", mock_url_session),
        ("AuthManagerTests.swift", auth_manager_tests)
    ]
    
    for filename, content in test_files:
        file_path = tests_dir / filename
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"💪 Created PROFESSIONAL: {filename} ({len(content)} chars)")

# =============================================================================
# EXECUTION - TESTING FOCUS ONLY
# =============================================================================

if __name__ == "__main__":
    print("🧪 iOS TESTING FOCUS - COMPREHENSIVE TEST GENERATION!")
    print("=" * 70)
    print("📊 MISSION: Create bulletproof unit tests for networking layer")
    print("=" * 70)
    
    # Create testing-focused crew
    testing_crew = Crew(
        agents=[test_architect, mock_specialist, test_implementer],
        tasks=[test_strategy_task, mock_creation_task, test_implementation_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        # Execute focused testing
        result = testing_crew.kickoff()
        
        # Create test files aggressively
        files_created = create_test_files_aggressively(result)
        
        print("\n" + "=" * 70)
        print("🧪 TESTING RESULTS:")
        print("📋 Test Files Created:")
        for filename in files_created:
            print(f"   ✅ {filename}")
        print("=" * 70)
        
        if len(files_created) >= 3:
            print("🎉 SUCCESS! Comprehensive test suite created!")
        else:
            print("⚠️  Limited test files - fallbacks created")
            
    except Exception as e:
        print(f"\n💥 TESTING FAILED: {str(e)}")

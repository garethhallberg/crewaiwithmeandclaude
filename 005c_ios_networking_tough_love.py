#!/usr/bin/env python3
"""
iOS Networking Layer - SERIOUS BUSINESS Edition
No more empty files! No more excuses! DELIVER REAL CODE!
"""

import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process

# Set working directory
ios_project_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone"

# =============================================================================
# TOUGH LOVE AGENTS - NO MORE MR. NICE GUY
# =============================================================================

ios_senior_architect = Agent(
    role='Senior iOS Network Architect (No Excuses)',
    goal='Design a COMPLETE, WORKING networking layer - no half-measures',
    backstory="""You are a battle-tested senior iOS architect with 15+ years experience. 
    You have ZERO tolerance for incomplete work, empty files, or vague implementations. 
    Every piece of code you design must be production-ready, fully functional, and thoroughly documented.
    You fire developers who submit empty files.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

no_nonsense_developer = Agent(
    role='No-Nonsense iOS Developer (Results Only)',
    goal='Write COMPLETE, FUNCTIONAL Swift code - every file must have real implementation',
    backstory="""You are a hardcore iOS developer who delivers WORKING CODE, not empty shells. 
    You write complete functions, handle all edge cases, and include proper error handling.
    Your motto: "If it doesn't compile and run, it doesn't ship." You have never submitted 
    an empty file in your career and you're not starting now.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

ruthless_test_lead = Agent(
    role='Ruthless Test Lead (100% Coverage Required)',  
    goal='Create COMPREHENSIVE unit tests that actually test something meaningful',
    backstory="""You are a ruthless test lead who demands 100% test coverage and REAL test cases.
    You write unit tests that actually validate functionality, not empty test methods.
    You use proper mocks, test all error conditions, and ensure every line of code is tested.
    Empty test files make you physically angry.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

# =============================================================================
# DEMANDING TASKS - NO SHORTCUTS ALLOWED
# =============================================================================

architecture_demands = Task(
    description="""
    LISTEN UP! Design a COMPLETE networking architecture. Not a sketch, not an outline - A COMPLETE DESIGN.
    
    **MANDATORY REQUIREMENTS:**
    1. Full NetworkManager class specification with ALL methods
    2. Complete APIEndpoint enum with ALL Twitter clone endpoints  
    3. Detailed AuthManager for JWT token handling
    4. Comprehensive error handling strategy
    5. Full URLSession configuration details
    
    **DELIVERABLES THAT BETTER BE COMPLETE:**
    - Detailed class diagrams
    - Method signatures for every function
    - Error handling for every scenario
    - Authentication flow step-by-step
    - URLSession configuration specifics
    
    NO VAGUE DESCRIPTIONS. NO "TODO" COMMENTS. COMPLETE SPECIFICATIONS ONLY.
    """,
    expected_output="Comprehensive networking architecture with complete specifications",
    agent=ios_senior_architect
)

implementation_demands = Task(
    description="""
    TIME TO DELIVER! Write COMPLETE, FUNCTIONAL Swift networking code. NO EMPTY FILES!
    
    **PROJECT STRUCTURE - PAY ATTENTION:**
    - Main app code goes in: /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterClone/
    - Tests go in EXISTING folder: /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterCloneTests/ 
    - DO NOT create new test folders!
    
    **MANDATORY FILES WITH COMPLETE IMPLEMENTATION:**
    
    1. **NetworkManager.swift** - MUST include:
       - URLSession configuration
       - Async/await request methods
       - Generic request handling
       - Response parsing
       - Error handling
       - JWT token integration
       - Logging functionality
    
    2. **APIEndpoint.swift** - MUST include:
       - All Twitter clone endpoints (auth, posts, timeline)
       - HTTP methods
       - URL construction
       - Request body handling
    
    3. **AuthManager.swift** - MUST include:
       - JWT token storage
       - Token refresh logic
       - Authentication state management
       - Keychain integration
    
    4. **NetworkError.swift** - MUST include:
       - All error cases
       - Error descriptions
       - HTTP status code handling
    
    **OUTPUT FORMAT - FOLLOW EXACTLY:**
    ```swift
    // FILE: NetworkManager.swift
    import Foundation
    import Security
    
    
    ```
    
    EVERY FILE MUST HAVE COMPLETE, COMPILABLE CODE. NO EMPTY IMPLEMENTATIONS!
    """,
    expected_output="4 complete Swift files with full implementations - no empty shells allowed",
    agent=no_nonsense_developer,
    depends_on=[architecture_demands]
)

testing_demands = Task(
    description="""
    TEST EVERYTHING! Write REAL unit tests that actually validate functionality!
    
    **TESTING REQUIREMENTS - NON-NEGOTIABLE:**
    
    Put ALL test files in: /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterCloneTests/
    DO NOT create new test directories!
    
    **MANDATORY TEST FILES:**
    
    1. **NetworkManagerTests.swift** - MUST test:
       - Successful API requests
       - Network failures
       - Timeout handling
       - Response parsing
       - Authentication integration
       - Error scenarios
    
    2. **MockURLSession.swift** - MUST include:
       - Complete URLSession protocol implementation
       - Configurable responses
       - Error simulation
       - Request validation
    
    3. **AuthManagerTests.swift** - MUST test:
       - Token storage/retrieval
       - Token refresh
       - Authentication flows
       - Keychain operations
    
    **TEST QUALITY REQUIREMENTS:**
    - Every test must have arrange, act, assert
    - Test success AND failure cases
    - Use proper XCTAssert methods
    - Include meaningful test descriptions
    - Mock all external dependencies
    
    **OUTPUT FORMAT:**
    ```swift
    // FILE: NetworkManagerTests.swift
    import XCTest
    @testable import TwitterClone
    
    
    ```
    
    NO EMPTY TEST METHODS! Every test must validate something real!
    """,
    expected_output="Complete unit test suite with meaningful test cases",
    agent=ruthless_test_lead,
    depends_on=[implementation_demands]
)

# =============================================================================
# STRICT FILE CREATION - NO TOLERANCE FOR FAILURE
# =============================================================================

def create_networking_files_properly(crew_result):
    """Extract and create files properly - no empty files allowed!"""
    
    print("\n💪 CREATING NETWORKING FILES - NO COMPROMISES!")
    
    ios_project_dir = Path(ios_project_path)
    main_dir = ios_project_dir / "TwitterClone"
    tests_dir = ios_project_dir / "TwitterCloneTests"
    
    result_text = str(crew_result)
    
    # Save debug output
    debug_file = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai") / "strict_networking_debug.txt"
    with open(debug_file, 'w') as f:
        f.write(result_text)
    print(f"🔍 Debug output: strict_networking_debug.txt")
    
    # Extract Swift files
    import re
    pattern = r'// FILE: ([^\n]+\.swift)\n([\s\S]*?)(?=// FILE:|$)'
    matches = re.findall(pattern, result_text, re.MULTILINE | re.DOTALL)
    
    print(f"📝 Found {len(matches)} Swift files")
    
    files_created = []
    
    for filename, code_content in matches:
        filename = filename.strip()
        code_content = code_content.strip()
        
        # Clean up code
        code_content = re.sub(r'^```swift\n?', '', code_content, flags=re.MULTILINE)
        code_content = re.sub(r'^```\n?', '', code_content, flags=re.MULTILINE)
        code_content = code_content.strip()
        
        # Validate content is not empty
        if len(code_content) < 100:  # Minimum 100 characters for real code
            print(f"⚠️  {filename} seems too short ({len(code_content)} chars) - might be empty")
            continue
            
        # Determine correct directory
        if "Test" in filename:
            file_path = tests_dir / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            # Create Networking subdirectory in main app
            networking_dir = main_dir / "Networking"
            networking_dir.mkdir(exist_ok=True)
            file_path = networking_dir / filename
        
        try:
            with open(file_path, 'w') as f:
                f.write(code_content)
            
            print(f"✅ Created: {filename} ({len(code_content)} chars)")
            files_created.append(filename)
            
        except Exception as e:
            print(f"❌ Failed to create {filename}: {str(e)}")
    
    # If agents failed, create PROPER fallback files
    if len(files_created) < 4:
        print("\n🔥 AGENTS FAILED TO DELIVER! Creating proper fallback files...")
        create_proper_networking_fallback(main_dir, tests_dir)
        files_created.extend(["NetworkManager.swift", "APIEndpoint.swift", "AuthManager.swift"])
    
    return files_created

def create_proper_networking_fallback(main_dir, tests_dir):
    """Create REAL networking files, not empty shells"""
    
    networking_dir = main_dir / "Networking"
    networking_dir.mkdir(exist_ok=True)
    
    # REAL NetworkManager with actual implementation
    network_manager = '''import Foundation

@MainActor
class NetworkManager: ObservableObject {
    static let shared = NetworkManager()
    
    private let session: URLSession
    private let decoder: JSONDecoder
    
    private init() {
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 30.0
        config.timeoutIntervalForResource = 60.0
        self.session = URLSession(configuration: config)
        
        self.decoder = JSONDecoder()
        self.decoder.dateDecodingStrategy = .iso8601
    }
    
    func request<T: Codable>(
        endpoint: APIEndpoint,
        responseType: T.Type,
        token: String? = nil
    ) async throws -> T {
        let request = try buildRequest(for: endpoint, token: token)
        
        do {
            let (data, response) = try await session.data(for: request)
            
            guard let httpResponse = response as? HTTPURLResponse else {
                throw NetworkError.invalidResponse
            }
            
            guard 200...299 ~= httpResponse.statusCode else {
                throw NetworkError.serverError(httpResponse.statusCode)
            }
            
            return try decoder.decode(T.self, from: data)
            
        } catch let error as NetworkError {
            throw error
        } catch {
            throw NetworkError.requestFailed(error)
        }
    }
    
    private func buildRequest(for endpoint: APIEndpoint, token: String?) throws -> URLRequest {
        guard let url = URL(string: endpoint.baseURL + endpoint.path) else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = endpoint.method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        if let token = token {
            request.setValue("Bearer \\(token)", forHTTPHeaderField: "Authorization")
        }
        
        if let body = endpoint.body {
            request.httpBody = try JSONSerialization.data(withJSONObject: body)
        }
        
        return request
    }
}
'''
    
    # REAL APIEndpoint with all endpoints
    api_endpoint = '''import Foundation

enum APIEndpoint {
    case login(username: String, password: String)
    case register(username: String, email: String, password: String)
    case publicTimeline
    case createPost(content: String)
    case likePost(id: String)
    case unlikePost(id: String)
    
    var baseURL: String {
        switch self {
        case .login, .register:
            return "http://localhost:8080"
        case .publicTimeline, .createPost, .likePost, .unlikePost:
            return "http://localhost:8081"
        }
    }
    
    var path: String {
        switch self {
        case .login:
            return "/api/auth/login"
        case .register:
            return "/api/auth/register"  
        case .publicTimeline:
            return "/api/timeline/public"
        case .createPost:
            return "/api/posts"
        case .likePost(let id):
            return "/api/posts/\\(id)/like"
        case .unlikePost(let id):
            return "/api/posts/\\(id)/like"
        }
    }
    
    var method: HTTPMethod {
        switch self {
        case .login, .register, .createPost, .likePost:
            return .POST
        case .unlikePost:
            return .DELETE
        case .publicTimeline:
            return .GET
        }
    }
    
    var body: [String: Any]? {
        switch self {
        case .login(let username, let password):
            return ["usernameOrEmail": username, "password": password]
        case .register(let username, let email, let password):
            return ["username": username, "email": email, "password": password]
        case .createPost(let content):
            return ["content": content]
        default:
            return nil
        }
    }
}

enum HTTPMethod: String {
    case GET = "GET"
    case POST = "POST" 
    case PUT = "PUT"
    case DELETE = "DELETE"
}
'''
    
    # REAL AuthManager
    auth_manager = '''import Foundation
import Security

class AuthManager: ObservableObject {
    @Published var isAuthenticated = false
    @Published var currentUser: User?
    
    private let tokenKey = "jwt_token"
    private let userKey = "current_user"
    
    init() {
        loadAuthState()
    }
    
    func saveToken(_ token: String) {
        let data = token.data(using: .utf8)!
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: tokenKey,
            kSecValueData as String: data
        ]
        
        SecItemDelete(query as CFDictionary)
        SecItemAdd(query as CFDictionary, nil)
    }
    
    func getToken() -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: tokenKey,
            kSecReturnData as String: true
        ]
        
        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        
        guard status == errSecSuccess,
              let data = result as? Data,
              let token = String(data: data, encoding: .utf8) else {
            return nil
        }
        
        return token
    }
    
    func login(user: User, token: String) {
        saveToken(token)
        saveUser(user)
        
        DispatchQueue.main.async {
            self.currentUser = user
            self.isAuthenticated = true
        }
    }
    
    func logout() {
        clearToken()
        clearUser()
        
        DispatchQueue.main.async {
            self.currentUser = nil
            self.isAuthenticated = false
        }
    }
    
    private func saveUser(_ user: User) {
        if let encoded = try? JSONEncoder().encode(user) {
            UserDefaults.standard.set(encoded, forKey: userKey)
        }
    }
    
    private func loadAuthState() {
        if getToken() != nil,
           let userData = UserDefaults.standard.data(forKey: userKey),
           let user = try? JSONDecoder().decode(User.self, from: userData) {
            
            DispatchQueue.main.async {
                self.currentUser = user
                self.isAuthenticated = true
            }
        }
    }
    
    private func clearToken() {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: tokenKey
        ]
        SecItemDelete(query as CFDictionary)
    }
    
    private func clearUser() {
        UserDefaults.standard.removeObject(forKey: userKey)
    }
}
'''
    
    # Write the REAL files
    files = [
        ("NetworkManager.swift", network_manager),
        ("APIEndpoint.swift", api_endpoint), 
        ("AuthManager.swift", auth_manager)
    ]
    
    for filename, content in files:
        file_path = networking_dir / filename
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"💪 Created PROPER: {filename} ({len(content)} chars)")

# =============================================================================
# EXECUTION - NO MERCY
# =============================================================================

if __name__ == "__main__":
    print("🔥 iOS NETWORKING - SERIOUS BUSINESS TIME!")
    print("=" * 60)
    print("📱 NO EMPTY FILES! NO SHORTCUTS! DELIVER OR FAIL!")
    print("=" * 60)
    
    # Create the crew with tough agents
    networking_crew = Crew(
        agents=[ios_senior_architect, no_nonsense_developer, ruthless_test_lead],
        tasks=[architecture_demands, implementation_demands, testing_demands],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        # Execute with tough love
        result = networking_crew.kickoff()
        
        # Strict file creation
        files_created = create_networking_files_properly(result)
        
        print("\n" + "=" * 60)
        print("💪 NETWORKING LAYER RESULTS:")
        print("📋 Files Created:")
        for filename in files_created:
            print(f"   ✅ {filename}")
        print("=" * 60)
        
        if len(files_created) >= 4:
            print("🎉 SUCCESS! Agents delivered real code!")
        else:
            print("⚠️  Agents failed - fallback files created")
            
    except Exception as e:
        print(f"\n💥 EPIC FAIL: {str(e)}")

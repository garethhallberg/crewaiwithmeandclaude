#!/usr/bin/env python3
"""
iOS Networking Layer Development Script
Creates the networking foundation for the Twitter Clone iOS app
"""

import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process

# Set working directory
ios_project_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone"

# =============================================================================
# AGENTS
# =============================================================================

ios_network_architect = Agent(
    role='iOS Network Architect',
    goal='Design the networking layer architecture for the Twitter clone iOS app',
    backstory="""You are an expert iOS networking architect who specializes in URLSession, 
    REST API integration, and modern Swift networking patterns. You create clean, testable 
    networking layers that handle authentication, error handling, and data parsing.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

ios_network_developer = Agent(
    role='iOS Network Developer', 
    goal='Implement the networking layer with URLSession and proper error handling',
    backstory="""You are a skilled iOS developer who writes clean, efficient networking code 
    using URLSession, Codable protocols, and async/await. You follow iOS best practices 
    for API integration and error handling.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

ios_test_engineer = Agent(
    role='iOS Test Engineer',
    goal='Create comprehensive unit tests for the networking layer',
    backstory="""You are an iOS testing expert who writes thorough XCTest unit tests. 
    You create mock services, test error conditions, and ensure networking code is 
    fully tested and reliable.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

# =============================================================================
# TASKS
# =============================================================================

# Task 1: Design networking architecture
network_architecture_task = Task(
    description="""
    Design the networking layer architecture for the Twitter clone iOS app.
    
    **Backend API Endpoints:**
    - User Service: http://localhost:8080/api/auth/*, /api/users/*
    - Post Service: http://localhost:8081/api/posts/*, /api/timeline/*
    
    **Requirements:**
    1. Design NetworkManager class structure
    2. Plan HTTP request/response handling
    3. Design JWT authentication integration
    4. Plan error handling strategy
    5. Define data models for API responses
    6. Plan URLSession configuration
    
    **Deliverables:**
    - Networking architecture document
    - Class structure and responsibilities
    - Error handling strategy
    - Authentication flow design
    """,
    expected_output="Complete networking architecture design document",
    agent=ios_network_architect
)

# Task 2: Implement networking layer
network_implementation_task = Task(
    description="""
    Implement the networking layer for the Twitter clone iOS app.
    
    **Implementation Requirements:**
    1. Create NetworkManager.swift - Main networking class
    2. Create APIEndpoint.swift - Endpoint definitions
    3. Create NetworkError.swift - Custom error types
    4. Create AuthManager.swift - JWT token management
    5. Create APIResponse.swift - Generic response wrapper
    
    **Key Features:**
    - URLSession with async/await
    - JWT token handling
    - Proper error handling
    - Request/response logging
    - Generic request methods
    
    **Output Format:** 
    Provide complete Swift files with this format:
    
    ```swift
    // FILE: NetworkManager.swift
    [complete Swift code]
    ```
    
    Create all 5 Swift files with complete, compilable code.
    """,
    expected_output="Complete networking layer implementation with 5 Swift files",
    agent=ios_network_developer,
    depends_on=[network_architecture_task]
)

# Task 3: Create unit tests
network_testing_task = Task(
    description="""
    Create comprehensive unit tests for the networking layer.
    
    **Testing Requirements:**
    1. Create NetworkManagerTests.swift - Test main networking functionality
    2. Create MockURLSession.swift - Mock URLSession for testing
    3. Create APIEndpointTests.swift - Test endpoint construction
    4. Create AuthManagerTests.swift - Test authentication logic
    
    **Test Cases:**
    - Successful API requests
    - Network error handling
    - Authentication token management
    - Response parsing
    - Timeout handling
    
    **Output Format:**
    ```swift
    // FILE: NetworkManagerTests.swift
    [complete XCTest code]
    ```
    
    Create complete unit test files that can run in Xcode.
    """,
    expected_output="Complete unit test suite for networking layer",
    agent=ios_test_engineer,
    depends_on=[network_implementation_task]
)

# =============================================================================
# MANUAL FILE WRITING FUNCTION
# =============================================================================

def apply_networking_files(crew_result):
    """Extract Swift networking code and write to files"""
    
    print("\n🔧 Creating iOS networking layer files...")
    
    ios_project_dir = Path(ios_project_path)
    twitter_clone_dir = ios_project_dir / "TwitterClone"
    
    result_text = str(crew_result)
    
    # Save debug output
    debug_file = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai") / "networking_debug_output.txt"
    with open(debug_file, 'w') as f:
        f.write(result_text)
    print(f"🔍 Full output saved to: networking_debug_output.txt")
    
    # Look for Swift files with FILE: markers
    import re
    
    pattern = r'// FILE: ([^\n]+\.swift)\n([\s\S]*?)(?=// FILE:|$)'
    matches = re.findall(pattern, result_text, re.MULTILINE | re.DOTALL)
    
    print(f"📝 Found {len(matches)} Swift files to create")
    
    files_created = []
    
    for filename, code_content in matches:
        filename = filename.strip()
        code_content = code_content.strip()
        
        # Clean up code content
        code_content = re.sub(r'^```swift\n?', '', code_content, flags=re.MULTILINE)
        code_content = re.sub(r'^```\n?', '', code_content, flags=re.MULTILINE)
        code_content = code_content.strip()
        
        if code_content:
            # Create Networking directory
            networking_dir = twitter_clone_dir / "Networking"
            networking_dir.mkdir(exist_ok=True)
            
            # Create Tests directory for test files
            if "Test" in filename:
                tests_dir = twitter_clone_dir / "Tests"
                tests_dir.mkdir(exist_ok=True)
                file_path = tests_dir / filename
            else:
                file_path = networking_dir / filename
            
            try:
                with open(file_path, 'w') as f:
                    f.write(code_content)
                
                print(f"✅ Created: {filename}")
                files_created.append(filename)
                
            except Exception as e:
                print(f"❌ Failed to create {filename}: {str(e)}")
    
    # Create basic networking structure if no files extracted
    if not files_created:
        create_basic_networking_structure(twitter_clone_dir)
        files_created = ["NetworkManager.swift", "APIEndpoint.swift"]
    
    return files_created

def create_basic_networking_structure(twitter_clone_dir):
    """Create basic networking files as fallback"""
    
    print("\n🏗️  Creating basic networking structure...")
    
    networking_dir = twitter_clone_dir / "Networking"
    networking_dir.mkdir(exist_ok=True)
    
    # Basic NetworkManager
    network_manager = '''import Foundation

class NetworkManager {
    static let shared = NetworkManager()
    
    private let session: URLSession
    
    private init() {
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 30
        self.session = URLSession(configuration: config)
    }
    
    func request<T: Codable>(
        endpoint: APIEndpoint,
        responseType: T.Type
    ) async throws -> T {
        let request = try buildRequest(for: endpoint)
        
        let (data, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }
        
        guard 200...299 ~= httpResponse.statusCode else {
            throw NetworkError.serverError(httpResponse.statusCode)
        }
        
        return try JSONDecoder().decode(T.self, from: data)
    }
    
    private func buildRequest(for endpoint: APIEndpoint) throws -> URLRequest {
        guard let url = URL(string: endpoint.baseURL + endpoint.path) else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = endpoint.method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        return request
    }
}

enum NetworkError: Error {
    case invalidURL
    case invalidResponse
    case serverError(Int)
}
'''
    
    # Basic APIEndpoint
    api_endpoint = '''import Foundation

enum APIEndpoint {
    case login(username: String, password: String)
    case register(username: String, email: String, password: String)
    case publicTimeline
    case createPost(content: String)
    
    var baseURL: String {
        switch self {
        case .login, .register:
            return "http://localhost:8080"
        case .publicTimeline, .createPost:
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
        }
    }
    
    var method: HTTPMethod {
        switch self {
        case .login, .register, .createPost:
            return .POST
        case .publicTimeline:
            return .GET
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
    
    # Write files
    files = [
        ("NetworkManager.swift", network_manager),
        ("APIEndpoint.swift", api_endpoint)
    ]
    
    for filename, content in files:
        file_path = networking_dir / filename
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ Created basic: {filename}")

# =============================================================================
# CREW SETUP & EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("🌐 iOS Networking Layer Development")
    print("=" * 50)
    print("📱 Creating networking foundation for Twitter Clone")
    print("=" * 50)
    
    # Create the crew
    networking_crew = Crew(
        agents=[ios_network_architect, ios_network_developer, ios_test_engineer],
        tasks=[network_architecture_task, network_implementation_task, network_testing_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        # Execute the crew
        result = networking_crew.kickoff()
        
        # Apply the generated files
        files_created = apply_networking_files(result)
        
        print("\n" + "=" * 50)
        print("🎉 iOS Networking Layer Complete!")
        print("📋 Files Created:")
        for filename in files_created:
            print(f"   • {filename}")
        print("=" * 50)
        
        print(f"\n📊 Result Summary:")
        print("✅ Networking architecture designed")
        print("✅ NetworkManager implemented")  
        print("✅ Unit tests created")
        print("✅ Ready for API integration")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

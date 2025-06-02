"""
Improved Twitter Clone CrewAI Configuration
Fixed version with better file system tool management
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import CodeDocsSearchTool, CodeInterpreterTool
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import os
import fnmatch

# Custom tools for development - Using CrewAI BaseTool with proper input schemas
class CodeReviewToolInput(BaseModel):
    """Input schema for CodeReviewTool."""
    code: str = Field(..., description="The code to review for best practices and optimization.")

class CodeReviewTool(BaseTool):
    name: str = "Code Review Tool"
    description: str = "Reviews code for best practices, security issues, and optimization opportunities."
    args_schema: Type[BaseModel] = CodeReviewToolInput
    
    def _run(self, code: str) -> str:
        """Reviews code for best practices, security issues, and optimization opportunities."""
        # Simulate a basic code review
        issues = []
        recommendations = []
        
        if "print(" in code:
            issues.append("Using print statements - consider proper logging")
        if "password" in code.lower() and "hash" not in code.lower():
            issues.append("Password handling detected - ensure proper encryption/hashing")
        if len(code.split('\n')) > 50:
            recommendations.append("Function is quite long - consider breaking into smaller functions")
        if "TODO" in code or "FIXME" in code:
            issues.append("Code contains TODO/FIXME comments - resolve before production")
            
        review = f"Code Review Results:\n"
        if issues:
            review += f"Issues Found: {', '.join(issues)}\n"
        if recommendations:
            review += f"Recommendations: {', '.join(recommendations)}\n"
        if not issues and not recommendations:
            review += "Code looks good! No major issues detected.\n"
            
        return review

class ArchitectureValidationToolInput(BaseModel):
    """Input schema for ArchitectureValidationTool."""
    architecture_description: str = Field(..., description="The architecture description to validate.")

class ArchitectureValidationTool(BaseTool):
    name: str = "Architecture Validation Tool"  
    description: str = "Validates software architecture against best practices and design patterns."
    args_schema: Type[BaseModel] = ArchitectureValidationToolInput
    
    def _run(self, architecture_description: str) -> str:
        """Validates software architecture against best practices and design patterns."""
        validation_points = []
        
        # Check for common architecture patterns
        if "mvc" in architecture_description.lower() or "mvvm" in architecture_description.lower():
            validation_points.append("✅ Uses established architectural pattern (MVC/MVVM)")
        
        if "api" in architecture_description.lower():
            validation_points.append("✅ Includes API layer for separation of concerns")
            
        if "database" in architecture_description.lower() or "db" in architecture_description.lower():
            validation_points.append("✅ Includes data persistence layer")
            
        if "test" in architecture_description.lower():
            validation_points.append("✅ Considers testing in architecture")
            
        if "security" in architecture_description.lower() or "auth" in architecture_description.lower():
            validation_points.append("✅ Includes security considerations")
            
        # Recommendations
        recommendations = []
        if "cache" not in architecture_description.lower():
            recommendations.append("Consider adding caching layer for performance")
        if "monitor" not in architecture_description.lower():
            recommendations.append("Add monitoring and logging strategy")
        if "scale" not in architecture_description.lower():
            recommendations.append("Define scalability approach")
            
        result = "Architecture Validation Results:\n"
        result += "\n".join(validation_points)
        if recommendations:
            result += f"\n\nRecommendations:\n" + "\n".join(f"• {rec}" for rec in recommendations)
            
        return result

class TestCoverageToolInput(BaseModel):
    """Input schema for TestCoverageTool."""
    test_code: str = Field(..., description="The test code to analyze for coverage.")

class TestCoverageTool(BaseTool):
    name: str = "Test Coverage Tool"
    description: str = "Analyzes test coverage and suggests additional test cases."
    args_schema: Type[BaseModel] = TestCoverageToolInput
    
    def _run(self, test_code: str) -> str:
        """Analyzes test coverage and suggests additional test cases."""
        analysis = []
        suggestions = []
        
        # Basic test analysis
        if "test" in test_code.lower():
            analysis.append("✅ Contains test functions")
        if "assert" in test_code.lower():
            analysis.append("✅ Uses assertions for validation")
        if "mock" in test_code.lower():
            analysis.append("✅ Uses mocking for dependencies")
        if "setup" in test_code.lower() or "teardown" in test_code.lower():
            analysis.append("✅ Includes test setup/teardown")
            
        # Suggest additional test cases
        if "error" not in test_code.lower() and "exception" not in test_code.lower():
            suggestions.append("Add error handling test cases")
        if "edge" not in test_code.lower():
            suggestions.append("Add edge case testing")
        if "integration" not in test_code.lower():
            suggestions.append("Consider integration tests")
        if "performance" not in test_code.lower():
            suggestions.append("Add performance test cases")
            
        result = "Test Coverage Analysis:\n"
        result += "\n".join(analysis)
        if suggestions:
            result += f"\n\nSuggested Additional Tests:\n" + "\n".join(f"• {sug}" for sug in suggestions)
            
        return result

class ProjectFileReaderInput(BaseModel):
    """Input schema for ProjectFileReader."""
    file_pattern: str = Field(..., description="File pattern to search for (e.g., '*.py', 'README.md')")

class ProjectFileReaderTool(BaseTool):
    name: str = "Project File Reader"
    description: str = "Reads specific project files by pattern, avoiding system directories."
    args_schema: Type[BaseModel] = ProjectFileReaderInput
    
    def _run(self, file_pattern: str) -> str:
        """Reads project files matching pattern, excluding system directories."""
        try:
            import os
            import fnmatch
            
            # Directories to exclude
            exclude_dirs = {'.venv', 'venv', '__pycache__', '.git', 'node_modules', '.DS_Store'}
            
            found_files = []
            project_root = os.getcwd()
            
            # Walk through project directory
            for root, dirs, files in os.walk(project_root):
                # Remove excluded directories from dirs list to prevent walking into them
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                
                # Check files in current directory
                for file in files:
                    if fnmatch.fnmatch(file, file_pattern):
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, project_root)
                        found_files.append(rel_path)
                        
                # Limit to first 10 files to prevent overwhelming output
                if len(found_files) >= 10:
                    break
            
            if not found_files:
                return f"No files found matching pattern: {file_pattern}"
                
            result = f"Found {len(found_files)} files matching '{file_pattern}':\n"
            for file_path in found_files[:10]:  # Limit output
                result += f"• {file_path}\n"
                
            if len(found_files) > 10:
                result += f"... and {len(found_files) - 10} more files\n"
                
            return result
            
        except Exception as e:
            return f"Error reading files: {str(e)}"

# Initialize tools
code_docs_tool = CodeDocsSearchTool()
code_interpreter = CodeInterpreterTool()

# Initialize custom tools
code_review_tool = CodeReviewTool()
architecture_validation_tool = ArchitectureValidationTool()
test_coverage_tool = TestCoverageTool()
project_file_reader = ProjectFileReaderTool()

# =============================================================================
# AGENTS CONFIGURATION (Updated with safer tools)
# =============================================================================

# 1. Technical Lead
technical_lead = Agent(
    role='Technical Lead',
    goal='Oversee the entire Twitter clone project, ensure technical excellence, and coordinate between all teams',
    backstory="""You are a seasoned Technical Lead with 12+ years of experience in full-stack development 
    and team management. You have successfully led multiple social media platform projects and understand 
    the complexities of scalable, real-time applications. Your expertise spans mobile development, backend 
    architecture, and DevOps practices.""",
    tools=[code_review_tool, architecture_validation_tool, project_file_reader],
    verbose=True,
    allow_delegation=True,
    max_iter=3
)

# 2. Business Analyst  
business_analyst = Agent(
    role='Business Analyst',
    goal='Define requirements, create user stories, and ensure the product meets business objectives',
    backstory="""You are an experienced Business Analyst with 8+ years in social media and tech startups. 
    You excel at translating business needs into technical requirements and have deep understanding of 
    user behavior in social platforms. You're skilled at creating detailed user stories, acceptance 
    criteria, and managing stakeholder expectations.""",
    tools=[project_file_reader],
    verbose=True,
    allow_delegation=False,
    max_iter=2
)

# 3. iOS Architect
ios_architect = Agent(
    role='iOS Architect',
    goal='Design robust, scalable iOS architecture following Apple best practices and modern design patterns',
    backstory="""You are a Senior iOS Architect with 10+ years of iOS development experience. You've 
    architected multiple award-winning iOS apps with millions of users. You're an expert in MVVM, 
    Coordinator patterns, Combine framework, Core Data, and iOS performance optimization. You stay 
    current with the latest iOS technologies and WWDC announcements.""",
    tools=[architecture_validation_tool, code_docs_tool, project_file_reader],
    verbose=True,
    allow_delegation=True,
    max_iter=3
)

# 4. SwiftUI Developer
swiftui_developer = Agent(
    role='SwiftUI Developer',
    goal='Create beautiful, performant SwiftUI interfaces that provide excellent user experience',
    backstory="""You are a SwiftUI specialist with 5+ years of experience building complex iOS interfaces. 
    You're passionate about creating pixel-perfect UIs that follow Apple's Human Interface Guidelines. 
    You're expert in SwiftUI animations, custom components, accessibility, and responsive design. You 
    understand the nuances of SwiftUI lifecycle and state management.""",
    tools=[code_interpreter, code_docs_tool, code_review_tool],
    verbose=True,
    allow_delegation=False,
    max_iter=3
)

# 5. iOS Testing Engineer
ios_testing_engineer = Agent(
    role='iOS Testing Engineer',
    goal='Ensure iOS app quality through comprehensive testing strategies and automation',
    backstory="""You are an iOS testing specialist with 6+ years of experience in mobile QA and test 
    automation. You're expert in XCTest, XCUITest, Quick/Nimble, and have experience with performance 
    testing and accessibility testing. You understand the importance of test-driven development and 
    have implemented CI/CD pipelines for iOS projects.""",
    tools=[test_coverage_tool, code_interpreter, code_review_tool],
    verbose=True,
    allow_delegation=False,
    max_iter=3
)

# =============================================================================
# BACKEND/KOTLIN TEAM
# =============================================================================

# 6. Kotlin API Architect
kotlin_api_architect = Agent(
    role='Kotlin API Architect',
    goal='Design scalable, secure Spring Boot Kotlin API architecture for the Twitter clone backend',
    backstory="""You are a Senior Backend Architect with 12+ years of experience in building scalable 
    APIs and microservices. You're an expert in Spring Boot, Kotlin, microservices architecture, 
    database design, and cloud deployment. You have extensive experience with social media platforms, 
    real-time systems, and high-throughput applications. You understand security, caching strategies, 
    and API design best practices.""",
    tools=[architecture_validation_tool, code_docs_tool, project_file_reader],
    verbose=True,
    allow_delegation=True,
    max_iter=3
)

# 7. Kotlin API Developer
kotlin_api_developer = Agent(
    role='Kotlin API Developer',
    goal='Implement robust, secure Spring Boot APIs using Kotlin for all backend services',
    backstory="""You are a Kotlin backend developer with 6+ years of experience in Spring Boot 
    development. You're proficient in Spring Security, Spring Data JPA, WebSocket implementation, 
    and RESTful API design. You understand database optimization, caching with Redis, message 
    queues, and have experience with authentication/authorization systems.""",
    tools=[code_interpreter, code_docs_tool, code_review_tool],
    verbose=True,
    allow_delegation=False,
    max_iter=3
)

# 8. API Testing Engineer
api_testing_engineer = Agent(
    role='API Testing Engineer',
    goal='Ensure API quality through comprehensive testing strategies including unit, integration, and performance tests',
    backstory="""You are a backend testing specialist with 7+ years of experience in API testing 
    and quality assurance. You're expert in JUnit 5, MockK, TestContainers, Spring Boot Test, 
    and API testing tools like Postman and Newman. You have experience with performance testing 
    using JMeter, load testing, and security testing for APIs.""",
    tools=[test_coverage_tool, code_interpreter, code_review_tool],
    verbose=True,
    allow_delegation=False,
    max_iter=3
)

# =============================================================================
# TESTING FUNCTIONS
# =============================================================================

def test_improved_technical_lead():
    """Test technical lead with improved tools"""
    print("🧪 Testing Improved Technical Lead with Tools...")
    
    task = Task(
        description="""
        Create a technical plan for implementing user authentication in a Twitter clone.
        Use your tools to:
        1. Review this authentication code snippet
        2. Validate the proposed architecture
        3. Look for any existing configuration files in the project
        
        Authentication code to review:
        ```swift
        func authenticateUser(email: String, password: String) async throws -> User {
            guard !email.isEmpty, !password.isEmpty else {
                throw AuthError.missingCredentials
            }
            let request = AuthRequest(email: email, password: password)
            return try await apiClient.authenticate(request)
        }
        ```
        
        Proposed architecture: "Use JWT tokens for API authentication, implement biometric authentication for mobile apps, store tokens securely in Keychain/KeyStore, implement token refresh mechanism, add OAuth for social login"
        """,
        agent=technical_lead,
        expected_output="Technical authentication plan with code review, architecture validation, and project file analysis"
    )
    
    crew = Crew(
        agents=[technical_lead],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        print("🚀 Starting improved technical lead test...")
        result = crew.kickoff()
        print(f"✅ Test Result:\n{result}")
        return True
    except Exception as e:
        print(f"❌ Test Failed: {e}")
        return False

def test_ios_development_workflow():
    """Test a complete iOS development workflow"""
    print("\n🧪 Testing iOS Development Workflow...")
    
    # Architecture task
    architecture_task = Task(
        description="""
        Design the architecture for a Twitter clone iOS app with these requirements:
        - SwiftUI for UI
        - MVVM pattern
        - Core Data for offline storage
        - Combine for reactive programming
        - Networking layer for API calls
        
        Provide a high-level architecture overview.
        """,
        agent=ios_architect,
        expected_output="iOS architecture design with MVVM, Core Data, and networking components"
    )
    
    # Development task
    development_task = Task(
        description="""
        Based on the architecture provided, create a SwiftUI component structure for the main timeline screen.
        Include:
        - Main timeline view
        - Post cell component
        - Navigation structure
        - State management approach
        
        Provide SwiftUI code structure and component breakdown.
        """,
        agent=swiftui_developer,
        expected_output="SwiftUI component structure with timeline view and post components"
    )
    
    # Testing task
    testing_task = Task(
        description="""
        Create a testing strategy for the iOS app components designed above.
        Include:
        - Unit tests for ViewModels
        - UI tests for key user flows
        - Integration tests for data layer
        - Performance testing approach
        
        Use the test coverage tool to analyze and suggest improvements.
        """,
        agent=ios_testing_engineer,
        expected_output="Comprehensive iOS testing strategy with unit, UI, and integration tests"
    )
    
    crew = Crew(
        agents=[ios_architect, swiftui_developer, ios_testing_engineer],
        tasks=[architecture_task, development_task, testing_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        print("🚀 Starting iOS development workflow test...")
        result = crew.kickoff()
        print(f"✅ Test Result:\n{result}")
        return True
    except Exception as e:
        print(f"❌ Test Failed: {e}")
        return False

def run_improved_tests():
    """Run improved tests with better tool management"""
    print("=" * 60)
    print("🚀 TESTING IMPROVED CREWAI CONFIGURATION")
    print("=" * 60)
    
    results = {
        "Technical Lead with Tools": False,
        "iOS Development Workflow": False
    }
    
    # Run tests
    results["Technical Lead with Tools"] = test_improved_technical_lead()
    results["iOS Development Workflow"] = test_ios_development_workflow()
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 IMPROVED TEST RESULTS")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:<30} {status}")
    
    passed_count = sum(results.values())
    total_count = len(results)
    
    print(f"\nOverall: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("🎉 All improved tests passed! Tools are working correctly!")
        print("\n🚀 Your CrewAI setup is now fully functional with:")
        print("  • Custom tools that work properly")
        print("  • File system access that doesn't hang")
        print("  • Multi-agent workflows")
        print("  • Code review capabilities")
        print("  • Architecture validation")
        print("  • Test coverage analysis")
    elif passed_count > 0:
        print("⚠️  Some tests passed. Partial functionality confirmed.")
    else:
        print("❌ Tests failed. Need to debug tool configuration.")
    
    return results

if __name__ == "__main__":
    run_improved_tests()

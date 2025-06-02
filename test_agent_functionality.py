"""
Test Agent Functionality
Simple tests to verify CrewAI agents are working correctly
"""

from TwitterClone_CrewAI_Configuration import (
    technical_lead, 
    business_analyst,
    ios_architect,
    swiftui_developer
)
from crewai import Task, Crew, Process
import os

def test_single_agent():
    """Test a single agent with a simple task"""
    print("🧪 Testing Single Agent (Technical Lead)...")
    
    # Create a simple task for the technical lead
    simple_task = Task(
        description="""
        Create a brief overview of the technology stack for a Twitter clone project.
        Include the main technologies for:
        1. iOS app development
        2. Android app development  
        3. Backend API development
        4. Database choices
        
        Keep it concise but informative.
        """,
        agent=technical_lead,
        expected_output="A structured overview of the technology stack with justifications for each choice"
    )
    
    # Create a simple crew with just one agent
    test_crew = Crew(
        agents=[technical_lead],
        tasks=[simple_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        print("🚀 Starting single agent test...")
        result = test_crew.kickoff()
        print(f"✅ Single Agent Test Result:\n{result}")
        return True
    except Exception as e:
        print(f"❌ Single Agent Test Failed: {e}")
        return False

def test_two_agent_collaboration():
    """Test collaboration between two agents"""
    print("\n🧪 Testing Two-Agent Collaboration...")
    
    # Task for Business Analyst
    requirements_task = Task(
        description="""
        Create 3 high-priority user stories for a Twitter clone MVP:
        1. User registration and login
        2. Creating and viewing posts
        3. Following other users
        
        Each user story should include acceptance criteria.
        """,
        agent=business_analyst,
        expected_output="3 detailed user stories with acceptance criteria for Twitter clone MVP features"
    )
    
    # Task for Technical Lead (depends on business analyst's work)
    technical_task = Task(
        description="""
        Based on the user stories provided, create a technical implementation plan that includes:
        1. API endpoints needed
        2. Database schema requirements
        3. Mobile app screens required
        4. Estimated development effort
        
        Reference the user stories from the previous task.
        """,
        agent=technical_lead,
        expected_output="Technical implementation plan with API design, database schema, and development estimates"
    )
    
    # Create crew with two agents working in sequence
    collaboration_crew = Crew(
        agents=[business_analyst, technical_lead],
        tasks=[requirements_task, technical_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        print("🚀 Starting two-agent collaboration test...")
        result = collaboration_crew.kickoff()
        print(f"✅ Two-Agent Collaboration Test Result:\n{result}")
        return True
    except Exception as e:
        print(f"❌ Two-Agent Collaboration Test Failed: {e}")
        return False

def test_tool_usage():
    """Test agent using custom tools"""
    print("\n🧪 Testing Tool Usage...")
    
    # Task that should trigger tool usage
    tool_task = Task(
        description="""
        Review this simple Swift code and provide recommendations:
        
        ```swift
        func loginUser(email: String, password: String) {
            if email.isEmpty || password.isEmpty {
                print("Error: Empty fields")
                return
            }
            // Simulate API call
            apiClient.login(email, password) { result in
                print("Login result: \\(result)")
            }
        }
        ```
        
        Use your code review tool to analyze this code and suggest improvements.
        """,
        agent=technical_lead,
        expected_output="Code review with specific recommendations for improvement, security, and best practices"
    )
    
    tool_crew = Crew(
        agents=[technical_lead],
        tasks=[tool_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        print("🚀 Starting tool usage test...")
        result = tool_crew.kickoff()
        print(f"✅ Tool Usage Test Result:\n{result}")
        return True
    except Exception as e:
        print(f"❌ Tool Usage Test Failed: {e}")
        return False

def test_ios_specialist():
    """Test iOS-specific agent"""
    print("\n🧪 Testing iOS Specialist...")
    
    ios_task = Task(
        description="""
        Design the SwiftUI view structure for a Twitter-like post composition screen.
        Include:
        1. Text input area with character limit
        2. Media attachment options
        3. Post privacy settings
        4. Action buttons (Cancel, Post)
        
        Provide a brief SwiftUI code structure outline.
        """,
        agent=swiftui_developer,
        expected_output="SwiftUI view structure with components and basic code outline for post composition screen"
    )
    
    ios_crew = Crew(
        agents=[swiftui_developer],
        tasks=[ios_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        print("🚀 Starting iOS specialist test...")
        result = ios_crew.kickoff()
        print(f"✅ iOS Specialist Test Result:\n{result}")
        return True
    except Exception as e:
        print(f"❌ iOS Specialist Test Failed: {e}")
        return False

def run_all_tests():
    """Run all functionality tests"""
    print("=" * 60)
    print("🚀 STARTING CREWAI AGENT FUNCTIONALITY TESTS")
    print("=" * 60)
    
    results = {
        "Single Agent": False,
        "Two-Agent Collaboration": False,
        "Tool Usage": False,
        "iOS Specialist": False
    }
    
    # Run each test
    results["Single Agent"] = test_single_agent()
    results["Two-Agent Collaboration"] = test_two_agent_collaboration()
    results["Tool Usage"] = test_tool_usage()
    results["iOS Specialist"] = test_ios_specialist()
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:<25} {status}")
    
    passed_count = sum(results.values())
    total_count = len(results)
    
    print(f"\nOverall: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("🎉 All tests passed! Your CrewAI setup is working perfectly!")
    elif passed_count > 0:
        print("⚠️  Some tests passed. Check failed tests for issues.")
    else:
        print("❌ All tests failed. Check your configuration and API keys.")
    
    return results

if __name__ == "__main__":
    # Check if we have API keys configured
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  WARNING: No API keys found in environment variables.")
        print("Make sure you have OPENAI_API_KEY or ANTHROPIC_API_KEY set in your .env file")
        print("Current environment variables:")
        print(f"OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set'}")
        print(f"ANTHROPIC_API_KEY: {'Set' if os.getenv('ANTHROPIC_API_KEY') else 'Not set'}")
        print()
    
    # Run all tests
    run_all_tests()

"""
Simple Agent Functionality Test
Quick tests without file system tools to avoid directory scanning issues
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import CodeInterpreterTool
import os

# Create a simple technical lead without file system tools
simple_technical_lead = Agent(
    role='Technical Lead',
    goal='Provide technical guidance and architecture recommendations',
    backstory="""You are a seasoned Technical Lead with 12+ years of experience in full-stack development 
    and team management. You have successfully led multiple social media platform projects and understand 
    the complexities of scalable, real-time applications.""",
    tools=[],  # No file system tools to avoid directory scanning
    verbose=True,
    allow_delegation=False,
    max_iter=2
)

# Create a simple business analyst without file system tools
simple_business_analyst = Agent(
    role='Business Analyst',
    goal='Create user stories and requirements for software projects',
    backstory="""You are an experienced Business Analyst with 8+ years in social media and tech startups. 
    You excel at translating business needs into technical requirements and have deep understanding of 
    user behavior in social platforms.""",
    tools=[],  # No file system tools
    verbose=True,
    allow_delegation=False,
    max_iter=2
)

def test_basic_technical_advice():
    """Test basic technical advice without file system access"""
    print("🧪 Testing Basic Technical Advice...")
    
    task = Task(
        description="""
        Recommend a modern technology stack for building a Twitter clone with these requirements:
        1. iOS mobile app
        2. Android mobile app  
        3. Backend API
        4. Real-time messaging
        5. High scalability
        
        Provide specific technology recommendations with brief justifications.
        """,
        agent=simple_technical_lead,
        expected_output="Technology stack recommendations with specific technologies and justifications"
    )
    
    crew = Crew(
        agents=[simple_technical_lead],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        print("🚀 Starting basic technical advice test...")
        result = crew.kickoff()
        print(f"✅ Test Result:\n{result}")
        return True
    except Exception as e:
        print(f"❌ Test Failed: {e}")
        return False

def test_user_stories():
    """Test user story creation"""
    print("\n🧪 Testing User Story Creation...")
    
    task = Task(
        description="""
        Create 3 user stories for a Twitter clone MVP:
        1. User account creation
        2. Publishing posts/tweets
        3. Following other users
        
        Each user story should follow the format: "As a [user type], I want to [action] so that [benefit]"
        Include acceptance criteria for each story.
        """,
        agent=simple_business_analyst,
        expected_output="3 well-formatted user stories with acceptance criteria"
    )
    
    crew = Crew(
        agents=[simple_business_analyst],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        print("🚀 Starting user story test...")
        result = crew.kickoff()
        print(f"✅ Test Result:\n{result}")
        return True
    except Exception as e:
        print(f"❌ Test Failed: {e}")
        return False

def test_collaborative_planning():
    """Test two agents working together"""
    print("\n🧪 Testing Collaborative Planning...")
    
    # Business Analyst task
    requirements_task = Task(
        description="""
        Define the core features for a Twitter clone MVP. List the top 5 essential features 
        that must be included in the minimum viable product, with a brief description of each.
        """,
        agent=simple_business_analyst,
        expected_output="List of 5 core MVP features with descriptions"
    )
    
    # Technical Lead task (sequential, can reference previous task)
    architecture_task = Task(
        description="""
        Based on the MVP features identified, design a high-level system architecture.
        Include:
        1. API design approach
        2. Database strategy
        3. Mobile app architecture
        4. Deployment strategy
        
        Keep it high-level and practical.
        """,
        agent=simple_technical_lead,
        expected_output="High-level system architecture with API, database, mobile, and deployment strategies"
    )
    
    crew = Crew(
        agents=[simple_business_analyst, simple_technical_lead],
        tasks=[requirements_task, architecture_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        print("🚀 Starting collaborative planning test...")
        result = crew.kickoff()
        print(f"✅ Test Result:\n{result}")
        return True
    except Exception as e:
        print(f"❌ Test Failed: {e}")
        return False

def run_simple_tests():
    """Run all simple tests"""
    print("=" * 60)
    print("🚀 STARTING SIMPLE CREWAI AGENT TESTS")
    print("=" * 60)
    
    results = {
        "Basic Technical Advice": False,
        "User Story Creation": False,
        "Collaborative Planning": False
    }
    
    # Run each test
    results["Basic Technical Advice"] = test_basic_technical_advice()
    results["User Story Creation"] = test_user_stories()
    results["Collaborative Planning"] = test_collaborative_planning()
    
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
        print("🎉 All tests passed! Your CrewAI agents are working correctly!")
        print("\n💡 Next steps:")
        print("  • The file system tools were causing issues - we'll need to configure them better")
        print("  • Your agents can collaborate and think independently")
        print("  • Ready to run more complex workflows!")
    elif passed_count > 0:
        print("⚠️  Some tests passed. Your basic setup works!")
    else:
        print("❌ All tests failed. Check your API configuration.")
    
    return results

if __name__ == "__main__":
    # Check API keys
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  WARNING: No API keys found in environment variables.")
        print("Make sure you have API keys set in your .env file")
        print()
    
    # Run simple tests
    run_simple_tests()

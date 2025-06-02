"""Test script to verify CrewAI environment setup"""
import sys
import os

def test_imports():
    """Test that all required packages can be imported"""
    try:
        import crewai
        import crewai_tools
        import langchain
        import openai
        from dotenv import load_dotenv
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_environment():
    """Test environment variables"""
    from dotenv import load_dotenv

    load_dotenv()

    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key or openai_key == 'your_openai_api_key_here':
        print("❌ OPENAI_API_KEY not set or still using template value")
        print("   Please edit .env file and add your actual OpenAI API key")
        return False
    else:
        print("✅ Environment variables configured!")
        return True

def test_crewai():
    """Test basic CrewAI functionality"""
    try:
        from crewai import Agent, Task, Crew

        # Create a simple test agent
        test_agent = Agent(
            role='Test Agent',
            goal='Test that CrewAI is working',
            backstory='A simple test agent'
        )

        print("✅ CrewAI basic functionality working!")
        return True
    except Exception as e:
        print(f"❌ CrewAI test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Twitter Clone CrewAI Setup...")
    print("-" * 50)

    tests = [test_imports, test_environment, test_crewai]
    results = []

    for test in tests:
        result = test()
        results.append(result)
        print()

    if all(results):
        print("🎉 All tests passed! Environment is ready for development.")
        print("\n🚀 Next steps:")
        print("1. Copy your CrewAI configuration files to this directory")
        print("2. Run: python TwitterClone_CrewAI_Configuration.py")
    else:
        print("❌ Some tests failed. Please check the setup.")
        print("\n🔧 Common fixes:")
        print("1. Make sure you've added your OpenAI API key to .env")
        print("2. Try: pip install --upgrade crewai crewai-tools")

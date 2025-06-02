#!/usr/bin/env python3
"""
CrewAI Script: Spring Boot Test Configuration Manager
This script manages Spring Boot test configurations and ensures best practices.
"""

from crewai import Agent, Task, Crew
from crewai.tools import tool
import os
import yaml
import subprocess
from pathlib import Path

@tool
def scan_spring_config_files(project_path: str) -> str:
    """Scan for Spring Boot configuration files and detect issues"""
    try:
        project_root = Path(project_path)
        config_files = []
        issues = []
        
        # Find all application*.yml files
        for root, dirs, files in os.walk(project_root):
            for file in files:
                if file.startswith('application') and (file.endswith('.yml') or file.endswith('.yaml')):
                    config_files.append(Path(root) / file)
        
        # Check each configuration file
        for config_file in config_files:
            try:
                with open(config_file, 'r') as f:
                    content = yaml.safe_load(f)
                
                filename = config_file.name
                is_profile_specific = '-' in filename and filename not in ['application.yml', 'application.yaml']
                
                if is_profile_specific and content and 'spring' in content:
                    spring_config = content['spring']
                    if 'profiles' in spring_config and 'active' in spring_config['profiles']:
                        profile_name = filename.split('-')[1].split('.')[0]
                        issues.append({
                            'file': str(config_file),
                            'profile': profile_name,
                            'issue': 'Profile-specific file contains spring.profiles.active',
                            'severity': 'HIGH'
                        })
            except Exception as e:
                issues.append({
                    'file': str(config_file),
                    'issue': f'Parse error: {str(e)}',
                    'severity': 'MEDIUM'
                })
        
        result = {
            'total_files': len(config_files),
            'issues': issues,
            'files_scanned': [str(f) for f in config_files]
        }
        
        return str(result)
        
    except Exception as e:
        return f"Error scanning configuration files: {str(e)}"

@tool
def fix_spring_config_issues(project_path: str) -> str:
    """Fix common Spring Boot configuration issues"""
    try:
        project_root = Path(project_path)
        fixed_files = []
        
        # Find all profile-specific application files
        for root, dirs, files in os.walk(project_root):
            for file in files:
                if (file.startswith('application-') and 
                    (file.endswith('.yml') or file.endswith('.yaml'))):
                    
                    config_file = Path(root) / file
                    
                    # Read the file
                    with open(config_file, 'r') as f:
                        lines = f.readlines()
                    
                    # Remove spring.profiles.active lines
                    new_lines = []
                    i = 0
                    while i < len(lines):
                        line = lines[i]
                        
                        # Check for spring.profiles.active pattern
                        if ('spring:' in line and 
                            i + 1 < len(lines) and 'profiles:' in lines[i + 1] and
                            i + 2 < len(lines) and 'active:' in lines[i + 2]):
                            
                            # Skip the spring.profiles.active block
                            new_lines.append('spring:\n')
                            i += 3  # Skip spring:, profiles:, and active: lines
                        elif ('profiles:' in line and 
                              i + 1 < len(lines) and 'active:' in lines[i + 1]):
                            # Skip profiles: and active: lines
                            i += 2
                        elif 'active:' in line and i > 0 and 'profiles:' in lines[i - 1]:
                            # Skip standalone active: line
                            i += 1
                        else:
                            new_lines.append(line)
                            i += 1
                    
                    # Write the fixed file
                    with open(config_file, 'w') as f:
                        f.writelines(new_lines)
                    
                    fixed_files.append(str(config_file))
        
        return f"Fixed {len(fixed_files)} configuration files: {fixed_files}"
        
    except Exception as e:
        return f"Error fixing configuration files: {str(e)}"

@tool
def run_gradle_clean(project_path: str) -> str:
    """Run gradle clean to clear build caches"""
    try:
        backend_path = Path(project_path) / "generated_code" / "backend"
        if not backend_path.exists():
            return "Backend directory not found"
        
        result = subprocess.run(
            ["./gradlew", "clean"],
            cwd=backend_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return "Successfully cleaned build directories"
        else:
            return f"Gradle clean failed: {result.stderr}"
            
    except Exception as e:
        return f"Error running gradle clean: {str(e)}"

@tool
def run_integration_tests(project_path: str, service: str = "user-service") -> str:
    """Run integration tests for a specific service"""
    try:
        backend_path = Path(project_path) / "generated_code" / "backend"
        if not backend_path.exists():
            return "Backend directory not found"
        
        result = subprocess.run(
            ["./gradlew", f":{service}:test", "--tests", "*IntegrationTest*", "--info"],
            cwd=backend_path,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        return f"Test execution completed with exit code {result.returncode}\n\nSTDOUT:\n{result.stdout[-1000:]}\n\nSTDERR:\n{result.stderr[-500:]}"
        
    except Exception as e:
        return f"Error running integration tests: {str(e)}"

# Define agents
config_analyst = Agent(
    role="Spring Boot Configuration Analyst",
    goal="Analyze Spring Boot configuration files and identify issues",
    backstory="You are an expert in Spring Boot configuration management with deep knowledge of profile-specific configurations, testing setups, and common pitfalls.",
    verbose=True
)

config_fixer = Agent(
    role="Configuration Fix Specialist",
    goal="Fix Spring Boot configuration issues automatically",
    backstory="You specialize in automatically fixing common Spring Boot configuration problems, especially those related to profile management and test configurations.",
    verbose=True
)

test_runner = Agent(
    role="Test Execution Specialist", 
    goal="Execute integration tests and validate fixes",
    backstory="You are responsible for running integration tests and ensuring that configuration fixes resolve the underlying issues.",
    verbose=True
)

# Define tasks
analysis_task = Task(
    description="""
    Analyze the Spring Boot project configuration files and identify any issues:
    1. Scan all application*.yml files in the project
    2. Identify profile-specific configuration issues
    3. Look for improper use of spring.profiles.active in profile-specific files
    4. Report any parsing errors or malformed configurations
    
    Project path: /Users/garethhallberg/Desktop/twitter-clone-crewai
    """,
    agent=config_analyst,
    tools=[scan_spring_config_files]
)

fix_task = Task(
    description="""
    Fix the identified Spring Boot configuration issues:
    1. Remove spring.profiles.active from profile-specific configuration files
    2. Ensure proper YAML structure after modifications
    3. Clean build directories to remove cached configurations
    4. Verify that @ActiveProfiles annotations are used correctly in test classes
    
    Project path: /Users/garethhallberg/Desktop/twitter-clone-crewai
    """,
    agent=config_fixer,
    tools=[fix_spring_config_issues, run_gradle_clean]
)

test_task = Task(
    description="""
    Run integration tests to validate the configuration fixes:
    1. Execute integration tests for the user-service
    2. Verify that the Spring Boot application context loads correctly
    3. Confirm that the test profile is activated properly
    4. Report the test results and any remaining issues
    
    Project path: /Users/garethhallberg/Desktop/twitter-clone-crewai
    """,
    agent=test_runner,
    tools=[run_integration_tests]
)

# Create and run the crew
crew = Crew(
    agents=[config_analyst, config_fixer, test_runner],
    tasks=[analysis_task, fix_task, test_task],
    verbose=True
)

if __name__ == "__main__":
    print("🚀 Starting Spring Boot Configuration Management...")
    result = crew.kickoff()
    print("\n✅ Configuration management completed!")
    print(result)

#!/usr/bin/env python3
"""
Advanced CrewAI Script: Twitter Clone Project Health Monitor
This script continuously monitors the Twitter clone project for configuration issues,
build problems, and maintains best practices across all services.
"""

from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
import os
import yaml
import subprocess
import json
from pathlib import Path
from datetime import datetime
import re

# Tools for project health monitoring
@tool
def scan_project_structure(project_path: str) -> str:
    """Scan the entire project structure and identify services and components"""
    try:
        project_root = Path(project_path)
        structure = {
            "backend_services": [],
            "client_apps": [],
            "config_files": [],
            "build_files": [],
            "test_files": []
        }
        
        # Scan backend services
        backend_path = project_root / "generated_code" / "backend"
        if backend_path.exists():
            for item in backend_path.iterdir():
                if item.is_dir() and (item / "build.gradle.kts").exists():
                    structure["backend_services"].append(str(item.name))
        
        # Scan for client applications
        clients_path = project_root / "generated_code"
        if clients_path.exists():
            for item in clients_path.iterdir():
                if item.name in ["ios", "android", "react"]:
                    structure["client_apps"].append(str(item.name))
        
        # Scan configuration files
        for root, dirs, files in os.walk(project_root):
            for file in files:
                if file.endswith(('.yml', '.yaml', '.properties')):
                    structure["config_files"].append(str(Path(root) / file))
                elif file.endswith(('.gradle.kts', '.gradle', 'build.gradle')):
                    structure["build_files"].append(str(Path(root) / file))
                elif 'test' in file.lower() and file.endswith(('.kt', '.java')):
                    structure["test_files"].append(str(Path(root) / file))
        
        return json.dumps(structure, indent=2)
        
    except Exception as e:
        return f"Error scanning project structure: {str(e)}"

@tool
def check_service_health(project_path: str, service_name: str) -> str:
    """Check the health of a specific backend service"""
    try:
        backend_path = Path(project_path) / "generated_code" / "backend"
        service_path = backend_path / service_name
        
        if not service_path.exists():
            return f"Service {service_name} not found"
        
        health_report = {
            "service": service_name,
            "config_issues": [],
            "build_status": "unknown",
            "test_status": "unknown",
            "dependencies": []
        }
        
        # Check configuration files
        test_config = service_path / "src" / "test" / "resources" / "application-test.yml"
        if test_config.exists():
            with open(test_config, 'r') as f:
                config = yaml.safe_load(f)
                if config and 'spring' in config:
                    spring_config = config['spring']
                    if 'profiles' in spring_config and 'active' in spring_config['profiles']:
                        health_report["config_issues"].append("Invalid spring.profiles.active in test config")
        
        # Check build status
        try:
            result = subprocess.run(
                ["./gradlew", f":{service_name}:compileKotlin", "--quiet"],
                cwd=backend_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            health_report["build_status"] = "success" if result.returncode == 0 else "failed"
        except:
            health_report["build_status"] = "error"
        
        # Check dependencies
        build_file = service_path / "build.gradle.kts"
        if build_file.exists():
            with open(build_file, 'r') as f:
                content = f.read()
                # Extract dependencies (simplified)
                deps = re.findall(r'implementation\("([^"]+)"\)', content)
                health_report["dependencies"] = deps[:10]  # Limit output
        
        return json.dumps(health_report, indent=2)
        
    except Exception as e:
        return f"Error checking service health: {str(e)}"

@tool
def run_comprehensive_tests(project_path: str) -> str:
    """Run comprehensive tests across all services"""
    try:
        backend_path = Path(project_path) / "generated_code" / "backend"
        test_results = {
            "overall_status": "unknown",
            "service_results": {},
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0
        }
        
        # Get list of services
        services = []
        for item in backend_path.iterdir():
            if item.is_dir() and (item / "build.gradle.kts").exists():
                services.append(item.name)
        
        # Run tests for each service
        for service in services:
            try:
                result = subprocess.run(
                    ["./gradlew", f":{service}:test", "--quiet"],
                    cwd=backend_path,
                    capture_output=True,
                    text=True,
                    timeout=180
                )
                
                service_status = "passed" if result.returncode == 0 else "failed"
                test_results["service_results"][service] = service_status
                
                # Parse test output for counts (simplified)
                if "tests completed" in result.stdout:
                    match = re.search(r'(\d+) tests completed', result.stdout)
                    if match:
                        test_results["total_tests"] += int(match.group(1))
                
            except Exception as e:
                test_results["service_results"][service] = f"error: {str(e)}"
        
        # Calculate overall status
        passed_services = sum(1 for status in test_results["service_results"].values() if status == "passed")
        total_services = len(test_results["service_results"])
        
        if passed_services == total_services:
            test_results["overall_status"] = "all_passed"
        elif passed_services > 0:
            test_results["overall_status"] = "partial_success"
        else:
            test_results["overall_status"] = "all_failed"
        
        return json.dumps(test_results, indent=2)
        
    except Exception as e:
        return f"Error running comprehensive tests: {str(e)}"

@tool
def generate_project_report(project_path: str) -> str:
    """Generate a comprehensive project health report"""
    try:
        report = {
            "timestamp": datetime.now().isoformat(),
            "project_path": project_path,
            "summary": {
                "total_services": 0,
                "healthy_services": 0,
                "config_issues": 0,
                "test_coverage": "unknown"
            },
            "recommendations": []
        }
        
        # Count services and basic metrics
        backend_path = Path(project_path) / "generated_code" / "backend"
        if backend_path.exists():
            services = [item.name for item in backend_path.iterdir() 
                       if item.is_dir() and (item / "build.gradle.kts").exists()]
            report["summary"]["total_services"] = len(services)
        
        # Add recommendations based on common issues
        report["recommendations"] = [
            "Ensure all services have proper integration tests",
            "Maintain consistent configuration patterns across services",
            "Regularly update dependencies to latest stable versions",
            "Implement proper logging and monitoring",
            "Use consistent error handling patterns",
            "Maintain API documentation with OpenAPI/Swagger"
        ]
        
        return json.dumps(report, indent=2)
        
    except Exception as e:
        return f"Error generating project report: {str(e)}"

@tool
def auto_fix_common_issues(project_path: str) -> str:
    """Automatically fix common configuration and build issues"""
    try:
        fixes_applied = []
        
        # Fix Spring Boot configuration issues
        backend_path = Path(project_path) / "generated_code" / "backend"
        if backend_path.exists():
            for service_dir in backend_path.iterdir():
                if service_dir.is_dir():
                    test_config = service_dir / "src" / "test" / "resources" / "application-test.yml"
                    if test_config.exists():
                        # Read and check for issues
                        with open(test_config, 'r') as f:
                            content = f.read()
                        
                        # Fix spring.profiles.active issue
                        if 'spring.profiles.active' in content:
                            # Remove the problematic lines
                            lines = content.split('\n')
                            fixed_lines = []
                            skip_next = False
                            
                            for i, line in enumerate(lines):
                                if skip_next:
                                    skip_next = False
                                    continue
                                    
                                if ('profiles:' in line and i + 1 < len(lines) and 
                                    'active:' in lines[i + 1]):
                                    skip_next = True
                                    continue
                                elif 'active:' in line and i > 0 and 'profiles:' in lines[i - 1]:
                                    continue
                                else:
                                    fixed_lines.append(line)
                            
                            # Write fixed content
                            with open(test_config, 'w') as f:
                                f.write('\n'.join(fixed_lines))
                            
                            fixes_applied.append(f"Fixed spring.profiles.active in {service_dir.name}")
        
        # Clean build directories
        try:
            result = subprocess.run(
                ["./gradlew", "clean"],
                cwd=backend_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                fixes_applied.append("Cleaned build directories")
        except:
            pass
        
        return f"Applied {len(fixes_applied)} fixes: {fixes_applied}"
        
    except Exception as e:
        return f"Error applying fixes: {str(e)}"

# Define specialized agents
project_architect = Agent(
    role="Senior Project Architect",
    goal="Analyze the overall architecture and structure of the Twitter clone project",
    backstory="You are a senior software architect with expertise in microservices, Spring Boot, and full-stack development. You understand the complexities of maintaining multi-service applications and mobile clients.",
    verbose=True
)

devops_specialist = Agent(
    role="DevOps and Build Specialist",
    goal="Ensure build processes, configurations, and deployment readiness",
    backstory="You specialize in build automation, CI/CD pipelines, and configuration management. You ensure that all services can be built, tested, and deployed reliably.",
    verbose=True
)

qa_engineer = Agent(
    role="Quality Assurance Engineer",
    goal="Validate functionality through comprehensive testing",
    backstory="You are responsible for ensuring code quality through automated testing, integration testing, and identifying potential issues before they reach production.",
    verbose=True
)

maintenance_expert = Agent(
    role="Project Maintenance Expert",
    goal="Keep the project healthy and apply best practices",
    backstory="You focus on long-term project health, applying fixes, maintaining consistency, and ensuring the project follows industry best practices.",
    verbose=True
)

# Define comprehensive tasks
architecture_analysis = Task(
    description="""
    Perform a comprehensive analysis of the Twitter clone project architecture:
    1. Scan the entire project structure
    2. Identify all backend services, client applications, and components
    3. Analyze the relationships between services
    4. Check for architectural consistency and best practices
    5. Identify potential scalability or maintainability issues
    
    Project location: /Users/garethhallberg/Desktop/twitter-clone-crewai
    """,
    agent=project_architect,
    tools=[scan_project_structure]
)

health_check_task = Task(
    description="""
    Check the health of all backend services:
    1. Verify configuration files for each service
    2. Check build status and compilation
    3. Analyze dependencies and potential conflicts
    4. Identify any service-specific issues
    5. Report on overall service ecosystem health
    
    Focus on: user-service, post-service, and any other discovered services
    """,
    agent=devops_specialist,
    tools=[check_service_health]
)

comprehensive_testing = Task(
    description="""
    Execute comprehensive testing across the project:
    1. Run unit tests for all services
    2. Execute integration tests
    3. Validate API endpoints and contracts
    4. Check test coverage and quality
    5. Identify failing tests and their root causes
    
    Provide detailed test results and recommendations for improvements.
    """,
    agent=qa_engineer,
    tools=[run_comprehensive_tests]
)

project_maintenance = Task(
    description="""
    Perform project maintenance and apply fixes:
    1. Automatically fix common configuration issues
    2. Clean build artifacts and caches
    3. Apply best practice improvements
    4. Generate recommendations for future maintenance
    5. Create a comprehensive project health report
    
    Focus on maintaining long-term project health and sustainability.
    """,
    agent=maintenance_expert,
    tools=[auto_fix_common_issues, generate_project_report]
)

# Create the maintenance crew
maintenance_crew = Crew(
    agents=[project_architect, devops_specialist, qa_engineer, maintenance_expert],
    tasks=[architecture_analysis, health_check_task, comprehensive_testing, project_maintenance],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    print("🚀 Starting Twitter Clone Project Health Monitoring...")
    print("=" * 60)
    
    result = maintenance_crew.kickoff()
    
    print("\n" + "=" * 60)
    print("✅ Project Health Monitoring Complete!")
    print("=" * 60)
    print(result)
    
    # Save results to file
    with open("/Users/garethhallberg/Desktop/twitter-clone-crewai/project_health_report.md", "w") as f:
        f.write(f"# Twitter Clone Project Health Report\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write(str(result))
    
    print(f"\n📊 Full report saved to: project_health_report.md")

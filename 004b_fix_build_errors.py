"""
004b_fix_build_errors.py - Build Error Analysis and Fix
Twitter Clone CrewAI Project - Phase 4b Fix

This script uses CrewAI agents to analyze build errors and generate fixes
for Gradle multi-module dependency issues and compilation problems.
"""

from improved_twitter_config import technical_lead, kotlin_api_architect, kotlin_api_developer
from crewai import Agent, Task, Crew, Process
from pathlib import Path

def analyze_and_fix_build_errors(error_output):
    """Use CrewAI agents to analyze build errors and generate fixes"""
    
    print("🔧 Starting Build Error Analysis with CrewAI...")
    print("=" * 80)
    print("🚨 PHASE 4b-FIX: Build Error Analysis & Resolution")
    print("=" * 80)
    print("CrewAI agents will analyze and fix build errors...")
    print("")

    # Task 1: Analyze Build Errors and Dependencies
    error_analysis_task = Task(
        description=f'''
        Analyze the following Gradle build errors and identify the root causes:
        
        BUILD ERRORS:
        {error_output}
        
        REQUIREMENTS:
        - Identify all compilation errors and their causes
        - Determine missing dependencies between modules
        - Identify Gradle configuration issues
        - Analyze multi-module dependency problems
        - Determine missing imports or classpath issues
        - Categorize errors by type (dependency, compilation, configuration)
        
        CRITICAL: Provide a detailed analysis of each error type and the fixes needed.
        
        Focus on:
        1. "Unresolved reference" errors - missing dependencies
        2. "Supertype initialization" errors - inheritance issues  
        3. Module dependency problems between common, user-service, post-service
        4. Missing Gradle build configurations
        5. Classpath and import resolution issues
        
        OUTPUT: Detailed error analysis with specific fixes needed for each issue.
        ''',
        agent=technical_lead,
        expected_output='Comprehensive analysis of build errors with categorized fixes needed'
    )

    # Task 2: Generate Gradle Configuration Fixes
    gradle_config_task = Task(
        description='''
        Generate corrected Gradle build files to fix multi-module dependency issues.
        
        REQUIREMENTS:
        Based on the error analysis, create these specific Gradle files:
        1. Updated root build.gradle.kts with proper module configuration
        2. common/build.gradle.kts - Library module without Spring Boot app
        3. user-service/build.gradle.kts - Service module depending on common
        4. post-service/build.gradle.kts - Service module depending on common
        
        CRITICAL: Provide complete, working Gradle build files.
        
        For root build.gradle.kts:
        - Configure subprojects with proper plugin applications
        - Set up common dependencies and repositories
        - Configure multi-module dependencies correctly
        
        For common/build.gradle.kts:
        - Library module configuration (no bootJar)
        - JPA and validation dependencies
        - Enable jar task, disable bootJar task
        
        For service modules:
        - Depend on project(":common")
        - Include Spring Boot application plugins
        - Add service-specific dependencies
        
        OUTPUT: Complete Gradle build files that resolve all dependency issues.
        ''',
        agent=kotlin_api_architect,
        expected_output='Complete Gradle build.gradle.kts files for root, common, user-service, and post-service modules'
    )

    # Task 3: Fix Entity and Repository Code Issues  
    code_fix_task = Task(
        description='''
        Generate fixes for Kotlin compilation errors in entity and repository classes.
        
        REQUIREMENTS:
        Based on the build errors, fix these specific code issues:
        1. Import statements for cross-module dependencies
        2. BaseEntity inheritance and constructor issues
        3. JPA annotation problems
        4. Repository interface compilation errors
        5. Missing dependencies in entity relationships
        
        CRITICAL: Provide corrected Kotlin code files.
        
        Focus on fixing:
        - Import statements for BaseEntity in User.kt and Post.kt
        - Proper inheritance syntax and constructor calls
        - Missing JPA plugin configuration effects
        - Repository method signatures and return types
        - Package structure and module boundaries
        
        Generate corrected versions of:
        1. BaseEntity.kt with proper JPA configuration
        2. User.kt with correct imports and inheritance
        3. Post.kt with correct imports and inheritance  
        4. UserRepository.kt with proper method signatures
        5. PostRepository.kt with proper method signatures
        
        OUTPUT: Corrected Kotlin entity and repository files that compile successfully.
        ''',
        agent=kotlin_api_developer,
        expected_output='Corrected Kotlin entity and repository files with proper imports and inheritance'
    )

    # Task 4: Generate Build Test and Verification
    verification_task = Task(
        description='''
        Create build verification steps and test commands to validate fixes.
        
        REQUIREMENTS:
        - Generate step-by-step build verification process
        - Create test commands to validate each module
        - Provide troubleshooting steps for common issues
        - Generate clean build process
        - Create dependency verification commands
        
        Generate verification steps that include:
        1. Clean build process (./gradlew clean)
        2. Individual module compilation tests
        3. Dependency resolution verification  
        4. Full build and test execution
        5. Troubleshooting commands for common failures
        
        OUTPUT: Complete build verification guide with commands and troubleshooting steps.
        ''',
        agent=technical_lead,
        expected_output='Complete build verification process with test commands and troubleshooting guide'
    )

    # Create the crew
    build_fix_crew = Crew(
        agents=[technical_lead, kotlin_api_architect, kotlin_api_developer],
        tasks=[error_analysis_task, gradle_config_task, code_fix_task, verification_task],
        process=Process.sequential,
        verbose=True
    )

    # Execute the crew
    print("🤖 CrewAI agents are analyzing build errors...")
    print("⏳ This may take a few minutes as agents generate fixes...")
    
    try:
        result = build_fix_crew.kickoff()
        
        # Save the results and apply fixes
        save_build_fix_results(result)
        
        print("\n" + "=" * 80)
        print("✅ BUILD ERROR ANALYSIS COMPLETE!")
        print("=" * 80)
        
        print("\n🎯 CrewAI agents have analyzed and generated fixes for:")
        print("  • Gradle multi-module dependency issues")
        print("  • Kotlin compilation errors")
        print("  • JPA entity inheritance problems")
        print("  • Repository interface issues")
        print("  • Import and classpath resolution")
        
        print("\n📁 Generated fixes saved to:")
        print("  • results/TwitterClone_BuildErrorFixes_Phase4b.md")
        
        print("\n🚀 Next Steps:")
        print("  • Review the generated fixes")
        print("  • Apply the corrected build files")
        print("  • Run the verification commands")
        print("  • Test: ./gradlew clean build")
        
        return {
            "status": "success", 
            "message": "Build error analysis completed successfully",
            "crew_output": str(result)
        }
        
    except Exception as e:
        print(f"\n❌ Error during build fix analysis: {str(e)}")
        return {
            "status": "error",
            "message": f"Build fix analysis failed: {str(e)}"
        }

def save_build_fix_results(crew_result):
    """Save the CrewAI build fix results"""
    
    # Ensure results directory exists
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    # Create comprehensive results file
    results_file = results_dir / "TwitterClone_BuildErrorFixes_Phase4b.md"
    
    with open(results_file, 'w') as f:
        f.write("# Twitter Clone - Build Error Fixes (Phase 4b)\n\n")
        f.write("*Generated by CrewAI Build Fix Team*\n\n")
        f.write("## Overview\n\n")
        f.write("This document contains the analysis and fixes for Gradle build errors ")
        f.write("in the Twitter Clone backend multi-module project.\n\n")
        f.write("## Build Error Analysis\n\n")
        f.write("### Agents Involved:\n")
        f.write("- **Technical Lead**: Analyzed errors and created verification process\n")
        f.write("- **Kotlin API Architect**: Fixed Gradle configuration issues\n") 
        f.write("- **Kotlin API Developer**: Corrected entity and repository code\n\n")
        f.write("### Error Categories Addressed:\n")
        f.write("1. **Multi-module Dependencies**: Cross-module reference issues\n")
        f.write("2. **Gradle Configuration**: Build file setup problems\n")
        f.write("3. **JPA Entity Issues**: Inheritance and annotation problems\n")
        f.write("4. **Import Resolution**: Missing imports and classpath issues\n")
        f.write("5. **Repository Interfaces**: Method signature problems\n\n")
        f.write("## CrewAI Analysis and Fixes\n\n")
        f.write("```\n")
        f.write(str(crew_result))
        f.write("\n```\n\n")
        f.write("## Application Instructions\n\n")
        f.write("1. Review the generated Gradle build files\n")
        f.write("2. Apply the corrected entity and repository code\n")
        f.write("3. Run the verification commands\n")
        f.write("4. Test the build with: `./gradlew clean build`\n")
        f.write("5. Run tests with: `./gradlew test`\n\n")
        f.write("---\n")
        f.write("*This analysis was generated using CrewAI agents specializing in Gradle and Kotlin development.*\n")
    
    print(f"✅ Build fix results saved to: {results_file.absolute()}")

if __name__ == "__main__":
    print("🔧 Twitter Clone - Build Error Analysis Phase")
    print("Using CrewAI agents to analyze and fix Gradle build errors")
    print("")
    
    # Get build error input
    print("Please paste the build error output below, then type 'END' on a new line:")
    print("=" * 60)
    
    error_lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END':
                break
            error_lines.append(line)
        except EOFError:
            break
    
    if not error_lines:
        print("No error output provided. Please run the script again with error output.")
        exit(1)
    
    error_output = '\n'.join(error_lines)
    
    # Run the build fix analysis
    result = analyze_and_fix_build_errors(error_output)
    
    if result["status"] == "success":
        print("\n🎉 Build error analysis completed successfully!")
        print("📋 Check the results directory for detailed fixes from CrewAI agents")
    else:
        print(f"\n💥 Build error analysis failed: {result['message']}")

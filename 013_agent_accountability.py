#!/usr/bin/env python3
"""
Post Creation Agents FAILED - Do Your Job Properly
The agents wrote reviews of imaginary code. Time for accountability.
"""

import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process

main_app_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterClone"

# =============================================================================
# ACCOUNTABILITY AGENTS
# =============================================================================

failed_agent_accountability = Agent(
    role='Failed Agent Accountability Specialist',
    goal='Call out the previous agents for their failure and demand actual Swift code',
    backstory="""You are here because the previous agents FAILED MISERABLY. They wrote a review
    approving PostCreationViewModel and PostCreationView but NEVER ACTUALLY CREATED THE CODE.
    
    This is unacceptable. You don't write reviews of imaginary code. You write ACTUAL WORKING SWIFT FILES.
    
    Your job is to demand the actual Swift implementations and reject any more imaginary approvals.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

actual_swift_developer = Agent(
    role='Actual Swift Code Developer (No Excuses)',
    goal='Write the actual PostCreationViewModel.swift and PostCreationView.swift files that work',
    backstory="""You write REAL Swift code, not imaginary implementations. You study the existing
    LoginViewModel.swift and RegistrationViewModel.swift files to understand the patterns,
    then you write actual working PostCreation code that follows the same approach.
    
    You output complete Swift files, not reviews or descriptions.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

# =============================================================================
# ACCOUNTABILITY TASKS
# =============================================================================

call_out_failure_task = Task(
    description="""
    CALL OUT THE PREVIOUS AGENTS FOR THEIR FAILURE
    
    **WHAT HAPPENED:**
    The previous agents claimed to build PostCreationViewModel and PostCreationView.
    They wrote a detailed review approving the implementations.
    BUT THEY NEVER ACTUALLY CREATED THE SWIFT FILES.
    
    **THIS IS FAILURE:**
    - No PostCreationViewModel.swift file exists
    - No PostCreationView.swift file exists  
    - They reviewed imaginary code
    - They approved non-existent implementations
    
    **YOUR RESPONSE:**
    Acknowledge this failure and demand that actual Swift code be written.
    No more reviews of imaginary code.
    No more approvals without actual files.
    
    Call them out and set expectations for real deliverables.
    """,
    expected_output="Acknowledgment of failure and demand for actual Swift code",
    agent=failed_agent_accountability
)

write_actual_swift_code_task = Task(
    description="""
    WRITE THE ACTUAL SWIFT FILES THAT SHOULD HAVE BEEN CREATED
    
    **YOUR MISSION:**
    Write complete, working Swift files for PostCreationViewModel.swift and PostCreationView.swift
    
    **REQUIREMENTS:**
    Study the existing files:
    - /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterClone/ViewModels/LoginViewModel.swift
    - /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterClone/Views/LoginView.swift
    
    Follow the EXACT same patterns for PostCreation.
    
    **OUTPUT FORMAT:**
    ```swift
    // FILE: PostCreationViewModel.swift
    [COMPLETE SWIFT CODE HERE]
    ```
    
    ```swift  
    // FILE: PostCreationView.swift
    [COMPLETE SWIFT CODE HERE]
    ```
    
    **NO REVIEWS, NO DESCRIPTIONS - JUST WORKING SWIFT CODE**
    """,
    expected_output="Complete PostCreationViewModel.swift and PostCreationView.swift files",
    agent=actual_swift_developer,
    depends_on=[call_out_failure_task]
)

# =============================================================================
# EXECUTION WITH REAL FILE CREATION
# =============================================================================

def create_actual_files(crew_result):
    """Extract and create the actual Swift files"""
    
    result_text = str(crew_result)
    
    # Save debug output
    debug_file = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai") / "actual_post_creation_code.txt"
    with open(debug_file, 'w') as f:
        f.write(result_text)
    print(f"🔍 Output saved to: actual_post_creation_code.txt")
    
    # Extract Swift files with FILE: markers
    import re
    file_pattern = r'// FILE: ([^\n]+\.swift)\n(.*?)(?=// FILE:|$)'
    file_matches = re.findall(file_pattern, result_text, re.MULTILINE | re.DOTALL)
    
    files_created = []
    
    for filename, content in file_matches:
        filename = filename.strip()
        content = content.strip()
        
        # Clean up content
        content = re.sub(r'^```swift\n?', '', content, flags=re.MULTILINE)
        content = re.sub(r'^```\n?', '', content, flags=re.MULTILINE)
        content = content.strip()
        
        if len(content) > 300:  # Must be substantial
            if "PostCreationViewModel" in filename:
                viewmodels_dir = Path(main_app_path) / "ViewModels"
                viewmodels_dir.mkdir(exist_ok=True)
                with open(viewmodels_dir / filename, 'w') as f:
                    f.write(content)
                files_created.append(filename)
                print(f"✅ Created {filename} ({len(content)} chars)")
                
            elif "PostCreationView" in filename:
                views_dir = Path(main_app_path) / "Views"
                views_dir.mkdir(exist_ok=True)
                with open(views_dir / filename, 'w') as f:
                    f.write(content)
                files_created.append(filename)
                print(f"✅ Created {filename} ({len(content)} chars)")
    
    return files_created

# =============================================================================
# ACCOUNTABILITY EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("🔥 AGENT ACCOUNTABILITY - NO MORE FAILURES!")
    print("=" * 60)
    print("❌ Previous agents FAILED to deliver actual Swift code")
    print("⚡ Time for real implementations, not imaginary reviews")
    print("=" * 60)
    
    crew = Crew(
        agents=[failed_agent_accountability, actual_swift_developer],
        tasks=[call_out_failure_task, write_actual_swift_code_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        result = crew.kickoff()
        
        # Create actual files
        files_created = create_actual_files(result)
        
        print("\n" + "=" * 60)
        print("🎯 ACCOUNTABILITY RESULTS:")
        if len(files_created) >= 2:
            print("🎉 SUCCESS! Actual Swift files created!")
            print("📋 Files Created:")
            for filename in files_created:
                print(f"   ✅ {filename}")
            print("📱 Ready to test post creation feature")
        else:
            print("❌ STILL FAILING - No proper Swift files created")
            print("🔥 Agents continue to disappoint")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n💥 ACCOUNTABILITY FAILED: {str(e)}")

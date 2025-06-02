#!/usr/bin/env python3
"""
Fix Timeline Navigation - View Timeline Button Does Nothing
The button exists but doesn't actually navigate to TimelineView
"""

import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process

main_app_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterClone"

# =============================================================================
# NAVIGATION FIX AGENTS
# =============================================================================

navigation_debugger = Agent(
    role='Navigation Debugger (Button Inspector)',
    goal='Find out why the View Timeline button does nothing and fix the navigation',
    backstory="""You debug broken navigation in iOS apps. You know that when a button 
    does nothing, it's usually because:
    1. The button action isn't connected properly
    2. The @State variable isn't set up
    3. The .sheet() or navigation isn't configured
    4. The button is calling the wrong function
    
    You study the working "Create Post" button to see how it works, then fix 
    the "View Timeline" button to work the same way.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

navigation_fixer = Agent(
    role='Navigation Fixer (Connection Expert)',
    goal='Fix the AuthenticatedView to properly navigate to TimelineView',
    backstory="""You fix broken navigation by connecting buttons to Views properly.
    You follow the exact same pattern as working navigation - if "Create Post" works,
    then "View Timeline" should work exactly the same way.
    
    You update the AuthenticatedView to include proper timeline navigation using
    the same @State and .sheet() pattern.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

# =============================================================================
# NAVIGATION FIX TASKS
# =============================================================================

debug_timeline_navigation_task = Task(
    description="""
    DEBUG WHY VIEW TIMELINE BUTTON DOES NOTHING
    
    **THE PROBLEM:**
    - "View Timeline" button exists on dashboard
    - Button does nothing when tapped
    - "Create Post" button works fine
    - Timeline navigation is broken
    
    **YOUR MISSION:**
    Study the current AuthenticatedView in LoginView.swift and identify the issue:
    
    1. **Compare Working vs Broken:**
       - How does "Create Post" button work?
       - What's different about "View Timeline" button?
       - What navigation patterns are missing?
    
    2. **Check Navigation Setup:**
       - Is there a @State var showTimeline variable?
       - Is the button action setting showTimeline = true?
       - Is there a .sheet(isPresented: $showTimeline) { TimelineView() }?
    
    3. **Identify Missing Pieces:**
       - What exact code is missing?
       - What needs to be added?
       - How should it match the "Create Post" pattern?
    
    **ANALYSIS REQUIRED:**
    - Exact comparison of working vs broken navigation
    - Specific missing code elements
    - Clear fix requirements
    
    Study the code and identify exactly what's broken with timeline navigation.
    """,
    expected_output="Analysis of why timeline navigation is broken and what needs to be fixed",
    agent=navigation_debugger
)

fix_timeline_navigation_task = Task(
    description="""
    FIX THE TIMELINE NAVIGATION IN AUTHENTICATEDVIEW
    
    **BASED ON DEBUG ANALYSIS:**
    Fix the AuthenticatedView to make "View Timeline" button work.
    
    **FOLLOW THE WORKING PATTERN:**
    Copy exactly how "Create Post" button works for timeline:
    
    1. **Add State Variable:**
       ```swift
       @State private var showTimeline = false
       ```
    
    2. **Fix Button Action:**
       ```swift
       Button(action: {
           showTimeline = true
       }) {
           // existing button content for View Timeline
       }
       ```
    
    3. **Add Sheet Navigation:**
       ```swift
       .sheet(isPresented: $showTimeline) {
           TimelineView()
       }
       ```
    
    **EXACT REQUIREMENTS:**
    - Add @State private var showTimeline = false
    - Update the "View Timeline" button action to set showTimeline = true
    - Add .sheet(isPresented: $showTimeline) { TimelineView() }
    - Follow the EXACT same pattern as "Create Post" button
    
    **OUTPUT FORMAT:**
    ```swift
    UPDATED_AUTHENTICATEDVIEW_START
    // Complete updated AuthenticatedView struct with working timeline navigation
    UPDATED_AUTHENTICATEDVIEW_END
    ```
    
    **FAILURE CONDITIONS:**
    - If you don't follow the exact same pattern as Create Post: FAILED
    - If you don't include all three required pieces: FAILED
    - If timeline navigation still doesn't work: FAILED
    
    Fix the navigation properly using the established working pattern.
    """,
    expected_output="Fixed AuthenticatedView with working timeline navigation",
    agent=navigation_fixer,
    depends_on=[debug_timeline_navigation_task]
)

# =============================================================================
# NAVIGATION FIX IMPLEMENTATION
# =============================================================================

def apply_navigation_fix(crew_result):
    """Apply the timeline navigation fix"""
    
    result_text = str(crew_result)
    
    # Save debug output
    debug_file = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai") / "timeline_navigation_fix.txt"
    with open(debug_file, 'w') as f:
        f.write(result_text)
    print(f"🔍 Navigation fix output saved to: timeline_navigation_fix.txt")
    
    # Extract the fixed AuthenticatedView
    import re
    
    fix_pattern = r'UPDATED_AUTHENTICATEDVIEW_START\n(.*?)\nUPDATED_AUTHENTICATEDVIEW_END'
    match = re.search(fix_pattern, result_text, re.DOTALL)
    
    if match:
        updated_code = match.group(1).strip()
        
        if len(updated_code) > 500 and "showTimeline" in updated_code:
            # Read current LoginView.swift
            login_file = Path(main_app_path) / "Views" / "LoginView.swift"
            
            if login_file.exists():
                with open(login_file, 'r') as f:
                    current_content = f.read()
                
                # Replace the AuthenticatedView struct
                pattern = r'struct AuthenticatedView: View \{.*?^\}'
                updated_content = re.sub(pattern, updated_code, current_content, flags=re.DOTALL | re.MULTILINE)
                
                with open(login_file, 'w') as f:
                    f.write(updated_content)
                
                print("✅ Fixed timeline navigation in AuthenticatedView")
                return True
            else:
                print("❌ LoginView.swift not found")
                return False
        else:
            print("❌ Invalid or incomplete navigation fix")
            return False
    else:
        print("❌ No navigation fix found in agent output")
        return False

# =============================================================================
# EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("🔧 TIMELINE NAVIGATION FIX - BROKEN BUTTON REPAIR")
    print("=" * 60)
    print("❌ PROBLEM: View Timeline button does nothing")
    print("✅ SOLUTION: Copy the working Create Post navigation pattern")
    print("=" * 60)
    
    crew = Crew(
        agents=[navigation_debugger, navigation_fixer],
        tasks=[debug_timeline_navigation_task, fix_timeline_navigation_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        result = crew.kickoff()
        
        # Apply the navigation fix
        success = apply_navigation_fix(result)
        
        print("\n" + "=" * 60)
        print("🎯 TIMELINE NAVIGATION FIX RESULTS:")
        if success:
            print("🎉 SUCCESS! Timeline navigation fixed!")
            print("📱 'View Timeline' button should now work")
            print("💡 Test by tapping 'View Timeline' on dashboard")
        else:
            print("❌ Navigation fix failed")
            print("📋 Check timeline_navigation_fix.txt for details")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n💥 NAVIGATION FIX FAILED: {str(e)}")

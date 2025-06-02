#!/usr/bin/env python3
"""
Timeline/Feed Discovery - Agent Research Phase
Agents investigate the codebase and backend to understand timeline requirements
"""

import os
from pathlib import Path
from crewai import Agent, Task, Crew, Process

# =============================================================================
# DISCOVERY AGENTS
# =============================================================================

ios_pattern_analyst = Agent(
    role='iOS Pattern Analyst',
    goal='Analyze existing iOS code patterns to understand how timeline/feed should be implemented',
    backstory="""You are an expert at analyzing iOS codebases to understand architectural patterns.
    You study existing Views and ViewModels to understand how list-based screens should be built.
    You identify reusable patterns, UI components, and data flow approaches that can be applied
    to new features like timeline/feed views.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

backend_api_researcher = Agent(
    role='Backend API Researcher',
    goal='Research backend endpoints and data structures for timeline/feed functionality',
    backstory="""You specialize in analyzing backend APIs to understand available endpoints,
    data structures, and integration requirements. You study existing API patterns to understand
    how timeline/feed data should be fetched, what authentication is needed, and what the
    response formats look like.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

technical_documentation_writer = Agent(
    role='Technical Documentation Writer',
    goal='Create comprehensive markdown documentation based on discovery findings',
    backstory="""You create clear, detailed technical documentation that serves as blueprints
    for development teams. You synthesize research findings into actionable specifications,
    requirements, and implementation strategies. Your documentation is the foundation that
    developers use to build features correctly.""",
    verbose=True,
    allow_delegation=False,
    tools=[]
)

# =============================================================================
# DISCOVERY TASKS
# =============================================================================

analyze_ios_patterns_task = Task(
    description="""
    ANALYZE iOS CODEBASE FOR TIMELINE/FEED PATTERNS
    
    **YOUR MISSION:**
    Study the existing iOS TwitterClone codebase to understand:
    
    1. **Existing Architecture Patterns:**
       - How do LoginView, RegistrationView, PostCreationView work?
       - What's the established MVVM pattern?
       - How are Views connected to ViewModels?
       - What navigation patterns are used?
    
    2. **Data Display Patterns:**
       - How are forms currently handled?
       - What UI components are available for lists/feeds?
       - How is data binding implemented?
       - What loading and error state patterns exist?
    
    3. **Network Integration:**
       - How do existing ViewModels call APIs?
       - What's the pattern for handling async data loading?
       - How are responses processed and displayed?
       - How is authentication handled in API calls?
    
    4. **Timeline/Feed Requirements:**
       - What would a timeline View need to display?
       - How should it integrate with existing navigation?
       - What ViewModel patterns should it follow?
       - How should posts be displayed in a list format?
    
    **ANALYZE AND DOCUMENT:**
    - Current MVVM patterns that timeline should follow
    - UI components that could be reused for timeline
    - Navigation integration points
    - Data flow patterns for list-based content
    
    Focus on understanding HOW timeline should fit into existing patterns.
    """,
    expected_output="Analysis of iOS patterns and how timeline should integrate",
    agent=ios_pattern_analyst
)

research_backend_api_task = Task(
    description="""
    RESEARCH BACKEND API FOR TIMELINE/FEED FUNCTIONALITY
    
    **YOUR MISSION:**
    Investigate the backend to understand timeline/feed capabilities:
    
    1. **Existing API Endpoints:**
       - What endpoints are available in the post-service?
       - Are there timeline or feed endpoints already?
       - What endpoints return lists of posts?
       - How are posts queried and filtered?
    
    2. **Data Structures:**
       - What does a Post object look like in responses?
       - What fields are available (id, content, user, likes, etc.)?
       - How are posts ordered (by date, popularity, etc.)?
       - What metadata is included with posts?
    
    3. **Authentication Requirements:**
       - Do timeline endpoints require authentication?
       - How should JWT tokens be passed?
       - What happens with unauthenticated requests?
    
    4. **API Patterns:**
       - How do existing endpoints handle pagination?
       - What's the request/response format?
       - How are errors returned?
       - What status codes are used?
    
    5. **Timeline Strategy:**
       - Should timeline show all posts (public feed)?
       - Should it show user-specific posts?
       - How should posts be ordered?
       - What's the simplest timeline implementation?
    
    **RESEARCH AND DOCUMENT:**
    - Available endpoints for fetching posts
    - Post data structure and fields
    - Authentication requirements
    - Recommended timeline implementation approach
    
    Focus on what's AVAILABLE now, not what needs to be built.
    """,
    expected_output="Research findings on backend API capabilities for timeline",
    agent=backend_api_researcher,
    depends_on=[analyze_ios_patterns_task]
)

create_timeline_specification_task = Task(
    description="""
    CREATE COMPREHENSIVE TIMELINE SPECIFICATION DOCUMENT
    
    **YOUR MISSION:**
    Based on the iOS analysis and backend research, create a detailed markdown specification.
    
    **DOCUMENT STRUCTURE:**
    
    ```markdown
    # Timeline/Feed Feature Specification
    
    ## Executive Summary
    - What is the timeline feature?
    - How does it fit into the existing app?
    - What's the user experience?
    
    ## iOS Implementation Strategy
    
    ### Architecture Patterns
    - MVVM pattern to follow (based on existing code)
    - How TimelineView should be structured
    - How TimelineViewModel should work
    - Integration with existing navigation
    
    ### UI Components
    - List/feed display approach
    - Post cell/row design
    - Loading states and error handling
    - Refresh and pagination (if applicable)
    
    ### Data Flow
    - How timeline data is fetched
    - How posts are displayed
    - How user interactions are handled
    - Integration with existing authentication
    
    ## Backend Integration
    
    ### API Endpoints
    - Which endpoints to use for timeline
    - Request format and parameters
    - Response format and data structure
    - Authentication requirements
    
    ### Data Models
    - Post structure and fields
    - Timeline response format
    - Error handling approach
    
    ## Implementation Plan
    
    ### Phase 1: Core Timeline
    - Minimum viable timeline implementation
    - Essential features only
    - Following established patterns
    
    ### Technical Requirements
    - TimelineView implementation details
    - TimelineViewModel specification
    - Integration points with existing code
    - Testing approach
    
    ## Success Criteria
    - What constitutes a working timeline?
    - How to verify it follows existing patterns?
    - Integration checkpoints
    ```
    
    **REQUIREMENTS:**
    - Be specific and actionable
    - Reference actual code patterns found
    - Include real API endpoint details
    - Provide clear implementation guidance
    - Keep it simple - timeline = list of posts
    - Focus on following existing patterns, not inventing new ones
    
    **OUTPUT FORMAT:**
    A complete markdown document that serves as the blueprint for implementation.
    """,
    expected_output="Complete timeline specification document in markdown format",
    agent=technical_documentation_writer,
    depends_on=[research_backend_api_task]
)

# =============================================================================
# EXECUTION AND DOCUMENTATION
# =============================================================================

def save_timeline_specification(crew_result):
    """Save the timeline specification document"""
    
    result_text = str(crew_result)
    
    # Save full output for debugging
    debug_file = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai") / "timeline_discovery_full_output.txt"
    with open(debug_file, 'w') as f:
        f.write(result_text)
    
    # Extract and save the markdown specification
    import re
    
    # Look for markdown content
    markdown_patterns = [
        r'```markdown\n(.*?)\n```',
        r'# Timeline/Feed Feature Specification\n(.*?)(?=\n\n---|\n\nAgent|$)',
        r'(# Timeline.*?)(?=\n\nAgent|\n\n##|\n\n---|\nAgent|$)'
    ]
    
    specification_content = None
    
    for pattern in markdown_patterns:
        matches = re.findall(pattern, result_text, re.DOTALL | re.IGNORECASE)
        for match in matches:
            if len(match) > 500:  # Substantial content
                if isinstance(match, tuple):
                    specification_content = match[0]
                else:
                    specification_content = match
                break
        if specification_content:
            break
    
    # If we found good specification content, save it
    if specification_content:
        # Clean up the content
        specification_content = specification_content.strip()
        
        # Ensure it starts with the main title
        if not specification_content.startswith('# Timeline'):
            specification_content = "# Timeline/Feed Feature Specification\n\n" + specification_content
        
        # Save the specification document
        spec_file = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai") / "TIMELINE_SPECIFICATION.md"
        with open(spec_file, 'w') as f:
            f.write(specification_content)
        
        print("📋 Timeline specification saved to: TIMELINE_SPECIFICATION.md")
        return True
    else:
        print("⚠️  No substantial markdown specification found in output")
        return False

# =============================================================================
# DISCOVERY EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("🔍 TIMELINE/FEED DISCOVERY - RESEARCH PHASE")
    print("=" * 60)
    print("🎯 Mission: Research and document timeline requirements")
    print("📋 Output: Comprehensive markdown specification")
    print("=" * 60)
    
    crew = Crew(
        agents=[ios_pattern_analyst, backend_api_researcher, technical_documentation_writer],
        tasks=[analyze_ios_patterns_task, research_backend_api_task, create_timeline_specification_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        result = crew.kickoff()
        
        # Save the specification document
        success = save_timeline_specification(result)
        
        print("\n" + "=" * 60)
        print("🎯 TIMELINE DISCOVERY RESULTS:")
        if success:
            print("✅ SUCCESS! Timeline specification document created!")
            print("📋 Review: TIMELINE_SPECIFICATION.md")
            print("💡 This document will guide the implementation phase")
        else:
            print("⚠️  Specification extraction failed")
            print("📋 Check: timeline_discovery_full_output.txt for raw output")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n💥 DISCOVERY FAILED: {str(e)}")

"""
001 - Planning Stage 1: Requirements Analysis and Technical Planning (Fixed)
Twitter Clone CrewAI Project - Phase 1

This script runs the initial planning phase with proper task separation and output capture.
"""

from improved_twitter_config import technical_lead, business_analyst
from crewai import Task, Crew, Process

def run_planning_stage_1():
    """Execute the first planning stage with proper task separation"""
    
    print("🚀 Starting Planning Stage 1...")
    print("=" * 80)
    print("📋 PHASE 1: Requirements Analysis & Technical Planning + Sprint Retro")
    print("=" * 80)
    print("This will take 5-7 minutes to complete.")
    print("")

    # Business Analysis Task
    requirements_task = Task(
        description='''
        Create a comprehensive requirements analysis for a multi-platform Twitter clone MVP.
        
        TARGET PLATFORMS:
        - Native iOS app (iPhone/iPad)
        - Native Android app 
        - React.js web application
        - Backend API (to serve all client platforms)
        
        Include:
        1. Core features for MVP (prioritized list) across all platforms (mobile + web)
        2. User personas and user journey mapping for mobile and web users
        3. Detailed user stories with acceptance criteria for mobile and web experiences
        4. Platform-specific considerations (iOS vs Android vs Web features)
        5. Non-functional requirements (performance, security, scalability) for mobile + web + backend
        6. Success metrics and KPIs for mobile app adoption and web engagement
        7. Scope definition (what's IN and what's OUT for MVP) for each platform
        8. API requirements to support mobile and web functionality
        9. Cross-platform feature parity and differences
        
        Focus on creating a realistic multi-platform MVP (mobile-first with web support) that can be built by a small team with backend, mobile, and web expertise.
        Consider offline capabilities, push notifications for mobile, and responsive web design.
        
        Provide a detailed, structured document with clear sections for each requirement area.
        ''',
        agent=business_analyst,
        expected_output='Complete multi-platform requirements document with user stories, acceptance criteria, and MVP scope definition for iOS, Android, React.js web app, and backend API'
    )

    # Technical Planning Task
    technical_planning_task = Task(
        description='''
        Based on the requirements analysis provided by the Business Analyst, create a detailed technical project plan for a comprehensive multi-platform Twitter clone.
        
        REQUIRED TECHNOLOGY STACK:
        - Backend: Kotlin with Spring Boot (team expertise in JVM/Kotlin)
        - Containerization: Docker for backend API deployment and development consistency
        - Mobile: Native iOS (Swift/SwiftUI) and Android (Kotlin/Jetpack Compose) apps
        - Web Frontend: React.js for dynamic, responsive web interface
        - Database: PostgreSQL for main data, Redis for caching
        - Real-time: WebSockets for live features across all platforms
        - Deployment: Docker containers with orchestration (Kubernetes/Docker Compose)
        
        Create a comprehensive technical plan that includes:
        1. Technology stack implementation plan (Dockerized Kotlin Spring Boot backend, iOS Swift, Android Kotlin, React.js web)
        2. Multi-platform architecture (unified backend API in Docker containers serving mobile and web clients)
        3. Docker containerization strategy for backend services and local development
        4. Development phases and timeline for backend + mobile + web development
        5. Team coordination strategy for backend, mobile, and web teams
        6. Risk assessment and mitigation strategies across all platforms
        7. CI/CD and deployment strategy for containerized backend, mobile apps, and web application
        8. Testing and quality assurance approach across all platforms
        9. API design strategy for mobile and web client communication
        10. Infrastructure and DevOps considerations for containerized deployment
        11. Shared component strategy and platform-specific optimizations
        
        Focus on leveraging the team's JVM/Kotlin expertise while building native mobile experiences and a modern web application.
        Emphasize Docker containerization for consistent deployment and development environments.
        Provide realistic estimates and identify potential bottlenecks for multi-platform development.
        
        Create a detailed, structured technical document with clear sections and actionable recommendations.
        ''',
        agent=technical_lead,
        expected_output='Comprehensive multi-platform technical project plan with containerized Kotlin Spring Boot backend, native iOS/Android apps, React.js web app, Docker deployment strategy, architecture, timeline, and risk assessment'
    )

    # Execute requirements and technical planning first
    print("=" * 60)
    print("📋 STEP 1: Requirements Analysis")
    print("=" * 60)
    
    requirements_crew = Crew(
        agents=[business_analyst],
        tasks=[requirements_task],
        process=Process.sequential,
        verbose=True
    )
    
    requirements_result = requirements_crew.kickoff()
    
    print("\n" + "=" * 60)
    print("🔧 STEP 2: Technical Planning")
    print("=" * 60)
    
    technical_crew = Crew(
        agents=[technical_lead],
        tasks=[technical_planning_task],
        process=Process.sequential,
        verbose=True
    )
    
    technical_result = technical_crew.kickoff()
    
    # Now do the retrospective with context
    print("\n" + "=" * 60)
    print("📊 STEP 3: Sprint Retrospective")
    print("=" * 60)
    
    sprint_retro_task = Task(
        description=f'''
        Conduct a sprint retrospective analysis of the planning phase that was just completed.
        
        You have access to the following deliverables that were just created:
        
        REQUIREMENTS ANALYSIS DELIVERABLE:
        {str(requirements_result)[:1000]}...
        
        TECHNICAL PLANNING DELIVERABLE:
        {str(technical_result)[:1000]}...
        
        RETROSPECTIVE FRAMEWORK:
        Use the "What went well / What didn't go well / What can we improve" format.
        
        Analyze the actual deliverables created and include:
        1. **What Went Well:**
           - Successful aspects of the requirements gathering
           - Effective technical planning elements
           - Good collaboration between business and technical perspectives
           - Clear deliverables and outcomes
           - Technology stack alignment with team expertise
        
        2. **What Didn't Go Well:**
           - Areas where requirements might be unclear or incomplete
           - Technical planning gaps or potential issues
           - Communication or coordination challenges
           - Missing considerations or blind spots
           - Potential scope or timeline concerns
        
        3. **What Can We Improve:**
           - Specific recommendations for next planning phases
           - Process improvements for future sprints
           - Areas needing more detail or refinement
           - Risk mitigation strategies
           - Better cross-platform coordination approaches
        
        4. **Action Items:**
           - Concrete next steps to address identified issues
           - Recommendations for upcoming development phases
           - Process improvements for the team
           - Documentation or planning gaps to fill
        
        Be honest and constructive in the analysis. Focus on continuous improvement and team learning.
        Reference specific aspects of the requirements and technical planning deliverables.
        ''',
        agent=technical_lead,
        expected_output='Comprehensive sprint retrospective report with what went well, what didn\'t go well, improvement recommendations, and concrete action items for the planning phase'
    )
    
    retro_crew = Crew(
        agents=[technical_lead],
        tasks=[sprint_retro_task],
        process=Process.sequential,
        verbose=True
    )
    
    retro_result = retro_crew.kickoff()
    
    # Combine and save all results
    print("\n" + "=" * 80)
    print("📋 PLANNING STAGE 1 COMPLETE")
    print("=" * 80)
    
    # Save comprehensive project plan
    with open('TwitterClone_ProjectPlan_Phase1.md', 'w') as f:
        f.write('# Twitter Clone Project Plan - Phase 1\n\n')
        f.write('## Requirements Analysis\n\n')
        f.write(str(requirements_result))
        f.write('\n\n## Technical Planning\n\n')
        f.write(str(technical_result))
        f.write('\n\n## Sprint Retrospective\n\n')
        f.write(str(retro_result))
        
    # Save individual sections
    with open('TwitterClone_Requirements_Phase1.md', 'w') as f:
        f.write('# Requirements Analysis - Phase 1\n\n')
        f.write(str(requirements_result))
        
    with open('TwitterClone_TechnicalPlan_Phase1.md', 'w') as f:
        f.write('# Technical Plan - Phase 1\n\n')
        f.write(str(technical_result))
        
    with open('TwitterClone_SprintRetro_Phase1.md', 'w') as f:
        f.write('# Sprint Retrospective - Phase 1\n\n')
        f.write(str(retro_result))
        
    print("\n✅ Files created:")
    print("  • TwitterClone_ProjectPlan_Phase1.md (Complete plan)")
    print("  • TwitterClone_Requirements_Phase1.md (Requirements only)")
    print("  • TwitterClone_TechnicalPlan_Phase1.md (Technical plan only)")
    print("  • TwitterClone_SprintRetro_Phase1.md (Retrospective only)")
    print("")
    print("🎯 Next Steps:")
    print("  • Review all generated documents")
    print("  • Address any issues identified in the retrospective")
    print("  • Run 002_planning_stage_2.py for detailed architecture")
    print("  • Or proceed to specific development phases:")
    print("    - Backend (Containerized Kotlin Spring Boot)")
    print("    - iOS (Swift/SwiftUI)")
    print("    - Android (Kotlin/Jetpack Compose)")
    print("    - Web Frontend (React.js)")
    
    return {
        'requirements': requirements_result,
        'technical': technical_result,
        'retrospective': retro_result
    }

if __name__ == "__main__":
    run_planning_stage_1()

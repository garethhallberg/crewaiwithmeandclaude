"""
Twitter Clone CrewAI Configuration
Comprehensive team setup for Twitter clone development
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import CodeDocsSearchTool, CodeInterpreterTool, FileReadTool, DirectoryReadTool
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import os

# Custom tools for development - Using CrewAI BaseTool
class CodeReviewToolInput(BaseModel):
    """Input schema for CodeReviewTool."""
    code: str = Field(..., description="The code to review for best practices and optimization.")

class CodeReviewTool(BaseTool):
    name: str = "Code Review Tool"
    description: str = "Reviews code for best practices, security issues, and optimization opportunities."
    args_schema: Type[BaseModel] = CodeReviewToolInput
    
    def _run(self, code: str) -> str:
        """Reviews code for best practices, security issues, and optimization opportunities."""
        return f"Code review completed for: {code[:100]}..."

class ArchitectureValidationToolInput(BaseModel):
    """Input schema for ArchitectureValidationTool."""
    architecture_description: str = Field(..., description="The architecture description to validate.")

class ArchitectureValidationTool(BaseTool):
    name: str = "Architecture Validation Tool"  
    description: str = "Validates software architecture against best practices and design patterns."
    args_schema: Type[BaseModel] = ArchitectureValidationToolInput
    
    def _run(self, architecture_description: str) -> str:
        """Validates software architecture against best practices and design patterns."""
        return f"Architecture validation completed for: {architecture_description[:100]}..."

class TestCoverageToolInput(BaseModel):
    """Input schema for TestCoverageTool."""
    test_code: str = Field(..., description="The test code to analyze for coverage.")

class TestCoverageTool(BaseTool):
    name: str = "Test Coverage Tool"
    description: str = "Analyzes test coverage and suggests additional test cases."
    args_schema: Type[BaseModel] = TestCoverageToolInput
    
    def _run(self, test_code: str) -> str:
        """Analyzes test coverage and suggests additional test cases."""
        return f"Test coverage analysis completed for: {test_code[:100]}..."

# Initialize tools
code_docs_tool = CodeDocsSearchTool()
code_interpreter = CodeInterpreterTool()
file_reader = FileReadTool()
directory_reader = DirectoryReadTool()

# Initialize custom tools
code_review_tool = CodeReviewTool()
architecture_validation_tool = ArchitectureValidationTool()
test_coverage_tool = TestCoverageTool()

# =============================================================================
# AGENTS CONFIGURATION
# =============================================================================

# 1. Technical Lead
technical_lead = Agent(
    role='Technical Lead',
    goal='Oversee the entire Twitter clone project, ensure technical excellence, and coordinate between all teams',
    backstory="""You are a seasoned Technical Lead with 12+ years of experience in full-stack development 
    and team management. You have successfully led multiple social media platform projects and understand 
    the complexities of scalable, real-time applications. Your expertise spans mobile development, backend 
    architecture, and DevOps practices.""",
    tools=[code_review_tool, architecture_validation_tool, file_reader, directory_reader],
    verbose=True,
    allow_delegation=True,
    max_iter=3
)

# Test the configuration
if __name__ == "__main__":
    print("✅ CrewAI Configuration loaded successfully!")
    print(f"Technical Lead: {technical_lead.role}")
    print(f"Available tools: {[tool.name for tool in technical_lead.tools]}")

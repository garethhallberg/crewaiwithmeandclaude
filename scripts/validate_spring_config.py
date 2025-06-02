#!/usr/bin/env python3
"""
CrewAI Script: Spring Boot Configuration Validator
This script validates Spring Boot configuration files to prevent common issues.
"""

import os
import yaml
import sys
from pathlib import Path

class SpringBootConfigValidator:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.issues = []
    
    def validate_project(self):
        """Validate all Spring Boot configuration files in the project"""
        print("🔍 Validating Spring Boot configuration files...")
        
        # Find all application*.yml and application*.yaml files
        config_files = []
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if file.startswith('application') and (file.endswith('.yml') or file.endswith('.yaml')):
                    config_files.append(Path(root) / file)
        
        print(f"Found {len(config_files)} configuration files")
        
        for config_file in config_files:
            self.validate_config_file(config_file)
        
        return self.issues
    
    def validate_config_file(self, config_file: Path):
        """Validate a specific configuration file"""
        try:
            with open(config_file, 'r') as f:
                content = yaml.safe_load(f)
            
            # Check if this is a profile-specific file
            filename = config_file.name
            is_profile_specific = '-' in filename and filename != 'application.yml' and filename != 'application.yaml'
            
            if is_profile_specific and content and 'spring' in content:
                spring_config = content['spring']
                
                # Check for spring.profiles.active in profile-specific files
                if 'profiles' in spring_config and 'active' in spring_config['profiles']:
                    profile_name = filename.split('-')[1].split('.')[0]
                    issue = {
                        'file': str(config_file),
                        'type': 'INVALID_PROFILE_ACTIVATION',
                        'message': f"Profile-specific file ({profile_name}) should not contain 'spring.profiles.active'",
                        'fix': "Remove 'spring.profiles.active' property and use @ActiveProfiles annotation in tests"
                    }
                    self.issues.append(issue)
                    print(f"❌ {config_file.relative_to(self.project_root)}: Invalid profile activation")
                else:
                    print(f"✅ {config_file.relative_to(self.project_root)}: Valid configuration")
            else:
                print(f"✅ {config_file.relative_to(self.project_root)}: Valid configuration")
                
        except Exception as e:
            issue = {
                'file': str(config_file),
                'type': 'PARSE_ERROR',
                'message': f"Failed to parse YAML: {str(e)}",
                'fix': "Check YAML syntax"
            }
            self.issues.append(issue)
            print(f"❌ {config_file.relative_to(self.project_root)}: Parse error - {str(e)}")
    
    def fix_issues(self):
        """Automatically fix common configuration issues"""
        print("\n🔧 Fixing configuration issues...")
        
        for issue in self.issues:
            if issue['type'] == 'INVALID_PROFILE_ACTIVATION':
                self.fix_profile_activation(issue['file'])
    
    def fix_profile_activation(self, config_file: str):
        """Fix invalid profile activation in config files"""
        try:
            with open(config_file, 'r') as f:
                lines = f.readlines()
            
            # Remove spring.profiles.active lines
            new_lines = []
            skip_next = False
            
            for i, line in enumerate(lines):
                if skip_next:
                    skip_next = False
                    continue
                    
                if 'profiles:' in line and i + 1 < len(lines) and 'active:' in lines[i + 1]:
                    # Skip both 'profiles:' and 'active:' lines
                    skip_next = True
                    continue
                elif 'active:' in line and i > 0 and 'profiles:' in lines[i - 1]:
                    # Skip if previous line was 'profiles:'
                    continue
                else:
                    new_lines.append(line)
            
            # Remove empty spring: blocks
            final_lines = []
            for i, line in enumerate(new_lines):
                if line.strip() == 'spring:':
                    # Check if the next non-empty line is at the same or lower indentation level
                    next_meaningful_line_idx = None
                    for j in range(i + 1, len(new_lines)):
                        if new_lines[j].strip():
                            next_meaningful_line_idx = j
                            break
                    
                    if (next_meaningful_line_idx is None or 
                        len(new_lines[next_meaningful_line_idx]) - len(new_lines[next_meaningful_line_idx].lstrip()) <= 
                        len(line) - len(line.lstrip())):
                        # Skip empty spring: block
                        continue
                
                final_lines.append(line)
            
            with open(config_file, 'w') as f:
                f.writelines(final_lines)
            
            print(f"✅ Fixed: {config_file}")
            
        except Exception as e:
            print(f"❌ Failed to fix {config_file}: {str(e)}")
    
    def generate_report(self):
        """Generate a summary report"""
        print(f"\n📊 Validation Summary:")
        print(f"Total issues found: {len(self.issues)}")
        
        if self.issues:
            print("\n🚨 Issues Details:")
            for issue in self.issues:
                print(f"  File: {issue['file']}")
                print(f"  Type: {issue['type']}")  
                print(f"  Message: {issue['message']}")
                print(f"  Fix: {issue['fix']}")
                print()

def main():
    if len(sys.argv) < 2:
        project_root = "/Users/garethhallberg/Desktop/twitter-clone-crewai"
    else:
        project_root = sys.argv[1]
    
    validator = SpringBootConfigValidator(project_root)
    issues = validator.validate_project()
    
    if issues:
        validator.fix_issues()
        print("\n✅ Configuration issues have been fixed!")
        print("You should now run './gradlew clean' to clear build caches.")
    else:
        print("\n✅ All configuration files are valid!")
    
    validator.generate_report()

if __name__ == "__main__":
    main()

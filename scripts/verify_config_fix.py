#!/usr/bin/env python3
"""
Simple verification script to check if Spring Boot configuration is fixed.
"""

import yaml
from pathlib import Path

def check_config_file(file_path):
    """Check if a config file has the invalid spring.profiles.active setting"""
    try:
        with open(file_path, 'r') as f:
            content = yaml.safe_load(f)
        
        if content and 'spring' in content:
            spring_config = content['spring']
            if 'profiles' in spring_config and 'active' in spring_config['profiles']:
                return False, "Contains spring.profiles.active"
        
        return True, "Configuration is valid"
    
    except Exception as e:
        return False, f"Error reading file: {str(e)}"

def main():
    project_root = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai")
    
    # Check the two main test configuration files
    test_configs = [
        project_root / "generated_code/backend/user-service/src/test/resources/application-test.yml",
        project_root / "generated_code/backend/post-service/src/test/resources/application-test.yml"
    ]
    
    print("🔍 Checking Spring Boot test configuration files...")
    print()
    
    all_valid = True
    
    for config_file in test_configs:
        if config_file.exists():
            is_valid, message = check_config_file(config_file)
            
            status = "✅" if is_valid else "❌"
            print(f"{status} {config_file.relative_to(project_root)}")
            print(f"   {message}")
            
            if not is_valid:
                all_valid = False
        else:
            print(f"❓ {config_file.relative_to(project_root)} - File not found")
    
    print()
    if all_valid:
        print("✅ All configuration files are valid!")
        print("You can now run the integration tests with:")
        print("cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend")
        print("./gradlew clean")
        print("./gradlew :user-service:test --tests '*IntegrationTest*'")
    else:
        print("❌ Some configuration files still have issues.")
        print("Please review the files marked with ❌ above.")

if __name__ == "__main__":
    main()

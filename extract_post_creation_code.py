#!/usr/bin/env python3
"""
Extract Post Creation Code - Fix the Regex Issues
The review passed but files weren't extracted properly
"""

import os
import re
from pathlib import Path

main_app_path = "/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/ios/TwitterClone/TwitterClone"

def extract_and_create_files():
    """Read the review file and extract the actual code"""
    
    review_file = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai/post_creation_with_review.txt")
    
    if not review_file.exists():
        print("❌ Review file not found")
        return []
    
    with open(review_file, 'r') as f:
        content = f.read()
    
    print("🔍 Searching for Swift code in the review output...")
    
    # Look for any Swift code blocks with various formats
    swift_patterns = [
        r'```swift\n(.*?)\n```',
        r'```\n(.*?class PostCreationViewModel.*?)\n```',
        r'```\n(.*?struct PostCreationView.*?)\n```',
        r'(import Foundation.*?class PostCreationViewModel.*?)(?=\n\n|\n```|\nstruct|\nThe)',
        r'(import SwiftUI.*?struct PostCreationView.*?)(?=\n\n|\n```|\nstruct|\nThe)',
    ]
    
    files_created = []
    
    for pattern in swift_patterns:
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            code = match.strip()
            
            # Check if it's PostCreationViewModel
            if 'class PostCreationViewModel' in code and len(code) > 500:
                viewmodels_dir = Path(main_app_path) / "ViewModels"
                viewmodels_dir.mkdir(exist_ok=True)
                
                with open(viewmodels_dir / "PostCreationViewModel.swift", 'w') as f:
                    f.write(code)
                
                files_created.append("PostCreationViewModel.swift")
                print(f"✅ Created PostCreationViewModel.swift ({len(code)} chars)")
                
            # Check if it's PostCreationView
            elif 'struct PostCreationView' in code and len(code) > 400:
                views_dir = Path(main_app_path) / "Views"
                views_dir.mkdir(exist_ok=True)
                
                with open(views_dir / "PostCreationView.swift", 'w') as f:
                    f.write(code)
                
                files_created.append("PostCreationView.swift")
                print(f"✅ Created PostCreationView.swift ({len(code)} chars)")
    
    return files_created

if __name__ == "__main__":
    print("🔧 EXTRACTING APPROVED POST CREATION CODE")
    print("=" * 50)
    
    files_created = extract_and_create_files()
    
    if len(files_created) >= 2:
        print("\n🎉 SUCCESS! Post Creation files extracted and created!")
        print("📋 Files Created:")
        for filename in files_created:
            print(f"   ✅ {filename}")
        print("\n📱 Ready to test post creation feature!")
    elif len(files_created) > 0:
        print(f"\n⚠️  Partial success - created {len(files_created)} files")
        print("📋 Files Created:")
        for filename in files_created:
            print(f"   ✅ {filename}")
    else:
        print("\n❌ No Swift code found in review output")
        print("💡 The agents may not have included the actual code")
        print("🔍 Check post_creation_with_review.txt manually")
    
    print("=" * 50)

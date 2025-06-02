#!/usr/bin/env python3
"""
Simple script to verify Spring Boot configuration is fixed and run integration tests
"""

import subprocess
import sys
from pathlib import Path

def run_command(command, cwd, description):
    """Run a command and return the result"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        return result
    except subprocess.TimeoutExpired:
        print(f"❌ {description} timed out")
        return None
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return None

def main():
    print("🚀 Spring Boot Integration Test Verification")
    print("=" * 50)
    
    backend_dir = Path("/Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend")
    
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        sys.exit(1)
    
    if not (backend_dir / "gradlew").exists():
        print("❌ Gradle wrapper not found!")
        sys.exit(1)
    
    # Step 1: Clean build
    clean_result = run_command(
        ["./gradlew", "clean"],
        backend_dir,
        "Cleaning build directories"
    )
    
    if clean_result is None or clean_result.returncode != 0:
        print("❌ Build clean failed")
        if clean_result:
            print("Error output:", clean_result.stderr[-500:])
        sys.exit(1)
    else:
        print("✅ Build clean successful")
    
    # Step 2: Compile to check for basic issues
    compile_result = run_command(
        ["./gradlew", ":user-service:compileKotlin"],
        backend_dir,
        "Compiling user-service"
    )
    
    if compile_result is None or compile_result.returncode != 0:
        print("❌ Compilation failed")
        if compile_result:
            print("Error output:", compile_result.stderr[-500:])
        sys.exit(1)
    else:
        print("✅ Compilation successful")
    
    # Step 3: Run integration tests
    test_result = run_command(
        ["./gradlew", ":user-service:test", "--tests", "*IntegrationTest*", "--info"],
        backend_dir,
        "Running user-service integration tests"
    )
    
    if test_result is None:
        print("❌ Test execution failed (timeout or error)")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    
    if test_result.returncode == 0:
        print("🎉 SUCCESS! Integration tests PASSED")
        print("✅ Spring Boot configuration fix was successful")
        print("✅ Application context loads correctly")
        print("✅ All test cases executed successfully")
        
        # Check for test summary in output
        if "tests completed" in test_result.stdout:
            print("\n📈 Test Summary:")
            lines = test_result.stdout.split('\n')
            for line in lines:
                if "tests completed" in line or "test" in line.lower() and ("passed" in line.lower() or "failed" in line.lower()):
                    print(f"   {line.strip()}")
        
    else:
        print("❌ FAILED! Integration tests did not pass")
        print("❌ Exit code:", test_result.returncode)
        
        # Show relevant error information
        if test_result.stderr:
            print("\n🔍 Error Details:")
            print(test_result.stderr[-1000:])  # Last 1000 chars of stderr
        
        if test_result.stdout:
            print("\n🔍 Test Output (last part):")
            print(test_result.stdout[-1000:])  # Last 1000 chars of stdout
        
        print("\n🔧 Troubleshooting suggestions:")
        print("1. Check if all required services are running")
        print("2. Verify database configurations")
        print("3. Ensure no port conflicts")
        print("4. Check application logs for detailed errors")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()

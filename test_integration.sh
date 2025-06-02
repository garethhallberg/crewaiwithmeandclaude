#!/bin/bash

# Quick Test Runner for Twitter Clone Integration Tests
# This script runs only the integration tests after fixing configuration issues

echo "🧪 Running Twitter Clone Integration Tests..."
echo "============================================="

# Navigate to backend directory
cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

# Check if we're in the right place
if [ ! -f "gradlew" ]; then
    echo "❌ Error: gradlew not found. Are you in the right directory?"
    exit 1
fi

# Clean build first to ensure fresh start
echo "🧹 Cleaning build directories..."
./gradlew clean

# Test user-service integration tests
echo ""
echo "🔬 Testing user-service integration tests..."
echo "--------------------------------------------"
if ./gradlew :user-service:test --tests '*IntegrationTest*' --info; then
    echo "✅ User service integration tests PASSED"
    USER_SERVICE_STATUS="PASSED"
else
    echo "❌ User service integration tests FAILED"
    USER_SERVICE_STATUS="FAILED"
fi

# Test post-service integration tests  
echo ""
echo "🔬 Testing post-service integration tests..."
echo "--------------------------------------------"
if ./gradlew :post-service:test --tests '*IntegrationTest*' --info; then
    echo "✅ Post service integration tests PASSED"
    POST_SERVICE_STATUS="PASSED"
else
    echo "❌ Post service integration tests FAILED"
    POST_SERVICE_STATUS="FAILED"
fi

# Summary
echo ""
echo "============================================="
echo "📊 Integration Test Summary"
echo "============================================="
echo "User Service: $USER_SERVICE_STATUS"
echo "Post Service: $POST_SERVICE_STATUS"

if [ "$USER_SERVICE_STATUS" = "PASSED" ] && [ "$POST_SERVICE_STATUS" = "PASSED" ]; then
    echo ""
    echo "🎉 ALL INTEGRATION TESTS PASSED!"
    echo "Your Spring Boot configuration fix was successful."
    exit 0
else
    echo ""
    echo "⚠️  Some integration tests failed."
    echo "Check the test output above for details."
    echo ""
    echo "Common troubleshooting steps:"
    echo "1. Ensure Docker is running (for TestContainers)"
    echo "2. Check if ports are available"
    echo "3. Verify database configurations"
    echo "4. Review application logs for errors"
    exit 1
fi

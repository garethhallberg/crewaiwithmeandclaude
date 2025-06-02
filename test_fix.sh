#!/bin/bash

echo "🧪 Testing Integration Tests After Configuration Fix"
echo "===================================================="

cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

# Clean build directories first
echo "🧹 Cleaning build directories..."
./gradlew clean

if [ $? -eq 0 ]; then
    echo "✅ Build cleanup successful"
else
    echo "❌ Build cleanup failed"
    exit 1
fi

echo ""
echo "🔬 Running User Service Integration Tests..."
echo "--------------------------------------------"

./gradlew :user-service:test --tests '*IntegrationTest*' --info

USER_TEST_RESULT=$?

echo ""
echo "📊 Test Results Summary"
echo "======================"

if [ $USER_TEST_RESULT -eq 0 ]; then
    echo "✅ User Service Integration Tests: PASSED"
    echo ""
    echo "🎉 SUCCESS! The Spring Boot configuration fix worked!"
    echo "Your integration tests are now running properly."
else
    echo "❌ User Service Integration Tests: FAILED"
    echo ""
    echo "The tests are still failing. Let's check for other issues..."
fi

echo ""
echo "Next steps:"
echo "1. If tests passed: Great! Your configuration is fixed."
echo "2. If tests failed: Check the error output above for specific issues."
echo "3. Common issues might be: Docker not running, port conflicts, or database setup."

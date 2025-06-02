#!/bin/bash

echo "🎯 Testing Final 401 Fix"
echo "========================"

cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

echo "🧹 Cleaning build..."
./gradlew clean

echo "🔬 Running integration tests..."
./gradlew :user-service:test --tests '*IntegrationTest*' --info

TEST_RESULT=$?

echo ""
echo "========================"
echo "🏆 FINAL TEST RESULTS"
echo "========================"

if [ $TEST_RESULT -eq 0 ]; then
    echo "🎉 SUCCESS! ALL INTEGRATION TESTS ARE NOW PASSING!"
    echo ""
    echo "✅ Spring Boot configuration issue: FIXED"
    echo "✅ Entity-Repository mismatch: FIXED"  
    echo "✅ Authentication entry point: FIXED"
    echo "✅ All integration tests: PASSING"
    echo ""
    echo "Your Twitter clone backend is working correctly! 🚀"
else
    echo "❌ Some tests are still failing"
    echo "Check the error output above for remaining issues"
fi

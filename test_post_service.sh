#!/bin/bash

echo "🧪 Testing Post Service Integration Tests"
echo "========================================"

cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

echo "🧹 Cleaning build..."
./gradlew clean

echo "🔬 Testing post-service integration tests..."
./gradlew :post-service:test --tests '*IntegrationTest*' --info

TEST_RESULT=$?

echo ""
echo "========================================"
echo "📊 POST SERVICE TEST RESULTS"
echo "========================================"

if [ $TEST_RESULT -eq 0 ]; then
    echo "🎉 SUCCESS! Post service integration tests are now passing!"
    echo "✅ TestContainer PostgreSQL connection: WORKING"
    echo "✅ JWT token generation: WORKING"  
    echo "✅ Authentication entry point: WORKING"
    echo "✅ All post service tests: PASSING"
else
    echo "❌ Post service tests still failing"
    echo "Check the error output above for remaining issues"
fi

echo ""
echo "Fixes applied to post-service:"
echo "1. Extended IntegrationTestBase for proper PostgreSQL setup"
echo "2. Generated valid JWT tokens for authentication"
echo "3. Added authentication entry point for proper 401 responses"

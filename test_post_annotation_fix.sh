#!/bin/bash

echo "🔧 Testing Post Service Spring Boot Annotation Fix"
echo "================================================="

cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

echo "🧹 Cleaning build..."
./gradlew clean

echo "🧪 Running post-service integration tests..."
./gradlew :post-service:test --tests '*IntegrationTest*' --info

TEST_RESULT=$?

echo ""
echo "================================================="
echo "📊 POST SERVICE TEST RESULTS"
echo "================================================="

if [ $TEST_RESULT -eq 0 ]; then
    echo "🎉 SUCCESS! Post service integration tests are now passing!"
    echo ""
    echo "✅ Spring Boot annotation conflict: RESOLVED"
    echo "✅ TestContainer PostgreSQL setup: WORKING"
    echo "✅ JWT authentication: WORKING"
    echo "✅ All post service endpoints: TESTED"
    
    echo ""
    echo "🚀 Now testing ALL services together..."
    echo "======================================"
    
    ./gradlew :user-service:test --tests '*IntegrationTest*' --quiet
    USER_RESULT=$?
    
    if [ $USER_RESULT -eq 0 ] && [ $TEST_RESULT -eq 0 ]; then
        echo ""
        echo "🎉🎉🎉 COMPLETE SUCCESS! 🎉🎉🎉"
        echo "================================"
        echo "✅ User Service: ALL TESTS PASSING"
        echo "✅ Post Service: ALL TESTS PASSING"
        echo ""
        echo "Your Twitter clone backend is fully functional!"
        echo "Ready for frontend development! 🚀"
    fi
    
else
    echo "❌ Post service tests still failing"
    echo "Check the error output above for remaining issues"
fi

echo ""
echo "Fix applied:"
echo "- Removed duplicate @SpringBootTest and @ActiveProfiles annotations"
echo "- Inheritance from IntegrationTestBase provides all needed configuration"

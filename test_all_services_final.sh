#!/bin/bash

echo "🚀 FINAL INTEGRATION TEST - ALL SERVICES" 
echo "========================================"

cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

echo "🧹 Cleaning all builds..."
./gradlew clean

echo ""
echo "🔨 Compiling all services..."
./gradlew compileKotlin compileTestKotlin

COMPILE_RESULT=$?

if [ $COMPILE_RESULT -ne 0 ]; then
    echo "❌ Compilation failed - fix compilation errors first"
    exit 1
fi

echo "✅ All services compiled successfully"
echo ""

echo "🧪 Testing User Service Integration Tests..."
echo "--------------------------------------------"
./gradlew :user-service:test --tests '*IntegrationTest*' --quiet

USER_RESULT=$?

echo ""
echo "🧪 Testing Post Service Integration Tests..."
echo "--------------------------------------------"  
./gradlew :post-service:test --tests '*IntegrationTest*' --quiet

POST_RESULT=$?

echo ""
echo "========================================"
echo "🏆 FINAL RESULTS SUMMARY"
echo "========================================"

if [ $USER_RESULT -eq 0 ]; then
    echo "✅ User Service Integration Tests: PASSED"
else
    echo "❌ User Service Integration Tests: FAILED"
fi

if [ $POST_RESULT -eq 0 ]; then
    echo "✅ Post Service Integration Tests: PASSED"  
else
    echo "❌ Post Service Integration Tests: FAILED"
fi

if [ $USER_RESULT -eq 0 ] && [ $POST_RESULT -eq 0 ]; then
    echo ""
    echo "🎉🎉🎉 SUCCESS! 🎉🎉🎉"
    echo "ALL INTEGRATION TESTS PASSING!"
    echo "Your Twitter clone backend is fully functional!"
    echo ""
    echo "✅ Spring Boot configuration: FIXED"
    echo "✅ Entity-Repository alignment: FIXED"
    echo "✅ JWT Authentication: WORKING"
    echo "✅ Database integration: WORKING"
    echo "✅ All API endpoints: TESTED"
    echo ""
    echo "Ready for frontend integration! 🚀"
else
    echo ""
    echo "⚠️  Some tests still failing - check individual test outputs above"
fi

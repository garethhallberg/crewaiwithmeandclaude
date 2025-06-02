#!/bin/bash

echo "🔨 Testing Post Service Compilation Fix"
echo "======================================"

cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

echo "🧹 Cleaning build..."
./gradlew clean

echo "🔨 Compiling post-service..."
./gradlew :post-service:compileTestKotlin

COMPILE_RESULT=$?

echo ""
echo "======================================"
echo "📊 COMPILATION RESULTS"
echo "======================================"

if [ $COMPILE_RESULT -eq 0 ]; then
    echo "✅ SUCCESS! Post service test compilation successful"
    echo ""
    echo "🧪 Now running integration tests..."
    ./gradlew :post-service:test --tests '*IntegrationTest*' --info
    
    TEST_RESULT=$?
    
    if [ $TEST_RESULT -eq 0 ]; then
        echo ""
        echo "🎉 ALL POST SERVICE INTEGRATION TESTS PASSING!"
    else
        echo ""
        echo "❌ Tests still failing - check output above"
    fi
else
    echo "❌ Compilation still failing"
    echo "Check the error output above"
fi

echo ""
echo "Fix applied:"
echo "- Created local IntegrationTestBase in post-service module"
echo "- Updated import to use local version instead of common module"

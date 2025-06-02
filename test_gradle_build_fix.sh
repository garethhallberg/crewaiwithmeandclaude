#!/bin/bash

echo "🔨 Testing Gradle Build Fix"
echo "==========================="

cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

echo "🧹 Cleaning all builds..."
./gradlew clean

echo "🔨 Testing build configuration..."
./gradlew build

BUILD_RESULT=$?

echo ""
echo "==========================="
echo "📊 BUILD RESULTS"
echo "==========================="

if [ $BUILD_RESULT -eq 0 ]; then
    echo "🎉 SUCCESS! Gradle build is now working!"
    echo ""
    echo "✅ Root project: No longer tries to create bootJar"
    echo "✅ User service: Creates bootJar with UserServiceApplication"
    echo "✅ Post service: Creates bootJar with PostServiceApplication"  
    echo "✅ Common module: Builds as library (no bootJar needed)"
    echo ""
    echo "🧪 Running integration tests to verify everything works..."
    ./gradlew test --tests '*IntegrationTest*' --quiet
    
    TEST_RESULT=$?
    
    if [ $TEST_RESULT -eq 0 ]; then
        echo "✅ All integration tests still passing!"
        echo ""
        echo "🚀 Your Twitter clone backend is ready for deployment!"
        echo "Individual service JARs can be found in:"
        echo "- user-service/build/libs/"
        echo "- post-service/build/libs/"
    else
        echo "⚠️  Build succeeded but some tests failing"
    fi
    
else
    echo "❌ Build still failing"
    echo "Check the error output above for remaining issues"
fi

echo ""
echo "Fix applied:"
echo "- Removed Spring Boot plugin from root project (apply false)"
echo "- Only apply Spring Boot to service modules that need it"
echo "- Root project no longer tries to create bootJar"

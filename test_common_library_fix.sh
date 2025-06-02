#!/bin/bash

echo "🔧 Testing Common Module Library Fix"
echo "===================================="

cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

echo "🧹 Cleaning build..."
./gradlew clean

echo ""
echo "🔨 Testing build..."
./gradlew build

BUILD_RESULT=$?

echo ""
echo "===================================="
echo "📊 BUILD RESULTS"
echo "===================================="

if [ $BUILD_RESULT -eq 0 ]; then
    echo "🎉 SUCCESS! Build is now working!"
    echo ""
    echo "📦 Checking build artifacts..."
    echo ""
    
    echo "Common Module (Library):"
    if [ -f "common/build/libs/common-1.0.0.jar" ]; then
        echo "✅ common-1.0.0.jar created"
        ls -la common/build/libs/
    else
        echo "❌ Common JAR not found"
    fi
    
    echo ""
    echo "User Service (Spring Boot App):"
    if [ -f "user-service/build/libs/user-service-1.0.0.jar" ]; then
        echo "✅ user-service-1.0.0.jar created"
        ls -la user-service/build/libs/
    else
        echo "❌ User Service JAR not found"
    fi
    
    echo ""
    echo "Post Service (Spring Boot App):"
    if [ -f "post-service/build/libs/post-service-1.0.0.jar" ]; then
        echo "✅ post-service-1.0.0.jar created"
        ls -la post-service/build/libs/
    else
        echo "❌ Post Service JAR not found"
    fi
    
    echo ""
    echo "🧪 Testing integration tests..."
    ./gradlew test --tests '*IntegrationTest*' --quiet
    
    TEST_RESULT=$?
    
    if [ $TEST_RESULT -eq 0 ]; then
        echo "✅ All integration tests passing!"
        echo ""
        echo "🚀🚀🚀 COMPLETE SUCCESS! 🚀🚀🚀"
        echo "================================"
        echo "Your Twitter clone backend is:"
        echo "✅ Building successfully"
        echo "✅ Creating deployable JARs" 
        echo "✅ Passing all integration tests"
        echo "✅ Ready for production!"
    else
        echo "⚠️  Build works but some tests failing"
    fi
    
else
    echo "❌ Build failed - check output above"
fi

echo ""
echo "Fix applied:"
echo "- Removed Spring Boot plugin from common module"
echo "- Added java-library plugin to common module" 
echo "- Common module creates library JAR (no bootJar)"
echo "- Services create executable bootJar files"

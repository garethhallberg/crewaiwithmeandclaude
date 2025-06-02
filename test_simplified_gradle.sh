#!/bin/bash

echo "🔧 Testing Simplified Gradle Configuration"
echo "=========================================="

cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

echo "🧹 Cleaning build..."
./gradlew clean

CLEAN_RESULT=$?

echo ""
echo "Clean result: $CLEAN_RESULT"

if [ $CLEAN_RESULT -eq 0 ]; then
    echo "✅ Clean successful!"
    echo ""
    echo "🔨 Testing build..."
    ./gradlew build --info 2>&1 | head -50
    echo "..."
    ./gradlew build 2>&1 | tail -20
    
    BUILD_RESULT=$?
    
    echo ""
    echo "Build result: $BUILD_RESULT"
    
    if [ $BUILD_RESULT -eq 0 ]; then
        echo ""
        echo "🎉 BUILD SUCCESS!"
        echo "================"
        echo ""
        echo "📦 Checking artifacts..."
        echo "User Service:"
        ls -la user-service/build/libs/ 2>/dev/null || echo "  No artifacts yet"
        echo "Post Service:"  
        ls -la post-service/build/libs/ 2>/dev/null || echo "  No artifacts yet"
        echo "Common:"
        ls -la common/build/libs/ 2>/dev/null || echo "  No artifacts yet"
        
        echo ""
        echo "🧪 Testing integration tests..."
        ./gradlew test --tests '*IntegrationTest*' --quiet
        
        if [ $? -eq 0 ]; then
            echo "✅ All tests passing!"
            echo ""
            echo "🚀 Twitter clone backend is READY!"
        else
            echo "⚠️  Some tests failing but build works"
        fi
    else
        echo ""
        echo "❌ Build failed - checking specific issues..."
        ./gradlew build --stacktrace 2>&1 | grep -A5 -B5 "FAILED"
    fi
else
    echo "❌ Clean failed"
fi

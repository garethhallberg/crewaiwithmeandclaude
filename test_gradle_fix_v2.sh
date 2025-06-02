#!/bin/bash

echo "🔧 Testing Gradle Build Fix v2"
echo "=============================="

cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

echo "🧹 Cleaning build..."
./gradlew clean

CLEAN_RESULT=$?

if [ $CLEAN_RESULT -eq 0 ]; then
    echo "✅ Clean successful"
    
    echo ""
    echo "🔨 Testing build..."
    ./gradlew build
    
    BUILD_RESULT=$?
    
    if [ $BUILD_RESULT -eq 0 ]; then
        echo ""
        echo "🎉 SUCCESS! Build is now working!"
        echo ""
        echo "🧪 Testing integration tests..."
        ./gradlew test --tests '*IntegrationTest*' --quiet
        
        TEST_RESULT=$?
        
        if [ $TEST_RESULT -eq 0 ]; then
            echo "✅ All integration tests passing!"
            echo ""
            echo "📦 Checking build artifacts..."
            echo "User Service JAR:"
            ls -la user-service/build/libs/ 2>/dev/null || echo "No JAR found"
            echo "Post Service JAR:"
            ls -la post-service/build/libs/ 2>/dev/null || echo "No JAR found"
            echo ""
            echo "🚀 Your Twitter clone backend is fully operational!"
        else
            echo "⚠️  Build works but some tests failing"
        fi
    else
        echo "❌ Build still failing - check output above"
    fi
else
    echo "❌ Clean failed - check output above"
fi

echo ""
echo "Fix applied:"
echo "- Used proper Gradle DSL syntax for subprojects configuration"
echo "- Used configure<JavaPluginExtension> for Java settings"
echo "- Used string quotes for dependency configuration names"

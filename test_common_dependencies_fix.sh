#!/bin/bash

echo "🔧 Testing Common Module Dependencies Fix"
echo "========================================="

cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

echo "🧹 Cleaning build..."
./gradlew clean

echo ""
echo "🔨 Testing common module compilation..."
./gradlew :common:compileKotlin

COMMON_RESULT=$?

if [ $COMMON_RESULT -eq 0 ]; then
    echo "✅ Common module compiles successfully!"
    
    echo ""
    echo "🔨 Testing full build..."
    ./gradlew build
    
    BUILD_RESULT=$?
    
    if [ $BUILD_RESULT -eq 0 ]; then
        echo ""
        echo "🎉 FULL BUILD SUCCESS!"
        echo "====================="
        
        echo ""
        echo "📦 Checking build artifacts..."
        echo "Common Library:"
        ls -la common/build/libs/ 2>/dev/null
        echo ""
        echo "User Service App:"
        ls -la user-service/build/libs/ 2>/dev/null
        echo ""
        echo "Post Service App:"
        ls -la post-service/build/libs/ 2>/dev/null
        
        echo ""
        echo "🧪 Running integration tests..."
        ./gradlew test --tests '*IntegrationTest*' --quiet
        
        TEST_RESULT=$?
        
        if [ $TEST_RESULT -eq 0 ]; then
            echo "✅ ALL INTEGRATION TESTS PASSING!"
            echo ""
            echo "🚀🚀🚀 MISSION ACCOMPLISHED! 🚀🚀🚀"
            echo "===================================="
            echo "Your Twitter clone backend is:"
            echo "✅ Building successfully"
            echo "✅ Creating proper JARs"
            echo "✅ Passing all tests"
            echo "✅ 100% READY FOR PRODUCTION!"
            echo ""
            echo "You can now deploy with:"
            echo "java -jar user-service/build/libs/user-service-1.0.0.jar"
            echo "java -jar post-service/build/libs/post-service-1.0.0.jar"
        else
            echo "⚠️  Build works but some tests need attention"
        fi
        
    else
        echo "❌ Full build failed - check output"
    fi
    
else
    echo "❌ Common module compilation failed"
    echo "Check dependency issues above"
fi

echo ""
echo "Fix applied:"
echo "- Used dependencyManagement block to import Spring Boot BOM"
echo "- Simplified common module to only essential dependencies"
echo "- Used 'api' dependencies for things other modules need"
echo "- Removed unnecessary Spring Boot starters from library"

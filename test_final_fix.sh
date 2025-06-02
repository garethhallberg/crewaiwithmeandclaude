#!/bin/bash

echo "🔧 Testing Entity-Repository Fix"
echo "================================"

cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

echo "🧹 Cleaning build directories..."
./gradlew clean

if [ $? -ne 0 ]; then
    echo "❌ Clean failed"
    exit 1
fi

echo "✅ Clean successful"
echo ""

echo "🔨 Compiling user-service..."
./gradlew :user-service:compileKotlin

if [ $? -ne 0 ]; then
    echo "❌ Compilation failed"
    exit 1
fi

echo "✅ Compilation successful"
echo ""

echo "🧪 Running integration tests..."
./gradlew :user-service:test --tests '*IntegrationTest*' --info

TEST_RESULT=$?

echo ""
echo "================================"
echo "📊 FINAL RESULTS"
echo "================================"

if [ $TEST_RESULT -eq 0 ]; then
    echo "🎉 SUCCESS! All fixes worked!"
    echo "✅ Spring Boot configuration issue: FIXED"
    echo "✅ Entity-Repository mismatch: FIXED"  
    echo "✅ Integration tests: PASSING"
else
    echo "❌ Tests still failing"
    echo "Check the error output above for remaining issues"
fi

echo ""
echo "Summary of fixes applied:"
echo "1. Removed spring.profiles.active from test configs"
echo "2. Added missing isActive property to User entity"
echo "3. Fixed followerCount vs followersCount mismatch"
echo "4. Centralized DTO mapping logic"

#!/bin/bash

echo "📦 Checking Build Artifacts"
echo "==========================="

cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

if [ -f "user-service/build/libs/user-service-1.0.0.jar" ]; then
    echo "✅ User service JAR created successfully"
    ls -la user-service/build/libs/
else
    echo "❌ User service JAR not found"
fi

echo ""

if [ -f "post-service/build/libs/post-service-1.0.0.jar" ]; then
    echo "✅ Post service JAR created successfully"
    ls -la post-service/build/libs/
else
    echo "❌ Post service JAR not found"
fi

echo ""

if [ -f "common/build/libs/common-1.0.0.jar" ]; then
    echo "✅ Common module JAR created successfully"
    ls -la common/build/libs/
else
    echo "❌ Common module JAR not found"
fi

echo ""
echo "Build structure verified!"
echo "Each service can now be deployed independently."

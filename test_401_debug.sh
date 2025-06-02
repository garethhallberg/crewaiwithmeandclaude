#!/bin/bash

echo "🧪 Testing the Modified 401 Test"
echo "================================"

cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

echo "🧹 Cleaning build..."
./gradlew clean

echo "🔬 Running integration tests..."
./gradlew :user-service:test --tests '*IntegrationTest*' --info

echo ""
echo "Test completed. Check the output above for the DEBUG lines that show the actual status code."

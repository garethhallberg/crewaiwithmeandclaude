#!/bin/bash

echo "🔍 Debugging the 401 Test Failure"
echo "================================="

cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

echo "Running integration tests with detailed output..."
./gradlew :user-service:test --tests '*IntegrationTest*' --info --stacktrace 2>&1 | grep -A 20 -B 5 "should return 401"

echo ""
echo "If that didn't show enough detail, let's run just that one test:"
./gradlew :user-service:test --tests '*should return 401*' --info --stacktrace

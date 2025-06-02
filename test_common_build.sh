#!/bin/bash
cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend
echo "Testing common module build..."
./gradlew :common:build --stacktrace
echo "Build result: $?"

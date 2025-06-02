#!/bin/bash
cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

echo "🧹 Cleaning previous builds..."
./gradlew clean

echo "🔨 Building user-service..."
./gradlew :user-service:build --stacktrace

echo "🔨 Building post-service..."  
./gradlew :post-service:build --stacktrace

echo "🎯 Building everything..."
./gradlew build --stacktrace

echo "✅ Build complete!"

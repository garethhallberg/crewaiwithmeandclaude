#!/bin/bash

echo "🔄 Rebuilding and restarting backend services..."

cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

echo "📦 Building services..."
./gradlew build -x test

echo "🚀 Starting user-service on port 8081..."
java -jar user-service/build/libs/user-service-1.0.0.jar --server.port=8081 &
USER_PID=$!

echo "🚀 Starting post-service on port 8082..."
java -jar post-service/build/libs/post-service-1.0.0.jar --server.port=8082 &
POST_PID=$!

echo "✅ Services started!"
echo "📝 User service PID: $USER_PID"
echo "📝 Post service PID: $POST_PID"

echo "⏳ Waiting for services to start..."
sleep 10

echo "🔍 Testing user service..."
curl -f http://localhost:8081/actuator/health || echo "❌ User service not ready"

echo "🔍 Testing post service..."
curl -f http://localhost:8082/actuator/health || echo "❌ Post service not ready"

echo "🎯 Backend services restarted with post creation fix!"

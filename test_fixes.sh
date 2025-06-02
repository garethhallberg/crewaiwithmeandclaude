#!/bin/bash
cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

echo "🧪 Testing individual service builds..."

echo "1️⃣ Testing user-service compilation..."
./gradlew :user-service:compileKotlin

echo "2️⃣ Testing post-service compilation..."  
./gradlew :post-service:compileKotlin

echo "3️⃣ Testing unit tests..."
./gradlew test --continue

echo "✅ Test results complete!"

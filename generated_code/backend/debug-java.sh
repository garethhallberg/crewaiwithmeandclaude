#!/bin/bash

echo "🔍 Java Environment Troubleshooting Script"
echo "=========================================="

echo ""
echo "📋 Current Java Version:"
java -version 2>&1

echo ""
echo "📋 JAVA_HOME Environment Variable:"
echo "JAVA_HOME = $JAVA_HOME"

echo ""
echo "📋 Available Java Installations:"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    ls -la /Library/Java/JavaVirtualMachines/ 2>/dev/null || echo "No Java installations found in /Library/Java/JavaVirtualMachines/"
    
    echo ""
    echo "📋 Java Home Alternatives on macOS:"
    /usr/libexec/java_home -V 2>/dev/null || echo "java_home utility not available"
else
    # Linux
    ls -la /usr/lib/jvm/ 2>/dev/null || echo "No Java installations found in /usr/lib/jvm/"
fi

echo ""
echo "📋 Gradle Version:"
cd "$(dirname "$0")"
./gradlew -version 2>&1 || echo "Gradle wrapper not working"

echo ""
echo "🔧 RECOMMENDED FIXES:"
echo "1. Install Java 17:"
echo "   macOS: brew install openjdk@17"
echo "   Ubuntu: sudo apt install openjdk-17-jdk"
echo ""
echo "2. Set JAVA_HOME temporarily:"
echo "   export JAVA_HOME=\"/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home\""
echo ""
echo "3. Or uncomment the correct path in gradle.properties"
echo ""
echo "4. Then try: ./gradlew clean build"

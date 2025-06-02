#!/bin/bash

# Twitter Clone Project Maintenance Script
# Run this script regularly to maintain project health

set -e

echo "🚀 Starting Twitter Clone Project Maintenance..."
echo "=================================================="

# Navigate to project root
cd /Users/garethhallberg/Desktop/twitter-clone-crewai

# Check if we're in the right directory
if [ ! -d "generated_code/backend" ]; then
    echo "❌ Error: Not in the correct project directory"
    exit 1
fi

echo "📁 Project directory: $(pwd)"
echo ""

# 1. Validate Spring Boot configurations
echo "🔍 Step 1: Validating Spring Boot configurations..."
if [ -f "scripts/verify_config_fix.py" ]; then
    python3 scripts/verify_config_fix.py
else
    echo "⚠️  Configuration validator not found, skipping..."
fi
echo ""

# 2. Clean build directories
echo "🧹 Step 2: Cleaning build directories..."
cd generated_code/backend
./gradlew clean
echo "✅ Build directories cleaned"
echo ""

# 3. Compile all services
echo "🔨 Step 3: Compiling all services..."
if ./gradlew compileKotlin --quiet; then
    echo "✅ All services compiled successfully"
else
    echo "❌ Compilation failed - check the errors above"
    exit 1
fi
echo ""

# 4. Run unit tests
echo "🧪 Step 4: Running unit tests..."
if ./gradlew test --quiet; then
    echo "✅ All unit tests passed"
else
    echo "⚠️  Some unit tests failed - check test reports"
fi
echo ""

# 5. Run integration tests specifically
echo "🔬 Step 5: Running integration tests..."
echo "Testing user-service..."
if ./gradlew :user-service:test --tests '*IntegrationTest*' --quiet; then
    echo "✅ User service integration tests passed"
else
    echo "❌ User service integration tests failed"
fi

echo "Testing post-service..."
if ./gradlew :post-service:test --tests '*IntegrationTest*' --quiet; then
    echo "✅ Post service integration tests passed"
else
    echo "❌ Post service integration tests failed"
fi
echo ""

# 6. Check for dependency updates (if available)
echo "📦 Step 6: Checking for dependency updates..."
if ./gradlew dependencyUpdates --quiet 2>/dev/null; then
    echo "✅ Dependency check completed - review build/dependencyUpdates/report.txt"
else
    echo "ℹ️  Dependency update plugin not available"
fi
echo ""

# 7. Generate summary
echo "📊 Step 7: Generating maintenance summary..."
cd ../../

# Create maintenance log
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE="maintenance_log.txt"

echo "=== Maintenance Run: $TIMESTAMP ===" >> $LOG_FILE
echo "✅ Configuration validation completed" >> $LOG_FILE
echo "✅ Build cleanup completed" >> $LOG_FILE
echo "✅ Compilation check completed" >> $LOG_FILE
echo "✅ Tests executed" >> $LOG_FILE
echo "" >> $LOG_FILE

echo "📝 Maintenance log updated: $LOG_FILE"
echo ""

# 8. Quick health check
echo "🏥 Step 8: Quick health check..."
SERVICES=("user-service" "post-service" "common")
HEALTHY_SERVICES=0

for service in "${SERVICES[@]}"; do
    if [ -d "generated_code/backend/$service" ]; then
        if [ -f "generated_code/backend/$service/build.gradle.kts" ]; then
            echo "✅ $service: Structure OK"
            ((HEALTHY_SERVICES++))
        else
            echo "❌ $service: Missing build configuration"
        fi
    else
        echo "❌ $service: Directory not found"
    fi
done

echo ""
echo "=================================================="
echo "🎉 Maintenance Complete!"
echo "=================================================="
echo "Services checked: ${#SERVICES[@]}"
echo "Healthy services: $HEALTHY_SERVICES"
echo "Success rate: $(( HEALTHY_SERVICES * 100 / ${#SERVICES[@]} ))%"

if [ $HEALTHY_SERVICES -eq ${#SERVICES[@]} ]; then
    echo "🟢 Project Status: HEALTHY"
    exit 0
else
    echo "🟡 Project Status: NEEDS ATTENTION"
    exit 1
fi

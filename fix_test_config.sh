#!/bin/bash

# Fix Spring Boot test configuration issue
# The problem: spring.profiles.active should not be set in profile-specific config files

echo "Fixing Spring Boot test configuration issue..."

# Navigate to the backend directory
cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend

# Clean all build directories to remove cached config files
echo "Cleaning build directories..."
./gradlew clean

# Verify the fixes are applied correctly
echo "Fixed configuration files:"
echo "=== user-service/src/test/resources/application-test.yml ==="
cat user-service/src/test/resources/application-test.yml
echo ""
echo "=== post-service/src/test/resources/application-test.yml ==="
cat post-service/src/test/resources/application-test.yml

echo ""
echo "Configuration files have been fixed!"
echo "The 'spring.profiles.active: test' property has been removed from profile-specific files."
echo "Tests will now use the @ActiveProfiles(\"test\") annotation to activate the test profile correctly."

echo ""
echo "Running integration tests..."
./gradlew :user-service:test --tests '*IntegrationTest*' --info

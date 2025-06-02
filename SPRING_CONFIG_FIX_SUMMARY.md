# Spring Boot Integration Test Configuration Fix

## Problem Summary

The integration tests were failing with the following error:
```
Property 'spring.profiles.active' imported from location 'class path resource [application-test.yml]' is invalid in a profile specific resource
```

## Root Cause

The issue was caused by setting `spring.profiles.active: test` inside profile-specific configuration files (`application-test.yml`). This creates a circular reference because:

1. Spring Boot loads `application-test.yml` when the `test` profile is active
2. But the file itself was trying to activate the `test` profile
3. This is not allowed in Spring Boot and causes the application context to fail to load

## Solution Applied

### 1. Fixed Configuration Files

Removed the `spring.profiles.active` property from these files:
- `user-service/src/test/resources/application-test.yml`
- `post-service/src/test/resources/application-test.yml`

**Before:**
```yaml
spring:
  profiles:
    active: test
  datasource:
    # ... rest of config
```

**After:**
```yaml
spring:
  datasource:
    # ... rest of config
```

### 2. Proper Profile Activation

The integration test classes already use the correct approach with the `@ActiveProfiles("test")` annotation:

```kotlin
@SpringBootTest(
    classes = [UserServiceApplication::class],
    webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT
)
@ActiveProfiles("test")
class UserServiceIntegrationTest {
    // ... test methods
}
```

## Next Steps

1. **Clean Build Cache:**
   ```bash
   cd /Users/garethhallberg/Desktop/twitter-clone-crewai/generated_code/backend
   ./gradlew clean
   ```

2. **Run Integration Tests:**
   ```bash
   ./gradlew :user-service:test --tests '*IntegrationTest*'
   ./gradlew :post-service:test --tests '*IntegrationTest*'
   ```

## Scripts Created

### 1. `fix_test_config.sh`
A bash script that cleans the build and runs the user service integration tests.

### 2. `scripts/validate_spring_config.py`
A Python script that validates Spring Boot configuration files and detects common issues.

### 3. `scripts/spring_config_manager.py`
A comprehensive CrewAI script that uses multiple agents to analyze, fix, and test Spring Boot configurations.

### 4. `scripts/verify_config_fix.py`
A verification script to check if the configuration fixes were applied correctly.

## Best Practices

1. **Never set `spring.profiles.active` in profile-specific files** (files named `application-{profile}.yml`)
2. **Use `@ActiveProfiles` annotation** in test classes to activate profiles
3. **Use `application.yml`** for default configuration and profile-specific files for overrides
4. **Clean build directories** after configuration changes to avoid cached issues

## Configuration File Structure

```
src/
├── main/resources/
│   ├── application.yml          # Default configuration
│   ├── application-dev.yml      # Development overrides (NO spring.profiles.active)
│   └── application-prod.yml     # Production overrides (NO spring.profiles.active)
└── test/resources/
    └── application-test.yml     # Test overrides (NO spring.profiles.active)
```

## Testing Configuration

For integration tests, use this pattern:

```kotlin
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class MyIntegrationTest {
    // Test methods
}
```

The `@ActiveProfiles("test")` annotation will automatically load `application-test.yml` without needing to specify `spring.profiles.active` in the file itself.

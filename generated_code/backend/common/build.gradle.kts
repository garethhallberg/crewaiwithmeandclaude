plugins {
    kotlin("jvm")
    kotlin("plugin.jpa")
}

dependencies {
    // JPA and validation dependencies
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-validation")
    implementation("jakarta.persistence:jakarta.persistence-api")
    implementation("jakarta.validation:jakarta.validation-api")
    implementation("org.jetbrains.kotlin:kotlin-reflect")
    implementation("com.fasterxml.jackson.core:jackson-annotations")
    
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

// Disable Spring Boot application tasks since this is a library module
tasks.named("bootJar") { enabled = false }
tasks.named("jar") { enabled = true }

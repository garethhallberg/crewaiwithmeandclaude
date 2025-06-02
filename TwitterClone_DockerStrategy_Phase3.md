# Docker Containerization Strategy - Phase 3

### 1. Docker Configuration for Kotlin Spring Boot

#### Dockerfile (Multi-stage build)

```Dockerfile
# Stage 1: Build
FROM maven:3.6.3-jdk-11-slim AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Actual container
FROM openjdk:11-jre-slim
COPY --from=build /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app.jar"]

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/actuator/health || exit 1
```

### 2. Development Environment

#### Docker Compose Configuration

```yaml
version: '3.8'
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      SPRING_PROFILES_ACTIVE: dev
    volumes:
      - .:/app
      - /app/target
    depends_on:
      - postgres
      - redis
  postgres:
    image: postgres:12
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data
  redis:
    image: redis:6
    volumes:
      - redis-data:/data
volumes:
  postgres-data:
  redis-data:
```

### 3. Production Deployment: Kubernetes Manifests

#### Deployment and Service

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kotlin-spring-boot-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: kotlin-app
  template:
    metadata:
      labels:
        app: kotlin-app
    spec:
      containers:
        - name: kotlin-app
          image: <your-docker-image>
          ports:
            - containerPort: 8080
          livenessProbe:
            httpGet:
              path: /actuator/health
              port: 8080
          readinessProbe:
            httpGet:
              path: /actuator/health
              port: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: kotlin-spring-boot-app-service
spec:
  selector:
    app: kotlin-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: LoadBalancer
```

### 4. Container Orchestration with Kubernetes

Ensure the Kubernetes cluster architecture is designed for high availability and scalability, focusing on namespaces for environment segregation, RBAC for security, and ingress controllers for routing.

#### Auto-scaling Configuration

```yaml
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: kotlin-spring-boot-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: kotlin-spring-boot-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 80
```

### 5. Monitoring and Logging

- **Prometheus** for metrics collection, integrated via application's `/actuator/prometheus` endpoint.
- **Grafana** for dashboards.
- Centralized logging with **Elasticsearch, Logstash, and Kibana (ELK)**.

### 6. CI/CD Pipeline Integration

#### GitLab CI/CD Example

```yaml
stages:
  - build
  - deploy

build_app:
  stage: build
  script:
    - docker build -t myregistry.com/myproject/kotlin-app:$CI_COMMIT_REF_SLUG .
    - docker push myregistry.com/myproject/kotlin-app:$CI_COMMIT_REF_SLUG

deploy_to_production:
  stage: deploy
  script:
    - kubectl set image deployment/kotlin-spring-boot-app kotlin-app=myregistry.com/myproject/kotlin-app:$CI_COMMIT_REF_SLUG
  only:
    - master
```

This comprehensive Docker containerization strategy with multi-stage builds, Kubernetes deployment, monitoring setup, and CI/CD integration ensures a secure, scalable, and efficient production environment for the Kotlin Spring Boot backend application.
FROM node:24.14.1-bookworm-slim@sha256:b506e7321f176aae77317f99d67a24b272c1f09f1d10f1761f2773447d8da26c AS frontend
WORKDIR /build/frontend
COPY frontend/package*.json ./
RUN npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

FROM maven:3.9.16-eclipse-temurin-25@sha256:93b8a14ea2f412782e4e842651273b4d903e35cc496284f178fbbe2d67d00976 AS backend
WORKDIR /build
COPY backend/ ./backend/
COPY --from=frontend /build/frontend/dist/ ./backend/application/src/main/resources/static/
RUN mvn -B -q -f backend/pom.xml verify

FROM eclipse-temurin:25.0.3_9-jre@sha256:7c1c6297dc3a3ff947922f3ab14ecd326e29083b9edaa8dbff3b94fef1688311
WORKDIR /app
COPY --from=backend /build/backend/application/target/application-0.1.0-SNAPSHOT.jar /app/erasure.jar
USER 10001:10001
EXPOSE 8080
ENTRYPOINT ["java", "-XX:MaxRAMPercentage=65", "-jar", "/app/erasure.jar"]

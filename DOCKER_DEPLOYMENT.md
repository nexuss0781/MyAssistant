# Ethco AI - Docker Deployment Guide

This guide covers deploying Ethco AI using Docker with both frontend and backend in a unified container.

## 🐳 Docker Deployment Options

### Option 1: Docker Compose (Recommended)
### Option 2: Standalone Docker Container
### Option 3: Development with Docker

---

## 🚀 Quick Start with Docker Compose

### Prerequisites
- Docker and Docker Compose installed
- Gemini API key from Google AI Studio

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd ethco-ai
```

### 2. Environment Configuration
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Build and Run
```bash
# Build and start the application
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

### 4. Access Application
- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 5. Stop Application
```bash
# Stop the application
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## 🔧 Standalone Docker Container

### Build the Image
```bash
docker build -t ethco-ai .
```

### Run the Container
```bash
docker run -d \
  --name ethco-ai-app \
  -p 8000:8000 \
  -e GEMINI_API_KEY=your_gemini_api_key_here \
  -v $(pwd)/sessions:/app/sessions \
  --restart unless-stopped \
  ethco-ai
```

### Container Management
```bash
# View logs
docker logs ethco-ai-app

# Stop container
docker stop ethco-ai-app

# Remove container
docker rm ethco-ai-app

# Remove image
docker rmi ethco-ai
```

---

## 🛠️ Development with Docker

### Development Compose
For development with hot reloading, create `docker-compose.dev.yml`:

```yaml
version: '3.8'

services:
  ethco-backend-dev:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./backend:/app
      - /app/venv  # Exclude venv from volume mount
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    restart: unless-stopped

  ethco-frontend-dev:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules  # Exclude node_modules from volume mount
    environment:
      - VITE_API_URL=http://localhost:8000
    depends_on:
      - ethco-backend-dev
    restart: unless-stopped
```

### Development Commands
```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up --build

# View logs for specific service
docker-compose -f docker-compose.dev.yml logs -f ethco-backend-dev
```

---

## 🏗️ Dockerfile Architecture

### Multi-Stage Build Process

#### Stage 1: Frontend Builder
- Uses `node:18-alpine` for lightweight build
- Installs dependencies and builds React app
- Optimized for production with `npm ci`

#### Stage 2: Python Dependencies
- Uses `python:3.11-slim` base image
- Installs system dependencies for Playwright
- Installs Python packages and Playwright browsers

#### Stage 3: Production Image
- Combines frontend build and backend
- Includes all runtime dependencies
- Configured for security with non-root user
- Health check endpoint included

### Key Features
- **Multi-stage build** for optimized image size
- **Playwright support** with all browser dependencies
- **Security hardening** with non-root user
- **Health checks** for container monitoring
- **Volume mounts** for session persistence

---

## 🔒 Production Deployment

### Environment Variables
```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
PYTHONPATH=/app
PLAYWRIGHT_BROWSERS_PATH=/root/.cache/ms-playwright
```

### Security Considerations
```bash
# Run with non-root user (already configured in Dockerfile)
# Mount volumes with proper permissions
docker run -d \
  --name ethco-ai-prod \
  -p 8000:8000 \
  -e GEMINI_API_KEY=your_api_key \
  -v $(pwd)/sessions:/app/sessions:rw \
  -v $(pwd)/logs:/app/logs:rw \
  --user 1000:1000 \
  --restart unless-stopped \
  --memory=2g \
  --cpus=2 \
  ethco-ai
```

### Reverse Proxy (Nginx)
Create `nginx.conf`:
```nginx
upstream ethco-ai {
    server localhost:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://ethco-ai;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket support
    location /ws/ {
        proxy_pass http://ethco-ai;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 🚀 Cloud Deployment

### Docker Hub
```bash
# Tag and push to Docker Hub
docker tag ethco-ai your-username/ethco-ai:latest
docker push your-username/ethco-ai:latest
```

### AWS ECS
```json
{
  "family": "ethco-ai",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "ethco-ai",
      "image": "your-username/ethco-ai:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "GEMINI_API_KEY",
          "value": "your_api_key_here"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ethco-ai",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Google Cloud Run
```bash
# Deploy to Cloud Run
gcloud run deploy ethco-ai \
  --image gcr.io/your-project/ethco-ai \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_api_key_here \
  --memory 2Gi \
  --cpu 2 \
  --port 8000
```

---

## 📊 Monitoring and Logging

### Health Checks
The container includes built-in health checks:
- **Endpoint**: `/health`
- **Interval**: 30 seconds
- **Timeout**: 30 seconds
- **Retries**: 3

### Container Logs
```bash
# View real-time logs
docker logs -f ethco-ai-app

# Export logs to file
docker logs ethco-ai-app > ethco-ai.log 2>&1
```

### Monitoring with Docker Stats
```bash
# Monitor resource usage
docker stats ethco-ai-app
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Playwright Browser Issues
```bash
# Check Playwright installation
docker exec -it ethco-ai-app playwright --version

# Reinstall browsers if needed
docker exec -it ethco-ai-app playwright install chromium
```

#### 2. Permission Issues
```bash
# Fix session directory permissions
sudo chown -R 1000:1000 ./sessions
```

#### 3. Memory Issues
```bash
# Increase container memory limit
docker update --memory=4g ethco-ai-app
```

#### 4. Port Conflicts
```bash
# Check if port 8000 is in use
netstat -tulpn | grep :8000

# Use different port
docker run -p 8080:8000 ethco-ai
```

### Debug Mode
```bash
# Run container in debug mode
docker run -it --rm \
  -e GEMINI_API_KEY=your_key \
  ethco-ai \
  /bin/bash
```

---

## 📋 Best Practices

### Image Optimization
- Use `.dockerignore` to exclude unnecessary files
- Multi-stage builds to reduce final image size
- Alpine Linux for smaller base images where possible
- Clean up package caches and temporary files

### Security
- Run containers as non-root user
- Use specific image tags instead of `latest`
- Scan images for vulnerabilities
- Limit container resources (CPU, memory)
- Use secrets management for API keys

### Performance
- Use volume mounts for persistent data
- Configure proper health checks
- Set appropriate resource limits
- Use container restart policies
- Monitor container performance

### Maintenance
- Regular image updates
- Automated backups of persistent data
- Log rotation and cleanup
- Monitor disk space usage
- Keep Docker and Docker Compose updated

---

## 🎯 Summary

The Ethco AI Docker deployment provides:
- **Unified Container**: Both frontend and backend in one image
- **Production Ready**: Optimized for performance and security
- **Easy Deployment**: Simple Docker Compose setup
- **Scalable**: Ready for cloud deployment
- **Monitored**: Built-in health checks and logging

Choose the deployment method that best fits your infrastructure and scale requirements!
# Multi-stage Dockerfile for Ethco AI - Frontend + Backend
# Optimized for production deployment with Playwright support

# Stage 1: Build the frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend

# Copy package files and install dependencies
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --only=production

# Copy frontend source and build
COPY frontend/ ./
RUN npm run build

# Stage 2: Setup Python dependencies
FROM python:3.11-slim AS python-deps
WORKDIR /app

# Install system dependencies required for Playwright and Python packages
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    software-properties-common \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Playwright and browsers
RUN playwright install chromium && \
    playwright install-deps

# Stage 3: Final production image
FROM python:3.11-slim
WORKDIR /app

# Install runtime dependencies for Playwright
RUN apt-get update && apt-get install -y \
    # Core system libraries
    libc6 \
    libgcc-s1 \
    libglib2.0-0 \
    libstdc++6 \
    # Playwright browser dependencies
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxss1 \
    libasound2 \
    # Additional dependencies
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libpango-1.0-0 \
    libcairo-gobject2 \
    libdbus-1-3 \
    libatspi2.0-0 \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from deps stage
COPY --from=python-deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=python-deps /usr/local/bin /usr/local/bin

# Copy Playwright browsers from deps stage
COPY --from=python-deps /root/.cache/ms-playwright /root/.cache/ms-playwright

# Copy backend application
COPY backend/ ./

# Copy built frontend from frontend-builder stage
COPY --from=frontend-builder /app/frontend/dist ./static

# Create sessions directory for file operations
RUN mkdir -p ./sessions

# Set environment variables
ENV PYTHONPATH=/app
ENV PLAYWRIGHT_BROWSERS_PATH=/root/.cache/ms-playwright

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose the port
EXPOSE 8000

# Create non-root user for security (optional but recommended)
RUN useradd -m -u 1000 ethco && \
    chown -R ethco:ethco /app
USER ethco

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
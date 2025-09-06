# Stage 1: Build the frontend
FROM node:18-alpine AS frontend
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Setup the backend
FROM python:3.10-slim AS backend
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./

# Stage 3: Final image
FROM python:3.10-slim
WORKDIR /app
COPY --from=backend /app .
COPY --from=frontend /app/frontend/dist ./static

# The port the container will listen on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

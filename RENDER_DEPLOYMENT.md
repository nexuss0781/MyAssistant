# Ethco AI - Render Deployment Guide

This guide provides two deployment strategies for Ethco AI on Render: **Separate Services** (recommended for production) and **Unified Docker** (simpler for development/testing).

## 📋 Prerequisites

- [Render Account](https://render.com) (free tier available)
- GitHub repository with your Ethco AI code
- Gemini API key from Google AI Studio

## 🎯 Deployment Options

### Option 1: Separate Services (Recommended) 

Deploy frontend and backend as separate services for better scalability and resource management.

#### Backend Service (Web Service)

**Render Configuration:**
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt && playwright install chromium`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Environment Variables:**
```
GEMINI_API_KEY=your_gemini_api_key_here
PYTHON_VERSION=3.11.0
```

#### Frontend Service (Static Site)

**Render Configuration:**
- **Root Directory**: `frontend`
- **Build Command**: `npm install && npm run build`
- **Publish Directory**: `dist`

### Option 2: Unified Docker Deployment

Deploy both frontend and backend in a single Docker container.

**Render Configuration (Docker):**
- **Root Directory**: (leave empty - uses repository root)
- **Dockerfile Path**: `./Dockerfile`

---

## 🚀 Step-by-Step Deployment Instructions

### Option 1: Separate Services Deployment

#### Step 1: Deploy Backend Service

1. **Connect Repository**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Backend Service**:
   ```
   Name: ethco-ai-backend
   Root Directory: backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt && playwright install chromium
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

3. **Set Environment Variables**:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   PYTHON_VERSION=3.11.0
   ```

4. **Advanced Settings**:
   - Auto-Deploy: Yes
   - Instance Type: Free (or paid for better performance)

#### Step 2: Deploy Frontend Service

1. **Create Static Site**:
   - Click "New +" → "Static Site"
   - Connect same GitHub repository

2. **Configure Frontend Service**:
   ```
   Name: ethco-ai-frontend
   Root Directory: frontend
   Build Command: npm install && npm run build
   Publish Directory: dist
   ```

3. **Advanced Settings**:
   - Auto-Deploy: Yes
   - Pull Request Previews: Yes (optional)

#### Step 3: Update Frontend Configuration

You need to update the frontend to point to your backend URL:

**File to modify**: `frontend/src/hooks/useWebSocket.js`

```javascript
// Replace localhost URLs with your Render backend URL
const BACKEND_URL = 'https://ethco-ai-backend.onrender.com'; // Replace with your backend URL
const WS_URL = 'wss://ethco-ai-backend.onrender.com'; // Replace with your backend URL

// Update WebSocket connection
const ws = new WebSocket(`${WS_URL}/ws/${clientId}`);

// Update API calls
const response = await fetch(`${BACKEND_URL}/sessions`);
```

**File to modify**: `frontend/src/App.jsx`

```javascript
// Replace all localhost:8000 URLs with your backend URL
const BACKEND_URL = 'https://ethco-ai-backend.onrender.com'; // Replace with your backend URL

// Example updates:
const response = await fetch(`${BACKEND_URL}/sessions`);
const response = await fetch(`${BACKEND_URL}/sessions/${activeSessionId}`);
await fetch(`${BACKEND_URL}/agent/run`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_prompt: prompt,
    session_id: activeSessionId,
    client_id: clientId
  })
});
```

#### Step 4: Update Backend CORS Settings

**File to modify**: `backend/app/main.py`

```python
# Update CORS origins to include your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Keep for local development
        "https://ethco-ai-frontend.onrender.com",  # Add your frontend URL
        "https://your-custom-domain.com"  # Add custom domain if you have one
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Option 2: Unified Docker Deployment

#### Step 1: Update Root Dockerfile

The root Dockerfile needs to be updated to serve the frontend properly:

**File to modify**: `Dockerfile` (root directory)

```dockerfile
# Stage 1: Build the frontend
FROM node:18-alpine AS frontend
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Setup the backend with Playwright
FROM python:3.11-slim AS backend
WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium
RUN playwright install-deps

COPY backend/ ./

# Stage 3: Final image
FROM python:3.11-slim
WORKDIR /app

# Install runtime dependencies for Playwright
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=backend /app .
COPY --from=backend /root/.cache/ms-playwright /root/.cache/ms-playwright
COPY --from=frontend /app/frontend/dist ./static

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Step 2: Update Backend to Serve Frontend

**File to modify**: `backend/app/main.py`

```python
# Uncomment and update the static file serving section
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Add after the CORS middleware setup
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the React app
@app.get("/{catchall:path}")
async def serve_frontend(catchall: str):
    # Serve API routes normally
    if catchall.startswith("api/") or catchall.startswith("ws/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    # Serve React app for all other routes
    return FileResponse("static/index.html")

# Add a root route for the main app
@app.get("/")
async def serve_root():
    return FileResponse("static/index.html")
```

#### Step 3: Deploy to Render

1. **Create Docker Service**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Docker Service**:
   ```
   Name: ethco-ai-unified
   Root Directory: (leave empty)
   Environment: Docker
   Dockerfile Path: ./Dockerfile
   ```

3. **Set Environment Variables**:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   PORT=8000
   ```

---

## 🔧 Environment Variables Reference

### Required for All Deployments:
- `GEMINI_API_KEY`: Your Google Gemini API key

### Backend-Specific (Separate Services):
- `PYTHON_VERSION`: 3.11.0
- `PORT`: Automatically set by Render

### Docker-Specific (Unified):
- `PORT`: 8000 (or use Render's automatic PORT)

## 🌐 Custom Domain Setup (Optional)

1. **Add Custom Domain**:
   - Go to your service settings in Render
   - Navigate to "Custom Domains"
   - Add your domain (e.g., `app.yourdomain.com`)

2. **Update CORS Settings**:
   ```python
   allow_origins=[
       "https://app.yourdomain.com",  # Your custom domain
       "https://ethco-ai-frontend.onrender.com",
       # ... other origins
   ]
   ```

## 🔍 Troubleshooting

### Common Issues:

1. **CORS Errors**:
   - Ensure backend CORS settings include your frontend URL
   - Check that URLs don't have trailing slashes

2. **WebSocket Connection Failed**:
   - Use `wss://` for HTTPS deployments
   - Ensure WebSocket endpoint is correctly configured

3. **Playwright Browser Issues**:
   - For Docker: Ensure all Playwright dependencies are installed
   - For separate services: Playwright should install during build

4. **Build Failures**:
   - Check build logs in Render dashboard
   - Ensure all dependencies are in requirements.txt/package.json

5. **Environment Variables Not Working**:
   - Restart services after adding environment variables
   - Check variable names match exactly (case-sensitive)

### Health Checks:

- **Backend**: `https://your-backend-url/health`
- **API Docs**: `https://your-backend-url/docs`
- **Frontend**: Should load the Ethco AI interface

## 📊 Performance Recommendations

### Separate Services (Production):
- **Backend**: Use paid instance for better performance
- **Frontend**: Free tier is sufficient for static sites
- **Database**: Consider adding PostgreSQL for session storage

### Unified Docker:
- **Instance Type**: Use paid instance (Docker containers need more resources)
- **Memory**: At least 1GB RAM for Playwright browser automation
- **Scaling**: Consider horizontal scaling for high traffic

## 🚀 Post-Deployment Steps

1. **Test All Features**:
   - File operations
   - Terminal commands
   - Browser automation
   - WebSocket connections

2. **Monitor Performance**:
   - Check Render metrics dashboard
   - Monitor response times and error rates

3. **Set Up Monitoring** (Optional):
   - Add health check endpoints
   - Set up uptime monitoring
   - Configure error tracking

4. **Backup Strategy**:
   - Regularly backup session data
   - Consider database for persistent storage

---

## 📝 Summary

- **Separate Services**: Better for production, more scalable, easier to debug
- **Unified Docker**: Simpler deployment, single service to manage
- **File Modifications**: Update API URLs in frontend, CORS settings in backend
- **Environment Variables**: Always set GEMINI_API_KEY and other required variables

Choose the deployment method that best fits your needs and scale requirements!
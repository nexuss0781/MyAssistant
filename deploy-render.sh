#!/bin/bash

# Ethco AI Render Deployment Script
echo "🚀 Ethco AI Render Deployment Helper"
echo "===================================="

# Check if user wants separate or unified deployment
echo ""
echo "Choose deployment method:"
echo "1) Separate Services (Frontend + Backend)"
echo "2) Unified Docker Container"
echo ""
read -p "Enter your choice (1 or 2): " choice

case $choice in
    1)
        echo ""
        echo "📋 SEPARATE SERVICES DEPLOYMENT"
        echo "==============================="
        echo ""
        echo "🔧 Required file modifications:"
        echo ""
        echo "1. Update frontend/src/hooks/useWebSocket.js:"
        echo "   - Replace 'localhost:8000' with 'https://your-backend-url.onrender.com'"
        echo ""
        echo "2. Update frontend/src/App.jsx:"
        echo "   - Replace all 'localhost:8000' with 'https://your-backend-url.onrender.com'"
        echo ""
        echo "3. Update backend/app/main.py CORS settings:"
        echo "   - Add 'https://your-frontend-url.onrender.com' to allow_origins"
        echo ""
        echo "📝 Render Configuration:"
        echo ""
        echo "BACKEND SERVICE:"
        echo "- Root Directory: backend"
        echo "- Build Command: pip install -r requirements.txt && playwright install chromium"
        echo "- Start Command: uvicorn app.main:app --host 0.0.0.0 --port \$PORT"
        echo "- Environment Variables: GEMINI_API_KEY, PYTHON_VERSION=3.11.0"
        echo ""
        echo "FRONTEND SERVICE:"
        echo "- Root Directory: frontend"
        echo "- Build Command: npm install && npm run build"
        echo "- Publish Directory: dist"
        echo ""
        echo "✅ Use render-separate-backend.yaml and render-separate-frontend.yaml as reference"
        ;;
    2)
        echo ""
        echo "🐳 UNIFIED DOCKER DEPLOYMENT"
        echo "============================="
        echo ""
        echo "🔧 Required file modifications:"
        echo ""
        echo "1. Update Dockerfile (root) - already configured for unified deployment"
        echo ""
        echo "2. Update backend/app/main.py:"
        echo "   - Uncomment static file serving sections"
        echo "   - Add frontend serving routes"
        echo ""
        echo "📝 Render Configuration:"
        echo ""
        echo "DOCKER SERVICE:"
        echo "- Root Directory: (empty - repository root)"
        echo "- Dockerfile Path: ./Dockerfile"
        echo "- Environment Variables: GEMINI_API_KEY, PORT=8000"
        echo ""
        echo "✅ Use render-unified.yaml as reference"
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again and choose 1 or 2."
        exit 1
        ;;
esac

echo ""
echo "🔑 Don't forget to:"
echo "- Set your GEMINI_API_KEY in Render environment variables"
echo "- Update any hardcoded URLs with your actual Render service URLs"
echo "- Test all features after deployment"
echo ""
echo "📖 For detailed instructions, see RENDER_DEPLOYMENT.md"
echo ""
echo "🎉 Happy deploying!"
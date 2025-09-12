#!/bin/bash

# Ethco AI Docker Build and Deployment Script
set -e

echo "🐳 Ethco AI Docker Build Script"
echo "==============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
IMAGE_NAME="ethco-ai"
CONTAINER_NAME="ethco-ai-app"
PORT="8000"
BUILD_ONLY=false
RUN_COMPOSE=false

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -b, --build-only    Only build the image, don't run"
    echo "  -c, --compose       Use docker-compose instead of standalone"
    echo "  -n, --name NAME     Set custom image/container name (default: ethco-ai)"
    echo "  -p, --port PORT     Set custom port (default: 8000)"
    echo ""
    echo "Examples:"
    echo "  $0                  # Build and run with default settings"
    echo "  $0 --build-only     # Only build the Docker image"
    echo "  $0 --compose        # Use docker-compose"
    echo "  $0 --name my-ethco --port 8080  # Custom name and port"
    exit 1
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            ;;
        -b|--build-only)
            BUILD_ONLY=true
            shift
            ;;
        -c|--compose)
            RUN_COMPOSE=true
            shift
            ;;
        -n|--name)
            IMAGE_NAME="$2"
            CONTAINER_NAME="${2}-app"
            shift 2
            ;;
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
    esac
done

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  No .env file found. Creating template...${NC}"
    cat > .env << EOF
# Ethco AI Environment Variables
GEMINI_API_KEY=your_gemini_api_key_here
EOF
    echo -e "${YELLOW}📝 Please edit .env file with your actual API key before running.${NC}"
fi

# Function to build Docker image
build_image() {
    echo -e "${BLUE}🔨 Building Docker image: ${IMAGE_NAME}${NC}"
    docker build -t ${IMAGE_NAME} .
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Image built successfully!${NC}"
        
        # Show image info
        echo -e "${BLUE}📊 Image Information:${NC}"
        docker images ${IMAGE_NAME} --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
    else
        echo -e "${RED}❌ Failed to build image${NC}"
        exit 1
    fi
}

# Function to run with docker-compose
run_compose() {
    echo -e "${BLUE}🚀 Starting with Docker Compose...${NC}"
    
    # Check if docker-compose.yml exists
    if [ ! -f "docker-compose.yml" ]; then
        echo -e "${RED}❌ docker-compose.yml not found${NC}"
        exit 1
    fi
    
    # Start services
    docker-compose up --build -d
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Services started successfully!${NC}"
        echo -e "${BLUE}📱 Application URLs:${NC}"
        echo "   Frontend: http://localhost:${PORT}"
        echo "   API Docs: http://localhost:${PORT}/docs"
        echo "   Health Check: http://localhost:${PORT}/health"
        echo ""
        echo -e "${BLUE}🔍 Useful Commands:${NC}"
        echo "   View logs: docker-compose logs -f"
        echo "   Stop services: docker-compose down"
        echo "   Restart: docker-compose restart"
    else
        echo -e "${RED}❌ Failed to start services${NC}"
        exit 1
    fi
}

# Function to run standalone container
run_standalone() {
    echo -e "${BLUE}🚀 Running standalone container...${NC}"
    
    # Stop and remove existing container if it exists
    if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        echo -e "${YELLOW}🔄 Stopping existing container...${NC}"
        docker stop ${CONTAINER_NAME} > /dev/null 2>&1
        docker rm ${CONTAINER_NAME} > /dev/null 2>&1
    fi
    
    # Load environment variables
    if [ -f ".env" ]; then
        export $(grep -v '^#' .env | xargs)
    fi
    
    # Check if API key is set
    if [ -z "${GEMINI_API_KEY}" ] || [ "${GEMINI_API_KEY}" = "your_gemini_api_key_here" ]; then
        echo -e "${YELLOW}⚠️  GEMINI_API_KEY not set or using placeholder value${NC}"
        echo -e "${YELLOW}   Please update your .env file with a valid API key${NC}"
    fi
    
    # Create sessions directory
    mkdir -p ./sessions
    
    # Run container
    docker run -d \
        --name ${CONTAINER_NAME} \
        -p ${PORT}:8000 \
        -e GEMINI_API_KEY="${GEMINI_API_KEY}" \
        -v $(pwd)/sessions:/app/sessions \
        --restart unless-stopped \
        ${IMAGE_NAME}
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Container started successfully!${NC}"
        echo -e "${BLUE}📱 Application URLs:${NC}"
        echo "   Frontend: http://localhost:${PORT}"
        echo "   API Docs: http://localhost:${PORT}/docs"
        echo "   Health Check: http://localhost:${PORT}/health"
        echo ""
        echo -e "${BLUE}🔍 Useful Commands:${NC}"
        echo "   View logs: docker logs -f ${CONTAINER_NAME}"
        echo "   Stop container: docker stop ${CONTAINER_NAME}"
        echo "   Remove container: docker rm ${CONTAINER_NAME}"
        echo "   Enter container: docker exec -it ${CONTAINER_NAME} /bin/bash"
        
        # Wait a moment and check if container is still running
        sleep 3
        if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
            echo -e "${RED}❌ Container stopped unexpectedly. Check logs:${NC}"
            echo "   docker logs ${CONTAINER_NAME}"
        fi
    else
        echo -e "${RED}❌ Failed to start container${NC}"
        exit 1
    fi
}

# Main execution
echo -e "${BLUE}🏗️  Configuration:${NC}"
echo "   Image Name: ${IMAGE_NAME}"
echo "   Container Name: ${CONTAINER_NAME}"
echo "   Port: ${PORT}"
echo "   Build Only: ${BUILD_ONLY}"
echo "   Use Compose: ${RUN_COMPOSE}"
echo ""

# Build the image
build_image

# Exit if build-only mode
if [ "${BUILD_ONLY}" = true ]; then
    echo -e "${GREEN}🎉 Build completed successfully!${NC}"
    exit 0
fi

# Run based on selected mode
if [ "${RUN_COMPOSE}" = true ]; then
    run_compose
else
    run_standalone
fi

echo ""
echo -e "${GREEN}🎉 Ethco AI is now running!${NC}"
echo -e "${BLUE}💡 Tip: Check the health endpoint to ensure everything is working properly${NC}"
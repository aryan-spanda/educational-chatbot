#!/bin/bash
# Docker Build Test Script
# This script tests the Docker builds locally before pushing to CI/CD

echo "🐳 Educational Chatbot - Docker Build Test"
echo "==========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        exit 1
    fi
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Test backend build
print_info "Testing backend Docker build..."
cd src/backend
docker build -t test-backend:local .
print_status $? "Backend build completed"

# Test frontend build  
print_info "Testing frontend Docker build..."
cd ../frontend
docker build -t test-frontend:local .
print_status $? "Frontend build completed"

cd ../../

# Check image sizes
print_info "Checking image sizes..."
echo "Backend image size:"
docker images test-backend:local --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

echo "Frontend image size:"
docker images test-frontend:local --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Optional: Test containers
print_info "Testing container startup (optional)..."
echo "You can now test the containers with:"
echo "  Backend:  docker run -p 8000:8000 test-backend:local"
echo "  Frontend: docker run -p 3000:80 test-frontend:local"

print_info "Cleaning up test images..."
docker rmi test-backend:local test-frontend:local 2>/dev/null || true

echo -e "${GREEN}🎉 All Docker builds successful!${NC}"
echo "The images should build correctly in CI/CD pipeline."

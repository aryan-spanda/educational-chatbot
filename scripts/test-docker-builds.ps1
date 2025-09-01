# Docker Build Test Script (PowerShell)
# This script tests the Docker builds locally before pushing to CI/CD

Write-Host "🐳 Educational Chatbot - Docker Build Test" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan

function Write-Status {
    param($Success, $Message)
    if ($Success) {
        Write-Host "✅ $Message" -ForegroundColor Green
    } else {
        Write-Host "❌ $Message" -ForegroundColor Red
        exit 1
    }
}

function Write-Info {
    param($Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Yellow
}

# Test backend build
Write-Info "Testing backend Docker build..."
Set-Location "src\backend"
$backendResult = docker build -t test-backend:local . 2>&1
$backendSuccess = $LASTEXITCODE -eq 0
Write-Status $backendSuccess "Backend build completed"

# Test frontend build  
Write-Info "Testing frontend Docker build..."
Set-Location "..\frontend"
$frontendResult = docker build -t test-frontend:local . 2>&1
$frontendSuccess = $LASTEXITCODE -eq 0
Write-Status $frontendSuccess "Frontend build completed"

Set-Location "..\.."

# Check image sizes
Write-Info "Checking image sizes..."
Write-Host "Backend image size:"
docker images test-backend:local --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

Write-Host "Frontend image size:"  
docker images test-frontend:local --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Optional: Test containers
Write-Info "Testing container startup (optional)..."
Write-Host "You can now test the containers with:"
Write-Host "  Backend:  docker run -p 8000:8000 test-backend:local"
Write-Host "  Frontend: docker run -p 3000:80 test-frontend:local"

Write-Info "Cleaning up test images..."
docker rmi test-backend:local test-frontend:local 2>$null

Write-Host "🎉 All Docker builds successful!" -ForegroundColor Green
Write-Host "The images should build correctly in CI/CD pipeline."

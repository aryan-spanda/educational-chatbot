# CI/CD Troubleshooting Guide

This guide helps you troubleshoot common issues with the GitHub Actions CI/CD pipeline.

## Common Issues and Solutions

### 1. **Service Discovery Issues**

#### Problem: "Invalid format" or JSON parsing errors
```
Error: Invalid format '  {'
Error: Unable to process file command 'output' successfully.
```

**Solution:**
- Check that Dockerfiles exist in `src/frontend/` and `src/backend/`
- Ensure Dockerfiles are properly formatted
- Verify the `platform-requirements.yml` source_directory is set to `"src/"`

**Debug Steps:**
```bash
# Check if Dockerfiles exist
ls -la src/*/Dockerfile

# Validate platform-requirements.yml
yq e '.cicd.source_directory' platform-requirements.yml
```

### 2. **Docker Authentication Issues**

#### Problem: Authentication failed when pushing to DockerHub
```
Error: denied: requested access to the resource is denied
```

**Solution:**
1. Verify GitHub Actions secrets are set correctly:
   - `DOCKERHUB_USERNAME` = `aryanpola`
   - `DOCKERHUB_TOKEN` = Your DockerHub access token

2. Check DockerHub token permissions:
   - Must have **Read, Write, Delete** permissions
   - Token should not be expired

**Debug Steps:**
```bash
# Test DockerHub login locally
docker login -u aryanpola

# Check if repositories exist on DockerHub
curl -s https://hub.docker.com/v2/repositories/aryanpola/educational-chatbot-frontend/
```

### 3. **Build Context Issues**

#### Problem: Docker build fails with "no such file or directory"
```
Error: failed to solve: failed to read dockerfile
```

**Solution:**
- Ensure Dockerfile paths are correct in the matrix
- Check that build context points to the right directory
- Verify source code exists in the expected locations

**Debug Steps:**
```bash
# Check directory structure
tree src/

# Verify Dockerfile contents
cat src/frontend/Dockerfile
cat src/backend/Dockerfile
```

### 4. **Matrix Strategy Issues**

#### Problem: Matrix job fails or doesn't run
```
Error: The workflow is not valid. Matrix is missing required 'strategy' field
```

**Solution:**
- Ensure service discovery outputs valid JSON
- Check that the `fromJson()` function receives proper input
- Verify the services array is not empty

**Debug in Workflow:**
```yaml
- name: Debug matrix
  run: |
    echo "Services: ${{ needs.discover.outputs.services }}"
    echo "${{ needs.discover.outputs.services }}" | jq .
```

### 5. **Environment Configuration Issues**

#### Problem: Wrong environment or branch not deploying

**Solution:**
1. Check `platform-requirements.yml` deployment_branches:
   ```yaml
   cicd:
     deployment_branches:
       - "main"
       - "develop"
       - "staging"
   ```

2. Verify environment mapping:
   ```yaml
   environment_mapping:
     main: "production"
     develop: "dev"
     staging: "staging"
   ```

### 6. **Security Scanning Issues**

#### Problem: Trivy scan fails or blocks deployment

**Solution:**
- Review scan results in GitHub Security tab
- Update base images to fix vulnerabilities
- Consider adding vulnerability exceptions for false positives

**Example fix:**
```dockerfile
# Update base image
FROM node:18-alpine  # Instead of older versions
FROM python:3.11-slim  # Instead of older versions
```

## Monitoring and Debugging

### GitHub Actions Logs
1. Go to: https://github.com/aryan-spanda/educational-chatbot/actions
2. Click on the failed workflow run
3. Expand the failed job to see detailed logs

### Key Log Sections to Check
- **Config job**: Reads platform-requirements.yml
- **Discover job**: Finds microservices and creates matrix
- **Build job**: Builds and pushes Docker images
- **Security job**: Runs vulnerability scanning

### Useful GitHub Actions Debug Commands

```yaml
# Debug environment variables
- name: Debug environment
  run: |
    echo "Branch: ${{ github.ref_name }}"
    echo "SHA: ${{ github.sha }}"
    echo "Event: ${{ github.event_name }}"
    env

# Debug file structure
- name: Debug files
  run: |
    ls -la
    find . -name "Dockerfile" -type f
    cat platform-requirements.yml

# Debug JSON parsing
- name: Debug JSON
  run: |
    echo '${{ needs.discover.outputs.services }}' | jq .
```

## Manual Testing

### Test Service Discovery Locally
```bash
# Navigate to project root
cd /path/to/educational-chatbot

# Run service discovery script
source_dir="src/"
services="[]"

for dockerfile in $(find "$source_dir" -name "Dockerfile" -type f); do
  service_dir=$(dirname "$dockerfile")
  service_name=$(basename "$service_dir")
  
  service_json=$(jq -n \
    --arg name "$service_name" \
    --arg dockerfile "$dockerfile" \
    --arg context "$service_dir" \
    '{name: $name, dockerfile: $dockerfile, context: $context}')
  
  services=$(echo "$services" | jq --argjson service "$service_json" '. + [$service]')
  echo "Found: $service_name"
done

echo "Final services JSON:"
echo "$services" | jq .
```

### Test Docker Build Locally
```bash
# Test frontend build
docker build -f src/frontend/Dockerfile -t test-frontend src/frontend/

# Test backend build
docker build -f src/backend/Dockerfile -t test-backend src/backend/
```

## Contact and Support

If issues persist:
1. Check the GitHub Actions documentation
2. Review the platform-requirements.yml configuration
3. Verify DockerHub account and permissions
4. Test Docker builds locally before pushing

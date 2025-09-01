# GitHub Actions Secrets Configuration

This document lists the GitHub Actions secrets required for the CI/CD pipeline to function properly.

## Required Secrets

### DockerHub Registry Authentication

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `DOCKERHUB_USERNAME` | Your DockerHub username | `aryanpola` |
| `DOCKERHUB_TOKEN` | DockerHub access token | `dckr_pat_xxxxxxxxxxxxx` |

### How to Configure Secrets

1. Go to your GitHub repository: https://github.com/aryan-spanda/educational-chatbot
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret from the table above

### DockerHub Token Creation

1. Log in to [DockerHub](https://hub.docker.com/)
2. Go to **Account Settings** → **Security**
3. Click **New Access Token**
4. Name it `github-actions-educational-chatbot`
5. Set permissions to **Read, Write, Delete**
6. Copy the generated token and use it as `DOCKERHUB_TOKEN`

## CI/CD Pipeline Behavior

### Image Naming Convention

The pipeline will build and push Docker images with the following naming pattern:
- Frontend: `aryanpola/educational-chatbot-frontend:tag`
- Backend: `aryanpola/educational-chatbot-backend:tag`

### Tag Strategy

| Branch | Tag Format | Example |
|--------|------------|---------|
| `main` | `main-{short-sha}` | `main-a1b2c3d` |
| `develop` | `develop-{short-sha}` | `develop-a1b2c3d` |
| `staging` | `staging-{short-sha}` | `staging-a1b2c3d` |

### Deployment Triggers

- **Push to `main`**: Builds and deploys to production
- **Push to `develop`**: Builds and deploys to development
- **Push to `staging`**: Builds and deploys to staging
- **Pull Request**: Builds images but doesn't deploy

## Security Scanning

The pipeline includes:
- **Trivy vulnerability scanning** for all built images
- **SARIF upload** to GitHub Security tab
- **Build failure** on critical vulnerabilities

## Platform Integration

### ArgoCD Image Updater

The pipeline automatically updates Helm chart values with new image tags through ArgoCD Image Updater, which monitors:
- DockerHub registry: `docker.io`
- Repository pattern: `aryanpola/educational-chatbot-*`
- Update policy: `newest-build`

### Kubernetes Deployment

Images are deployed to Kubernetes using:
- **Helm charts** in `deploy/helm/`
- **Environment-specific values** (dev, staging, production)
- **ArgoCD GitOps** workflow

## Troubleshooting

### Common Issues

1. **Build fails with "authentication failed"**
   - Check `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets
   - Ensure DockerHub token has write permissions

2. **Images not updating in cluster**
   - Verify ArgoCD Image Updater configuration
   - Check ArgoCD Image Updater logs
   - Ensure proper RBAC permissions

3. **Security scan failures**
   - Review Trivy scan results in GitHub Security tab
   - Update base images to fix vulnerabilities
   - Consider adding vulnerability exceptions if needed

### Pipeline Logs

Monitor pipeline execution in:
- **GitHub Actions** → **Workflows** → **Build and Deploy Educational Chatbot**
- **ArgoCD UI** for deployment status
- **Kubernetes logs** for runtime issues

## Next Steps

After configuring secrets:
1. Push changes to trigger the pipeline
2. Monitor the first build in GitHub Actions
3. Verify images are pushed to DockerHub
4. Check ArgoCD for automatic deployment updates

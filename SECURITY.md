#  Security Best Practices

This document outlines security best practices for Artemis City development and deployment.

##  Table of Contents

1. [Environment Variables](#environment-variables)
2. [API Key Management](#api-key-management)
3. [Version Control](#version-control)
4. [Development Workflow](#development-workflow)
5. [Production Deployment](#production-deployment)
6. [Incident Response](#incident-response)

## 🔑 Environment Variables

### Setup

1. **Copy the template:**
   ```bash
   # Root directory
   cp .env.example .env

   # Memory Layer
   cd "Artemis Agentic Memory Layer "
   cp .env.example .env
   ```

2. **Generate secure API keys:**
   ```bash
   # Generate a random API key
   openssl rand -hex 32

   # Or use Python
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

3. **Set appropriate permissions:**
   ```bash
   chmod 600 .env
   chmod 600 "Artemis Agentic Memory Layer /.env"
   ```

### Best Practices

-  **DO** use `.env` files for local development
-  **DO** use different keys for development and production
-  **DO** rotate keys periodically (every 90 days recommended)
-  **DO** use strong, randomly generated keys (32+ characters)
-  **DON'T** commit `.env` files to version control
-  **DON'T** share API keys in chat, email, or documentation
-  **DON'T** hardcode secrets in source code
-  **DON'T** use predictable or weak keys

##  API Key Management

### Key Types

1. **MCP_API_KEY**: Authentication between Python agents and MCP server
2. **OBSIDIAN_API_KEY**: Authentication with Obsidian Local REST API
3. **External API Keys**: OpenAI, Anthropic, GitHub, etc.

### Key Storage

**Local Development:**
```bash
# Use .env files (already in .gitignore)
export MCP_API_KEY=$(cat .env | grep MCP_API_KEY | cut -d '=' -f2)
```

**Production:**
- Use environment variables from hosting platform
- Consider secret management services:
  - AWS Secrets Manager
  - Google Cloud Secret Manager
  - Azure Key Vault
  - HashiCorp Vault

**macOS Keychain:**
```bash
# Store key
security add-generic-password -a artemis -s mcp_api_key -w "your-key-here"

# Retrieve key
security find-generic-password -a artemis -s mcp_api_key -w
```

### Key Rotation

1. Generate new key: `openssl rand -hex 32`
2. Update `.env` files with new key
3. Restart services
4. Update any external systems using the old key
5. Monitor logs for authentication failures
6. Invalidate old key after transition period

## 🚫 Version Control

### Protected Patterns

The `.gitignore` file protects:

- **Environment files**: `.env`, `.env.*`, `.envrc`
- **API keys**: `*.key`, `*.pem`, `secrets/`
- **Credentials**: `credentials.json`, `auth.json`
- **SSH keys**: `id_rsa`, `id_ed25519`, etc.
- **Cloud config**: `.aws/`, `.gcloud/`, `.azure/`

### Pre-commit Checks

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Check for potential secrets in staged files

if git diff --cached --name-only | xargs grep -l "API_KEY\|SECRET\|PASSWORD" 2>/dev/null; then
    echo "  WARNING: Potential secrets detected in staged files!"
    echo "Review the following files:"
    git diff --cached --name-only | xargs grep -l "API_KEY\|SECRET\|PASSWORD" 2>/dev/null
    echo ""
    echo "If these are false positives, you can commit with --no-verify"
    exit 1
fi
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

### Git History Cleanup

If secrets were accidentally committed:

```bash
# Install BFG Repo Cleaner
brew install bfg

# Remove secrets from history
bfg --replace-text passwords.txt  # File with patterns to remove
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (coordinate with team!)
git push --force
```

 **Warning**: This rewrites history. Coordinate with your team!

##  Development Workflow

### Secure Development Practices

1. **Use environment variables:**
   ```python
   import os

   #  Good
   api_key = os.environ.get('MCP_API_KEY')

   #  Bad
   api_key = "abc123"
   ```

2. **Validate input:**
   ```python
   # Check required environment variables on startup
   required_vars = ['MCP_API_KEY', 'OBSIDIAN_API_KEY']
   missing = [var for var in required_vars if not os.environ.get(var)]
   if missing:
       raise EnvironmentError(f"Missing required environment variables: {missing}")
   ```

3. **Never log secrets:**
   ```python
   #  Good
   logger.info("API key configured")

   #  Bad
   logger.info(f"API key: {api_key}")
   ```

4. **Use secure connections:**
   - Always use HTTPS/TLS in production
   - Validate SSL certificates
   - Don't disable certificate verification

### Code Review Checklist

- [ ] No hardcoded secrets
- [ ] No secrets in logs
- [ ] Environment variables used correctly
- [ ] Sensitive data not in comments
- [ ] No debug credentials
- [ ] `.env.example` updated if new variables added

##  Production Deployment

### Environment Variable Setup

**Docker:**
```bash
# Use env_file or environment in docker-compose.yml
docker-compose --env-file .env.production up
```

**Cloud Platform Examples:**

```bash
# Heroku
heroku config:set MCP_API_KEY=xxx

# AWS Elastic Beanstalk
eb setenv MCP_API_KEY=xxx

# Google Cloud Run
gcloud run services update SERVICE_NAME --set-env-vars MCP_API_KEY=xxx
```

### Security Headers

Add to MCP server (Express):

```javascript
app.use(helmet({
  contentSecurityPolicy: true,
  hsts: true,
  noSniff: true,
  frameguard: { action: 'deny' }
}));
```

### Rate Limiting

Protect against brute force attacks:

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});

app.use('/api/', limiter);
```

## 🚨 Incident Response

### If Secrets Are Exposed

**Immediate Actions:**

1. **Rotate compromised keys immediately**
   ```bash
   # Generate new key
   openssl rand -hex 32

   # Update .env
   # Restart services
   ```

2. **Revoke old keys**
   - Update all systems using the key
   - Remove from any external services

3. **Monitor for unauthorized access**
   - Check logs for suspicious activity
   - Look for unexpected API calls
   - Review access patterns

4. **Document the incident**
   - What was exposed?
   - How was it exposed?
   - What actions were taken?
   - What systems were affected?

### Prevention Checklist

- [ ] `.gitignore` is properly configured
- [ ] Pre-commit hooks are installed
- [ ] Environment variables are used for all secrets
- [ ] Team is trained on security practices
- [ ] Regular security audits are scheduled
- [ ] Key rotation schedule is documented

##  Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [Git-secrets](https://github.com/awslabs/git-secrets) - Prevents committing secrets
- [Talisman](https://github.com/thoughtworks/talisman) - Git hooks for secret detection

## 📞 Contact

If you discover a security vulnerability:

1. **DO NOT** create a public GitHub issue
2. Email the maintainer directly
3. Provide details of the vulnerability
4. Allow time for a fix before public disclosure

---

**Remember**: Security is everyone's responsibility!

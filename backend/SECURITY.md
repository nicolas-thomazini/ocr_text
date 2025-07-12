# Security - Family Search OCR AI System

## 🔐 Secret Key

### Automatic Generation
The system automatically generates a **cryptographically secure secret key** using Python's `secrets` module, which uses the operating system's cryptographic random number generator.

### Secret Key Characteristics
- **Size**: 32 bytes (256 bits)
- **Format**: URL-safe base64
- **Entropy**: Cryptographically secure
- **Example**: `<generated_secret_key>`

### Generating a New Secret Key

#### Method 1: Automatic Script (Recommended)
```bash
cd backend
python generate_secret.py
```

This script:
- ✅ Generates a new secure secret key
- ✅ Automatically updates the `.env` file
- ✅ Automatically updates `docker-compose.yml`
- ✅ Provides feedback about the updates

#### Method 2: Manual
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Files Containing the Secret Key

1. **`.env`** - Local configuration
2. **`docker-compose.yml`** - Docker deployment
3. **`env.example`** - Configuration template

## 🛡️ Security Settings

### JWT (JSON Web Tokens)
- **Algorithm**: HS256 (HMAC SHA-256)
- **Expiration**: 30 minutes
- **Secret**: Uses the automatically generated secret key

### CORS (Cross-Origin Resource Sharing)
```python
# Current configuration (development)
CORS(
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**⚠️ For production, specify allowed domains:**
```python
CORS(
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### File Uploads
- **Max size**: 10MB
- **Allowed types**: Images only
- **Validation**: MIME type and extension
- **Storage**: Local file system

### Database
- **Connection**: PostgreSQL with SSL (recommended)
- **Credentials**: Environment variables
- **Backup**: Implement regular backup

## 🔒 Security Best Practices

### 1. Secret Key
- ✅ **Never commit** the secret key to the repository
- ✅ **Use environment variables** in production
- ✅ **Generate a new key** for each environment
- ✅ **Keep a secure backup** of your keys

### 2. Production
- ✅ **Use HTTPS** for all communications
- ✅ **Configure CORS** properly
- ✅ **Implement rate limiting**
- ✅ **Use a firewall** to protect the API
- ✅ **Monitor security logs**

### 3. Sensitive Data
- ✅ **Encrypt** sensitive data in the database
- ✅ **Implement secure backup**
- ✅ **Control access** to data
- ✅ **Audit** access regularly

### 4. Deployment
- ✅ **Use secrets management** (Docker Secrets, Kubernetes Secrets)
- ✅ **Configure SSL/TLS** properly
- ✅ **Implement health checks**
- ✅ **Use containers** for isolation

## 🚨 Security Checklist

### Before Deployment
- [ ] Unique and secure secret key
- [ ] Properly configured CORS
- [ ] HTTPS enabled
- [ ] Rate limiting implemented
- [ ] Security logs configured
- [ ] Data backup configured

### Continuous Monitoring
- [ ] Access logs monitored
- [ ] Suspicious access attempts
- [ ] Application performance
- [ ] Resource usage
- [ ] Security errors

### Maintenance
- [ ] Regular security updates
- [ ] Secret key rotation
- [ ] Permission audits
- [ ] Penetration testing
- [ ] Backup and recovery tested

## 🔧 Production Configuration

### Critical Environment Variables
```bash
# Required
SECRET_KEY=your-super-secure-secret-key
DATABASE_URL=postgresql://user:pass@host:port/db?sslmode=require

# Recommended
ENVIRONMENT=production
LOG_LEVEL=warning
CORS_ORIGINS=https://your-domain.com
```

### Docker Secrets (Recommended)
```yaml
version: '3.8'
services:
  app:
    secrets:
      - secret_key
      - db_password

secrets:
  secret_key:
    external: true
  db_password:
    external: true
```

## 📞 Reporting Security Issues

If you find a security issue:

1. **DO NOT** open a public issue
2. **DO NOT** discuss in public forums
3. **Contact** the maintainers directly
4. **Provide specific details** about the issue
5. **Wait for a response** before disclosing

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Python Security](https://python-security.readthedocs.io/)
- [Docker Security](https://docs.docker.com/engine/security/) 
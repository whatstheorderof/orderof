# OrderOf.org Deployment Guide

## Quick Start

### Prerequisites
- Node.js 20+ and pnpm
- Python 3.11+ with pip
- Git

### Local Development Setup

1. **Clone and Setup Backend**
```bash
# Backend is already created in orderof_backend/
cd orderof_backend
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

2. **Setup Frontend**
```bash
# Frontend is already created in orderof_frontend/
cd orderof_frontend
pnpm install
pnpm run dev --host
```

3. **Access the Application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

## Production Deployment Options

### Option 1: Full-Stack Deployment (Recommended)

#### Step 1: Prepare the Application
```bash
# Build the frontend
cd orderof_frontend
pnpm run build

# Copy built files to Flask static directory
cp -r dist/* ../orderof_backend/src/static/
```

#### Step 2: Update Flask to Serve Frontend
```python
# Add to orderof_backend/src/main.py
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
```

#### Step 3: Deploy Backend
```bash
cd orderof_backend
# Deploy using the service_deploy_backend tool
```

### Option 2: Separate Frontend/Backend Deployment

#### Frontend Deployment
```bash
cd orderof_frontend
pnpm run build
# Deploy using the service_deploy_frontend tool
```

#### Backend Deployment
```bash
cd orderof_backend
# Deploy using the service_deploy_backend tool
```

## Environment Configuration

### Production Environment Variables
```bash
# Create .env file in orderof_backend/
FLASK_ENV=production
TMDB_API_KEY=8b459b6f6aa0f76b7bf3fba33086cb81
RAWG_API_KEY=e27f4f6149ec4c358472cfd6913e6d85
AMAZON_UK_TAG=your-uk-affiliate-tag
AMAZON_US_TAG=your-us-affiliate-tag
DATABASE_URL=sqlite:///production.db  # or PostgreSQL URL
```

### Frontend Environment Variables
```bash
# Create .env file in orderof_frontend/
VITE_API_BASE_URL=https://your-backend-domain.com
```

## Database Migration

### For Production
1. **Backup Current Data**
```bash
sqlite3 src/database/app.db ".backup backup.db"
```

2. **Migrate to PostgreSQL** (Recommended for production)
```python
# Update database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@host:port/dbname'
```

## Performance Optimization

### Frontend Optimizations
1. **Enable Gzip Compression**
2. **Implement CDN for Static Assets**
3. **Optimize Images**
4. **Enable Browser Caching**

### Backend Optimizations
1. **Add Redis Caching**
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})
```

2. **Database Connection Pooling**
3. **API Response Caching**
4. **Rate Limiting**

## Monitoring and Analytics

### Application Monitoring
```python
# Add to Flask app
from flask import request
import logging

@app.before_request
def log_request_info():
    logging.info('Request: %s %s', request.method, request.url)
```

### Analytics Integration
```html
<!-- Add to index.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## Security Checklist

### Backend Security
- [ ] Enable HTTPS
- [ ] Set secure headers
- [ ] Implement rate limiting
- [ ] Validate all inputs
- [ ] Use environment variables for secrets
- [ ] Enable CORS properly

### Frontend Security
- [ ] Sanitize user inputs
- [ ] Implement CSP headers
- [ ] Use HTTPS for all requests
- [ ] Validate API responses

## Backup Strategy

### Database Backup
```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
sqlite3 /path/to/app.db ".backup /backups/orderof_$DATE.db"
```

### File Backup
- Static assets
- Configuration files
- SSL certificates

## Troubleshooting

### Common Issues

1. **CORS Errors**
```python
# Ensure CORS is properly configured
from flask_cors import CORS
CORS(app, origins=['https://your-frontend-domain.com'])
```

2. **API Rate Limits**
```python
# Implement exponential backoff
import time
import random

def api_call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(2 ** attempt + random.uniform(0, 1))
```

3. **Database Connection Issues**
```python
# Add connection pooling and retry logic
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

## Maintenance Tasks

### Weekly Tasks
- [ ] Check API rate limit usage
- [ ] Review error logs
- [ ] Update franchise data
- [ ] Monitor affiliate link performance

### Monthly Tasks
- [ ] Database optimization
- [ ] Security updates
- [ ] Performance review
- [ ] Backup verification

### Quarterly Tasks
- [ ] API integration updates
- [ ] Feature usage analysis
- [ ] Cost optimization review
- [ ] Security audit

## Scaling Considerations

### Horizontal Scaling
1. **Load Balancer Setup**
2. **Multiple Backend Instances**
3. **Database Read Replicas**
4. **CDN Implementation**

### Vertical Scaling
1. **Increase Server Resources**
2. **Database Optimization**
3. **Caching Implementation**
4. **Code Optimization**

## Support and Maintenance

### Log Monitoring
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/orderof.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
```

### Health Check Endpoint
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
```

---

*This deployment guide ensures a smooth transition from development to production for OrderOf.org.*


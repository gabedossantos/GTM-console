# JourneyLens Deployment Guide
## Customer Intelligence Console - Complete Setup Instructions

### Overview
JourneyLens is a lightweight internal console that ingests customer interactions, generates structured insights, and provides role-based views for GTM teams. This guide covers the complete deployment process from development to production.

## Prerequisites

### System Requirements
- **Python 3.9+** for backend services
- **Node.js 18+** for frontend development
- **PostgreSQL 14+** or SQLite for development
- **Redis** (optional, for caching and task queues)
- **Docker** (recommended for containerized deployment)

### Development Tools
- **VS Code** with Python and TypeScript extensions
- **Git** for version control
- **Postman** or similar for API testing

## Quick Start (Development)

### 1. Backend Setup (FastAPI)

```bash
# Clone and setup backend
mkdir journeylens && cd journeylens
git init

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2 python-multipart

# Copy the backend code (journeylens_backend.py)
# Update database URL and API keys in code

# Run development server
uvicorn journeylens_backend:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup (Next.js)

```bash
# Create Next.js project
npx create-next-app@latest journeylens-frontend --typescript --tailwind --eslint
cd journeylens-frontend

# Install additional dependencies
npm install axios react-query recharts @headlessui/react @heroicons/react
npm install @hookform/resolvers zod lucide-react clsx tailwind-merge

# Copy frontend components and pages
# Update API_BASE_URL in lib/api.ts

# Run development server
npm run dev
```

### 3. Database Initialization

```python
# Create database tables
from journeylens_backend import Base, engine
Base.metadata.create_all(bind=engine)

# Or run migrations if using Alembic
alembic upgrade head
```

### 4. Load Demo Data

```bash
# Use the generated CSV files to populate database
python load_demo_data.py

# Or manually upload conversation files through the UI
```

## Production Deployment

### Option 1: Docker Deployment

#### Backend Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "journeylens_backend:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Dockerfile
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

CMD ["node", "server.js"]
```

#### Docker Compose
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: journeylens
      POSTGRES_USER: journeylens
      POSTGRES_PASSWORD: your_secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://journeylens:your_secure_password@postgres:5432/journeylens
      OPENAI_API_KEY: your_openai_api_key
    ports:
      - "8000:8000"
    depends_on:
      - postgres

  frontend:
    build: ./frontend
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### Option 2: Cloud Deployment (Vercel + Railway)

#### Vercel Frontend Deployment
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy frontend
cd journeylens-frontend
vercel --prod

# Set environment variables in Vercel dashboard:
# NEXT_PUBLIC_API_URL=https://your-backend-url.up.railway.app
```

#### Railway Backend Deployment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway add postgresql
railway deploy

# Set environment variables:
# API_KEY=your_api_key
# DATABASE_URL will be automatically set by Railway
```

## Configuration

### Environment Variables

#### Backend (.env)
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/journeylens
API_KEY=your-api-key
SECRET_KEY=your-jwt-secret-key
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
ENVIRONMENT=production
```

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_ENV=development
```

### Insight Engine Configuration

You can replace the default heuristic engine with your own logic or connect to external services as needed.

## Security Setup

### Authentication
```python
# JWT token configuration
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication

SECRET = "your-secret-key"
jwt_authentication = JWTAuthentication(
    secret=SECRET, 
    lifetime_seconds=3600,
    tokenUrl="/auth/login"
)
```

### CORS Configuration
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Rate Limiting
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/api/insights")
@limiter.limit("10/minute")
async def get_insights(request: Request):
    # API endpoint with rate limiting
    pass
```

## Monitoring & Observability

### Logging Setup
```python
import logging
from pythonjsonlogger import jsonlogger

# Configure structured logging
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
```

### Health Checks
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0"
    }

@app.get("/health/db")
async def db_health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"database": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Database unhealthy")
```

### Metrics Collection
```python
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests')
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')

@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    
    REQUEST_COUNT.inc()
    REQUEST_LATENCY.observe(time.time() - start_time)
    
    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest())
```

## Performance Optimization

### Database Optimization
```python
# Add database indexes
from sqlalchemy import Index

# Create indexes for common queries
Index('idx_interactions_account_timestamp', 
      Interaction.account_id, Interaction.timestamp)
Index('idx_insights_risk_score', Insight.risk_score)
Index('idx_feedback_rating', Feedback.rating)
```

### Caching Layer
```python
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache(expiry=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, expiry, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache(expiry=600)
async def get_dashboard_data(role: str, user_id: str):
    # Cached dashboard data
    pass
```

### Background Tasks
```python
from celery import Celery

celery_app = Celery('journeylens', broker='redis://localhost:6379')

@celery_app.task
def process_uploaded_file(file_path: str, account_id: int):
    # Process large file uploads in background
    pass

@celery_app.task
def generate_weekly_reports():
    # Generate automated reports
    pass
```

## Testing Strategy

### Unit Tests
```python
import pytest
from fastapi.testclient import TestClient
from journeylens_backend import app

client = TestClient(app)

def test_create_interaction():
    response = client.post("/interactions/", json={
        "account_id": 1,
        "channel": "email",
        "content": "Test interaction content"
    })
    assert response.status_code == 200
    assert "intent" in response.json()

def test_insight_analysis():
    from journeylens_backend import InsightService
    
    insight_service = InsightService()
    result = insight_service.analyze_interaction("I want to cancel my subscription")
    
    assert "intent" in result
    assert "sentiment" in result
```

### Integration Tests
```python
@pytest.mark.integration
def test_full_workflow():
    # Test complete workflow: upload -> process -> insights -> feedback
    # Upload file
    response = client.post("/upload/conversations", 
                          files={"files": ("test.txt", "test content", "text/plain")})
    
    # Check insights generated
    insights = client.get("/insights/").json()
    assert len(insights) > 0
    
    # Submit feedback
    feedback_response = client.post("/feedback/", json={
        "insight_id": insights[0]["id"],
        "rating": True,
        "reason_code": "accurate"
    })
    assert feedback_response.status_code == 200
```

## Maintenance

### Database Migrations
```bash
# Using Alembic for schema changes
alembic init migrations
alembic revision --autogenerate -m "Add new table"
alembic upgrade head
```

### Backup Strategy
```bash
# Database backups
pg_dump journeylens > backup_$(date +%Y%m%d).sql

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump journeylens | gzip > /backups/journeylens_$DATE.sql.gz

# Keep only last 30 days of backups
find /backups -name "journeylens_*.sql.gz" -mtime +30 -delete
```

### Log Rotation
```bash
# Logrotate configuration
/var/log/journeylens/*.log {
    daily
    missingok
    rotate 30
    compress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload journeylens
    endscript
}
```

## Scaling Considerations

### Horizontal Scaling
- **Load Balancer**: NGINX or AWS ALB
- **Multiple Backend Instances**: Scale FastAPI with Gunicorn
- **Database Read Replicas**: PostgreSQL streaming replication
- **CDN**: CloudFlare or AWS CloudFront for static assets

### Vertical Scaling
- **Database**: Increase PostgreSQL memory and CPU
    # (Optional) GPU instances for advanced analysis
- **Caching**: Redis cluster for distributed caching

## Troubleshooting

### Common Issues

#### 1. Analysis Failures
```python
# Implement fallback analysis
return {
    "intent": "analysis_failed",
    "sentiment": "neutral",
    "risk_score": 0.5,
    "confidence": 0.1
}
```

#### 2. Database Connection Issues
```python
# Add connection pooling
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

#### 3. Frontend API Errors
```typescript
// Add retry logic
const apiWithRetry = axios.create({
  timeout: 10000,
  retry: 3,
  retryDelay: 1000
});
```

### Log Analysis
```bash
# Common log queries
grep "ERROR" /var/log/journeylens/app.log | tail -50
grep "risk_score.*0.[89]" /var/log/journeylens/app.log  # High risk detections

```

## Success Metrics

### Technical KPIs
- **API Response Time**: <200ms p95
- **Analysis Accuracy**: >85% on evaluation set
- **System Uptime**: >99.5%
- **Database Query Performance**: <50ms average

### Business KPIs
- **User Engagement**: Daily active users
- **Insight Quality**: Feedback useful rate >80%
- **GTM Efficiency**: Time saved per user per day
- **Customer Satisfaction**: NPS score from GTM teams

---

## Next Steps

1. **Deploy to staging environment**
2. **Load test with realistic data volumes**
3. **Train GTM teams on new workflows**
4. **Implement monitoring and alerting**
5. **Plan production rollout strategy**

This deployment guide provides a comprehensive foundation for implementing JourneyLens in production. Adjust configurations based on your specific infrastructure and requirements.
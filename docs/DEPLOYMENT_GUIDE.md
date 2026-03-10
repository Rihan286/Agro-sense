# AgroSense Deployment Guide

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Production Deployment](#production-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)

---

## Local Development Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Step 1: Clone and Setup

```bash
# Navigate to project directory
cd agrosense

# Run setup script (Unix/Mac)
chmod +x setup.sh
./setup.sh

# Or manually setup:
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy example environment file
cp backend/.env.example backend/.env

# Edit .env file and add your API keys
nano backend/.env  # or use any text editor
```

Required API keys:
- `OPENWEATHER_API_KEY`: Get from https://openweathermap.org/api

### Step 3: Run Backend

```bash
cd backend
python app.py
```

Backend will start at: `http://localhost:5000`

### Step 4: Run Frontend

**Option 1: Direct File Access**
```bash
# Simply open in browser
cd frontend
open index.html  # Mac
# or double-click index.html
```

**Option 2: Python HTTP Server (Recommended)**
```bash
cd frontend
python -m http.server 8000
```

Access at: `http://localhost:8000`

**Option 3: Node.js HTTP Server**
```bash
cd frontend
npx http-server -p 8000
```

---

## Production Deployment

### Backend Deployment

#### Using Gunicorn (Recommended)

```bash
# Install gunicorn (already in requirements.txt)
pip install gunicorn

# Run with gunicorn
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Configuration for production:
```bash
# Create gunicorn config
nano gunicorn.conf.py
```

```python
# gunicorn.conf.py
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
errorlog = "logs/error.log"
accesslog = "logs/access.log"
loglevel = "info"
```

Run with config:
```bash
gunicorn -c gunicorn.conf.py app:app
```

#### Using uWSGI

```bash
# Install uwsgi
pip install uwsgi

# Run
uwsgi --http 0.0.0.0:5000 --module app:app --processes 4
```

### Frontend Deployment

#### Using Nginx

```nginx
# /etc/nginx/sites-available/agrosense

server {
    listen 80;
    server_name agrosense.yourdomain.com;
    
    root /var/www/agrosense/frontend;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    # Proxy API requests to backend
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Enable gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/agrosense /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL/HTTPS with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d agrosense.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Docker Deployment

### Create Dockerfile for Backend

```dockerfile
# backend/Dockerfile

FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Create Dockerfile for Frontend

```dockerfile
# frontend/Dockerfile

FROM nginx:alpine

# Copy frontend files
COPY . /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
```

### Docker Compose

```yaml
# docker-compose.yml

version: '3.8'

services:
  backend:
    build: ./backend
    container_name: agrosense-backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - OPENWEATHER_API_KEY=${OPENWEATHER_API_KEY}
    volumes:
      - ./backend/uploads:/app/uploads
      - ./backend/models:/app/models
    restart: unless-stopped

  frontend:
    build: ./frontend
    container_name: agrosense-frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

Run with Docker Compose:
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Cloud Deployment

### AWS Deployment

#### Using EC2

1. **Launch EC2 Instance**
   - Choose Ubuntu 20.04 LTS
   - Instance type: t2.medium or higher
   - Configure security groups (ports 80, 443, 5000)

2. **Setup Server**
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx -y

# Clone your repository
git clone https://github.com/yourusername/agrosense.git
cd agrosense

# Run setup
./setup.sh
```

3. **Configure Nginx and SSL**
   - Follow production deployment steps above

#### Using Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.9 agrosense

# Create environment
eb create agrosense-env

# Deploy
eb deploy

# Check status
eb status
```

### Google Cloud Platform

#### Using App Engine

```yaml
# app.yaml

runtime: python39

entrypoint: gunicorn -b :$PORT app:app

env_variables:
  OPENWEATHER_API_KEY: "your-key"

automatic_scaling:
  min_instances: 1
  max_instances: 10
```

Deploy:
```bash
gcloud app deploy
```

### Heroku Deployment

```bash
# Create Procfile
echo "web: gunicorn app:app" > backend/Procfile

# Create runtime.txt
echo "python-3.9.16" > backend/runtime.txt

# Deploy
cd backend
heroku create agrosense-api
heroku config:set OPENWEATHER_API_KEY=your-key
git push heroku main
```

### DigitalOcean

1. Create Droplet (Ubuntu 20.04)
2. Follow EC2 setup steps
3. Use DigitalOcean's managed database for PostgreSQL (if needed)
4. Setup load balancer for scaling

---

## Environment Variables

### Development
```bash
FLASK_ENV=development
DEBUG=True
```

### Production
```bash
FLASK_ENV=production
DEBUG=False
SECRET_KEY=your-secure-random-key
OPENWEATHER_API_KEY=your-key
DATABASE_URL=your-database-url  # if using database
```

---

## Monitoring and Logging

### Setup Logging

```python
# backend/app.py

import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    # File handler
    file_handler = RotatingFileHandler(
        'logs/agrosense.log',
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('AgroSense startup')
```

### Monitoring Tools

1. **Application Performance Monitoring**
   - New Relic
   - Datadog
   - Sentry (for error tracking)

2. **Server Monitoring**
   - Prometheus + Grafana
   - CloudWatch (AWS)
   - Stackdriver (GCP)

---

## Backup and Recovery

### Database Backup (if using database)
```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump agrosense_db > backups/agrosense_$DATE.sql
```

### Application Backup
```bash
# Backup uploads and models
tar -czf backup_$DATE.tar.gz backend/uploads backend/models
```

---

## Security Checklist

- [ ] Use HTTPS (SSL/TLS certificates)
- [ ] Set strong SECRET_KEY
- [ ] Enable CORS only for trusted domains
- [ ] Implement rate limiting
- [ ] Use environment variables for sensitive data
- [ ] Keep dependencies updated
- [ ] Implement input validation
- [ ] Use secure headers (helmet.js equivalent)
- [ ] Regular security audits
- [ ] Implement authentication (for production)

---

## Troubleshooting

### Backend not starting
```bash
# Check Python version
python --version

# Check if port is in use
lsof -i :5000

# Check logs
tail -f logs/error.log
```

### CORS errors
- Verify CORS_ORIGINS in .env
- Check browser console for specific error
- Ensure backend is running

### API Key errors
- Verify .env file exists
- Check API key is valid
- Ensure environment variables are loaded

---

## Performance Optimization

1. **Backend**
   - Use caching (Redis)
   - Optimize database queries
   - Enable gzip compression
   - Use CDN for static assets

2. **Frontend**
   - Minify CSS/JS
   - Optimize images
   - Enable browser caching
   - Use lazy loading

3. **Model Inference**
   - Use TensorFlow Lite for mobile
   - Batch predictions when possible
   - Consider GPU acceleration

---

## Scaling

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Deploy multiple backend instances
- Use session store (Redis)

### Vertical Scaling
- Increase server resources
- Optimize code performance
- Use caching extensively

---

For additional help, refer to:
- Flask documentation: https://flask.palletsprojects.com/
- Gunicorn documentation: https://docs.gunicorn.org/
- Nginx documentation: https://nginx.org/en/docs/

---

**Last Updated:** February 2024
**Version:** 1.0.0

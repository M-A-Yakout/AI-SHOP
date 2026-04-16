# Deployment Guide

## Quick Start Deployment

### Local Development

1. **Setup**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
```

2. **Database**
```bash
python manage.py makemigrations
python manage.py migrate
python seed_data.py
```

3. **Run**
```bash
python manage.py runserver
```

### Production Deployment Options

## Option 1: Heroku

1. **Install Heroku CLI**
```bash
heroku login
```

2. **Create app**
```bash
heroku create your-app-name
```

3. **Add PostgreSQL**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. **Set environment variables**
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set OPENAI_API_KEY=your-openai-key
```

5. **Deploy**
```bash
git push heroku main
heroku run python manage.py migrate
heroku run python seed_data.py
```

## Option 2: AWS EC2

1. **Launch EC2 instance** (Ubuntu 22.04)

2. **SSH into instance**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. **Install dependencies**
```bash
sudo apt update
sudo apt install python3-pip python3-venv postgresql nginx
```

4. **Clone project**
```bash
git clone your-repo-url
cd project
```

5. **Setup virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. **Configure PostgreSQL**
```bash
sudo -u postgres psql
CREATE DATABASE ecommerce_db;
CREATE USER ecommerce_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;
\q
```

7. **Setup environment**
```bash
cp .env.example .env
# Edit .env with production values
```

8. **Run migrations**
```bash
python manage.py migrate
python manage.py collectstatic
python seed_data.py
```

9. **Setup Gunicorn service**
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/project
ExecStart=/home/ubuntu/project/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/project/gunicorn.sock config.wsgi:application

[Install]
WantedBy=multi-user.target
```

10. **Start Gunicorn**
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

11. **Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/ecommerce
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ubuntu/project;
    }
    
    location /media/ {
        root /home/ubuntu/project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/project/gunicorn.sock;
    }
}
```

12. **Enable site**
```bash
sudo ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## Option 3: Docker

1. **Create Dockerfile**
```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

2. **Create docker-compose.yml**
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ecommerce_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

3. **Deploy**
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python seed_data.py
```

## Option 4: DigitalOcean App Platform

1. **Connect GitHub repository**
2. **Configure build settings**
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn config.wsgi:application`
3. **Add PostgreSQL database**
4. **Set environment variables**
5. **Deploy**

## Post-Deployment Checklist

- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up PostgreSQL
- [ ] Configure static files serving
- [ ] Set up SSL certificate
- [ ] Configure email backend
- [ ] Set up monitoring (Sentry)
- [ ] Configure backups
- [ ] Set up CI/CD pipeline
- [ ] Load test the application
- [ ] Set up logging
- [ ] Configure rate limiting
- [ ] Set up CDN for media files

## Environment Variables for Production

```env
SECRET_KEY=generate-strong-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_ENGINE=postgresql
DB_NAME=ecommerce_db
DB_USER=your_db_user
DB_PASSWORD=strong_password
DB_HOST=your_db_host
DB_PORT=5432
OPENAI_API_KEY=your_openai_key
AI_MOCK_MODE=False
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

## Monitoring Setup

### Sentry (Error Tracking)

```bash
pip install sentry-sdk
```

Add to settings.py:
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
)
```

## Backup Strategy

### Database Backups

```bash
# Backup
pg_dump -U username dbname > backup.sql

# Restore
psql -U username dbname < backup.sql
```

### Automated Backups (Cron)

```bash
crontab -e
```

Add:
```
0 2 * * * pg_dump -U username dbname > /backups/db_$(date +\%Y\%m\%d).sql
```

## Scaling Tips

1. **Database**: Use connection pooling (pgBouncer)
2. **Caching**: Implement Redis
3. **Static Files**: Use CDN (CloudFront, Cloudflare)
4. **Media Files**: Use S3 or similar
5. **Load Balancing**: Use multiple app servers
6. **Async Tasks**: Set up Celery workers

## Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic --clear
```

### Database connection issues
- Check DATABASE_URL or DB_* variables
- Verify PostgreSQL is running
- Check firewall rules

### 502 Bad Gateway
- Check Gunicorn is running
- Verify socket file permissions
- Check Nginx configuration

## Security Hardening

1. **Use HTTPS only**
2. **Set secure cookie flags**
3. **Implement rate limiting**
4. **Regular security updates**
5. **Use environment variables for secrets**
6. **Enable CSRF protection**
7. **Configure CORS properly**
8. **Use strong passwords**
9. **Regular backups**
10. **Monitor logs**

---

For more help, refer to Django deployment documentation: https://docs.djangoproject.com/en/stable/howto/deployment/

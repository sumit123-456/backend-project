# Django HRMS Deployment Guide

This document provides comprehensive deployment instructions for the Django HRMS application across different platforms and environments.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Environment Setup](#environment-setup)
3. [Docker Deployment](#docker-deployment)
4. [Heroku Deployment](#heroku-deployment)
5. [Traditional Server Deployment](#traditional-server-deployment)
6. [Cloud Platform Deployments](#cloud-platform-deployments)
7. [Security Configuration](#security-configuration)
8. [Monitoring and Logging](#monitoring-and-logging)
9. [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites

- Python 3.11+
- MySQL 8.0+
- Redis (for caching)
- Nginx (for production)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Backend-Project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Setup database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Environment Setup

### Environment Variables Configuration

Copy `.env.example` to `.env` and configure the following variables:

```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-super-secret-key-change-this-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database Configuration
DB_NAME=hrmodel
DB_USER=hrms_user
DB_PASSWORD=secure_password
DB_HOST=127.0.0.1
DB_PORT=3306

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Database Setup

#### MySQL Setup

1. **Install MySQL**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install mysql-server
   
   # CentOS/RHEL
   sudo yum install mysql-server
   
   # macOS with Homebrew
   brew install mysql
   ```

2. **Create database and user**
   ```sql
   CREATE DATABASE hrmodel CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'hrms_user'@'localhost' IDENTIFIED BY 'secure_password';
   GRANT ALL PRIVILEGES ON hrmodel.* TO 'hrms_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

## Docker Deployment

### Using Docker Compose (Recommended)

1. **Build and start services**
   ```bash
   docker-compose up -d --build
   ```

2. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. **Collect static files**
   ```bash
   docker-compose exec web python manage.py collectstatic --noinput
   ```

5. **Access the application**
   - Web: http://localhost
   - Admin: http://localhost/admin

### Using Docker Only

1. **Build the image**
   ```bash
   docker build -t django-hrms .
   ```

2. **Run with MySQL container**
   ```bash
   docker run -d \
     --name mysql-db \
     -e MYSQL_DATABASE=hrmodel \
     -e MYSQL_ROOT_PASSWORD=rootpassword \
     mysql:8.0
   
   docker run -d \
     --name hrms-app \
     --link mysql-db:mysql \
     -p 8000:8000 \
     -e DB_PASSWORD=rootpassword \
     django-hrms
   ```

## Heroku Deployment

### Prerequisites

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Ubuntu/Debian
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

### Deployment Steps

1. **Create Heroku app**
   ```bash
   heroku create your-hrms-app-name
   ```

2. **Add PostgreSQL addon (optional, or use external MySQL)**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

3. **Configure environment variables**
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   heroku config:set EMAIL_HOST_USER=your-email@domain.com
   heroku config:set EMAIL_HOST_PASSWORD=your-app-password
   ```

4. **Add MySQL addon (ClearDB)**
   ```bash
   heroku addons:create cleardb:ignite
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Run migrations**
   ```bash
   heroku run python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   heroku run python manage.py createsuperuser
   ```

8. **Collect static files**
   ```bash
   heroku run python manage.py collectstatic --noinput
   ```

## Traditional Server Deployment

### Ubuntu/Debian Server

1. **Update system**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install dependencies**
   ```bash
   sudo apt install python3 python3-pip python3-venv mysql-server nginx redis-server git -y
   ```

3. **Setup application directory**
   ```bash
   sudo mkdir -p /var/www/hrms
   sudo chown $USER:$USER /var/www/hrms
   cd /var/www/hrms
   ```

4. **Clone and setup application**
   ```bash
   git clone <repository-url> .
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with production settings
   ```

6. **Setup database**
   ```bash
   sudo mysql_secure_installation
   # Create database and user as shown above
   ```

7. **Run migrations**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

8. **Configure Gunicorn**
   ```bash
   # Create systemd service
   sudo nano /etc/systemd/system/gunicorn.service
   ```

   ```ini
   [Unit]
   Description=gunicorn daemon for Django HRMS
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/hrms
   Environment="PATH=/var/www/hrms/venv/bin"
   ExecStart=/var/www/hrms/venv/bin/gunicorn \
           --config gunicorn.py \
           hrms.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

9. **Configure Nginx**
   ```bash
   sudo cp nginx/nginx.conf /etc/nginx/nginx.conf
   sudo cp nginx/default.conf /etc/nginx/sites-available/hrms
   sudo ln -s /etc/nginx/sites-available/hrms /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

10. **Start services**
    ```bash
    sudo systemctl start gunicorn
    sudo systemctl enable gunicorn
    sudo systemctl start nginx
    sudo systemctl enable nginx
    ```

## Cloud Platform Deployments

### AWS (Amazon Web Services)

#### Using AWS Elastic Beanstalk

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB application**
   ```bash
   eb init
   ```

3. **Create environment**
   ```bash
   eb create production
   ```

4. **Deploy**
   ```bash
   eb deploy
   ```

#### Using AWS EC2

1. **Launch EC2 instance (Ubuntu 22.04)**
2. **Follow Traditional Server Deployment steps**
3. **Configure RDS for MySQL**
4. **Configure ElastiCache for Redis**
5. **Configure Application Load Balancer**
6. **Setup SSL with AWS Certificate Manager**

### Google Cloud Platform (GCP)

#### Using Google App Engine

1. **Create app.yaml**
   ```yaml
   runtime: python39
   
   env_variables:
     SECRET_KEY: "your-secret-key"
     DEBUG: "False"
     ALLOWED_HOSTS: "your-domain.com"
   
   handlers:
   - url: /static
     static_dir: staticfiles/
   
   - url: /.*
     script: auto
   ```

2. **Deploy**
   ```bash
   gcloud app deploy
   ```

### Microsoft Azure

#### Using Azure App Service

1. **Create App Service**
2. **Configure deployment from Git**
3. **Setup MySQL Flexible Server**
4. **Configure environment variables**
5. **Deploy via Git/Azure DevOps**

## Security Configuration

### SSL/HTTPS Setup

1. **Obtain SSL certificate (Let's Encrypt)**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

2. **Configure Django settings for HTTPS**
   ```python
   # settings/production.py
   SECURE_SSL_REDIRECT = True
   SECURE_HSTS_SECONDS = 31536000
   SECURE_HSTS_INCLUDE_SUBDOMAINS = True
   SECURE_HSTS_PRELOAD = True
   SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
   ```

### Firewall Configuration

```bash
# Ubuntu/Debian UFW
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable

# CentOS/RHEL Firewalld
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### Database Security

1. **MySQL secure installation**
2. **Database user with minimal privileges**
3. **Regular backups**
4. **Connection encryption**

## Monitoring and Logging

### Application Monitoring

1. **Django Debug Toolbar (Development only)**
   ```bash
   pip install django-debug-toolbar
   ```

2. **Sentry for error tracking**
   ```bash
   pip install sentry-sdk[django]
   ```

   ```python
   # settings/production.py
   import sentry_sdk
   from sentry_sdk.integrations.django import DjangoIntegration
   
   sentry_sdk.init(
       dsn="YOUR_SENTRY_DSN",
       integrations=[DjangoIntegration()],
       traces_sample_rate=1.0,
       send_default_pii=True
   )
   ```

### Log Configuration

```python
# settings/production.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/hrms.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Health Checks

```python
# hrms/health_check.py
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'version': '1.0.0'
    })
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check database credentials
   - Verify database service is running
   - Check firewall rules
   - Verify MySQL user privileges

2. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check nginx configuration
   - Verify STATIC_ROOT path
   - Check file permissions

3. **Email Not Sending**
   - Verify SMTP credentials
   - Check email service configuration
   - Test with console email backend
   - Verify firewall rules

4. **Memory Issues**
   - Increase server memory
   - Optimize database queries
   - Implement caching
   - Configure worker processes

### Performance Optimization

1. **Database Optimization**
   ```sql
   CREATE INDEX idx_employee_name ON app_employee(name);
   ANALYZE TABLE app_employee;
   ```

2. **Caching Configuration**
   ```python
   # settings/production.py
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.redis.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
       }
   }
   ```

3. **Static Files CDN**
   - Use AWS CloudFront
   - Configure nginx caching
   - Enable gzip compression

### Backup and Recovery

1. **Database Backup Script**
   ```bash
   #!/bin/bash
   DATE=$(date +%Y%m%d_%H%M%S)
   mysqldump -u root -p hrmodel > backup_$DATE.sql
   ```

2. **Application Backup**
   ```bash
   tar -czf hrms_backup_$(date +%Y%m%d).tar.gz /var/www/hrms/
   ```

3. **Automated Backups**
   - Setup cron jobs
   - Use cloud backup services
   - Test restore procedures

### Support and Maintenance

- Regular security updates
- Monitor application logs
- Performance monitoring
- Database maintenance
- SSL certificate renewal
- Backup verification

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)

---

**Note**: Always test deployments in a staging environment before deploying to production. Ensure you have proper monitoring and rollback procedures in place.
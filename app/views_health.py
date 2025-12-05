"""
Health check views for deployment monitoring
"""

from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.conf import settings
import time

# Optional redis import
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


def health_check(request):
    """
    Basic health check endpoint
    """
    try:
        # Check Django application is running
        response_data = {
            'status': 'healthy',
            'application': 'Django HRMS',
            'version': '1.0.0',
            'timestamp': int(time.time()),
            'debug': settings.DEBUG
        }
        
        return JsonResponse(response_data, status=200)
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)


def detailed_health_check(request):
    """
    Detailed health check with database and cache connectivity
    """
    health_data = {
        'status': 'healthy',
        'application': 'Django HRMS',
        'version': '1.0.0',
        'timestamp': int(time.time()),
        'checks': {}
    }
    
    issues = []
    
    # Database connectivity check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_data['checks']['database'] = {
                'status': 'healthy',
                'engine': settings.DATABASES['default']['ENGINE']
            }
    except Exception as e:
        issues.append(f"Database connection failed: {str(e)}")
        health_data['checks']['database'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
    
    # Cache connectivity check (Redis/Django Cache)
    try:
        if hasattr(settings, 'CACHES') and 'default' in settings.CACHES:
            cache.set('health_check', 'ok', 10)
            cache_result = cache.get('health_check')
            if cache_result == 'ok':
                health_data['checks']['cache'] = {
                    'status': 'healthy',
                    'type': settings.CACHES['default']['BACKEND'],
                    'redis_available': REDIS_AVAILABLE
                }
            else:
                issues.append("Cache write/read test failed")
                health_data['checks']['cache'] = {
                    'status': 'unhealthy',
                    'error': 'Cache write/read test failed',
                    'redis_available': REDIS_AVAILABLE
                }
        else:
            health_data['checks']['cache'] = {
                'status': 'not_configured',
                'redis_available': REDIS_AVAILABLE
            }
    except Exception as e:
        issues.append(f"Cache connection failed: {str(e)}")
        health_data['checks']['cache'] = {
            'status': 'unhealthy',
            'error': str(e),
            'redis_available': REDIS_AVAILABLE
        }
    
    # Email configuration check
    try:
        email_backend = settings.EMAIL_BACKEND
        health_data['checks']['email'] = {
            'status': 'configured',
            'backend': email_backend,
            'host': getattr(settings, 'EMAIL_HOST', 'not_configured')
        }
    except Exception as e:
        health_data['checks']['email'] = {
            'status': 'error',
            'error': str(e)
        }
        issues.append(f"Email configuration error: {str(e)}")
    
    # Static files check
    try:
        static_url = settings.STATIC_URL
        media_url = settings.MEDIA_URL
        health_data['checks']['static_files'] = {
            'status': 'configured',
            'static_url': static_url,
            'media_url': media_url
        }
    except Exception as e:
        health_data['checks']['static_files'] = {
            'status': 'error',
            'error': str(e)
        }
    
    # Security settings check
    try:
        security_checks = {
            'debug_mode': settings.DEBUG,
            'secret_key_set': bool(getattr(settings, 'SECRET_KEY', None)),
            'allowed_hosts': getattr(settings, 'ALLOWED_HOSTS', [])
        }
        health_data['checks']['security'] = security_checks
        
        # Flag if debug is enabled in production
        if not settings.DEBUG and health_data['checks']['security']['secret_key_set']:
            health_data['status'] = 'healthy'
        else:
            issues.append("Security configuration issues detected")
            health_data['status'] = 'warning'
            
    except Exception as e:
        health_data['checks']['security'] = {
            'status': 'error',
            'error': str(e)
        }
    
    # Set overall status
    if issues:
        health_data['status'] = 'degraded' if len(issues) <= 2 else 'unhealthy'
        health_data['issues'] = issues
        health_data['timestamp'] = int(time.time())
        
        return JsonResponse(health_data, status=503)
    else:
        return JsonResponse(health_data, status=200)


def readiness_check(request):
    """
    Readiness check for Kubernetes/container orchestrators
    """
    try:
        # Check if database is reachable
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Check if cache is working (if configured)
        if hasattr(settings, 'CACHES') and 'default' in settings.CACHES:
            cache.set('readiness_check', 'ok', 30)
            if cache.get('readiness_check') != 'ok':
                return JsonResponse({
                    'status': 'not_ready',
                    'reason': 'Cache connectivity failed'
                }, status=503)
        
        return JsonResponse({
            'status': 'ready',
            'timestamp': int(time.time())
        }, status=200)
        
    except Exception as e:
        return JsonResponse({
            'status': 'not_ready',
            'reason': str(e)
        }, status=503)


def liveness_check(request):
    """
    Liveness check for Kubernetes/container orchestrators
    """
    try:
        # Simple check that the Django application is responsive
        return JsonResponse({
            'status': 'alive',
            'timestamp': int(time.time())
        }, status=200)
    except Exception as e:
        return JsonResponse({
            'status': 'dead',
            'reason': str(e)
        }, status=503)
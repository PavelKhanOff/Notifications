import os

# POSTGRES_CONFIG
DB_ENGINE = os.environ.get('DB_ENGINE', 'postgresql+asyncpg')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'admin')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'LOYAg3Wv')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'db_notifications')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'eduonepostgresdbnotifications')
SQLALCHEMY_DATABASE_URL = (
    f"{DB_ENGINE}://{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:"
    f"{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)

# JWT CONFIG
SECRET = os.environ.get('JWTSECRET', 'SOMESECRET')


# Celery Settings
REDIS_HOST = os.environ.get("REDIS_HOST", 'redis')
REDIS_PORT = os.environ.get("REDIS_PORT", '6379')
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", 'secrett')

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_BACKEND_URL = (
        "sentinel://sentinel-0.sentinel.default.svc.cluster.local:5000/0;"
        "sentinel://sentinel-1.sentinel.default.svc.cluster.local:5000/0;"
        "sentinel://sentinel-2.sentinel.default.svc.cluster.local:5000/0"
    )


# Middleware
MIDDLEWARE_HOST = os.environ.get("MIDDLEWARE_HOST", "middleware-service")
MIDDLEWARE_PORT = os.environ.get("MIDDLEWARE_PORT", 6000)
CORE_HOST = os.environ.get("CORE_HOST", "core-service")
CORE_PORT = os.environ.get("CORE_PORT", 8000)
PROTOCOL = 'http'
URL_CHECK_SUPER_USER = os.environ.get(
    "URL_CHECK_SUPER_USER", 'middleware/check_superuser'
)
URL_CHECK_USER = os.environ.get("URL_CHECK_SUPER_USER", 'middleware/check_user')
MIDDLEWARE_URL_CHECK_SUPER_USER = (
    f'{PROTOCOL}://{MIDDLEWARE_HOST}:{MIDDLEWARE_PORT}/{URL_CHECK_SUPER_USER}'
)
MIDDLEWARE_URL_CHECK_USER = (
    f'{PROTOCOL}://{MIDDLEWARE_HOST}:{MIDDLEWARE_PORT}/{URL_CHECK_USER}'
)

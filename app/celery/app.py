from celery import Celery
import celery_pool_asyncio
from app.config import CELERY_BROKER_URL, CELERY_BACKEND_URL
celery_pool_asyncio.__package__


celery_app = Celery(
    "tasks",
    # broker="amqp://guest:guest@rabbitmq-1.rabbitmq.default.svc.cluster.local:5672/",
    # backend=CELERY_BACKEND_URL,
    # backend="redis://notifications-redis:6379/0",
    # broker="amqp://admin:mypass@notifications-rabbitmq:5672//",
    backend=CELERY_BACKEND_URL,
    broker=CELERY_BROKER_URL
)


celery_app.autodiscover_tasks(['app.sender'])

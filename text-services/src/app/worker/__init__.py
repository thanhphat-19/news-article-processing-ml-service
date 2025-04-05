import urllib.parse

import celery
from celery import Celery
from src.configs.app import app_settings
from redis import Redis

# Celery
app = Celery("tasks", broker=app_settings.MQ_URL, backend=app_settings.REDIS_URL)


@celery.signals.celeryd_init.connect
def setup_log_format(sender, conf, **kwargs):
    conf.worker_log_format = """
        [%(asctime)s: %(levelname)s/%(processName)s {0}] %(message)s
    """.strip().format(
        sender
    )
    conf.worker_task_log_format = (
        "[%(asctime)s: %(levelname)s/%(processName)s {0}] "
        "[%(task_name)s(%(task_id)s)] %(message)s"
    ).format(sender)


# Redis
parsed_redis = urllib.parse.urlparse(app_settings.REDIS_URL)
redis = Redis(
    host=parsed_redis.hostname,
    port=parsed_redis.port,
    password=parsed_redis.password,
    db=parsed_redis.path.lstrip("/"),
)

from src.app.worker import task

from celery import Celery

celery = Celery(
    "app.tasks",
    broker="redis://redis.default.svc:6379/0"
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_ignore_result=True,
    task_ask_late=True,
    task_reject_on_worker_lost=True,
    broker_transport_options={
        "visibility_timeout": 3600,  # 1 hour
    },
)
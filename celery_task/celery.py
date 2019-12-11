from __future__ import absolute_import
import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "luffyapi.settings.dev")
django.setup()


from celery import Celery

broker = 'redis://127.0.0.1:6379/5'
backend = 'redis://127.0.0.1:6379/5'
app = Celery(broker=broker, backend=backend, include=['celery_task.tasks'])


# 时区
app.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
app.conf.enable_utc = False

# 自动任务的定时配置
from celery.schedules import crontab
from datetime import timedelta
app.conf.beat_schedule = {
    # 定时任务：任务名自定义
    'update_banner_cache': {
        'task': 'celery_task.tasks.update_banner_cache',  # 任务源
        'args': (),  # 任务参数
        'schedule': timedelta(seconds=5), # 定时添加任务的时间
        # 'schedule': crontab(hour=8, day_of_week=1),  # 每周一早八点
    }
}








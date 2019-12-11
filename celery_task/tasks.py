from .celery import app
# from home.models import Banner
# from django.core.cache import cache
# from home.serializers import BannerModelSerializer
@app.task
def update_banner_cache():
    res = 10+10
    print(res)
    return res



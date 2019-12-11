import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "luffyapi.settings.dev")
django.setup()
from order.views import SuccessAPIView

# from django.core.cache import cache
# from redis import Redis
#
# redis = Redis(db=1)
# redis.setex('name',30,'jack')
print(SuccessAPIView.mro())
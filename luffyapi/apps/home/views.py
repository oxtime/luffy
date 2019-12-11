from . import models
from . import serializers
from rest_framework.generics import ListAPIView

class BannerListAPIView(ListAPIView):
    queryset = models.Banner.objects.filter(is_delete=False,is_show=True).order_by('-orders')
    serializer_class = serializers.BannerModelSerializer
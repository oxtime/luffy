from django.urls import path, re_path

from rest_framework.views import APIView
from rest_framework.response import Response
from . import views


urlpatterns = [
    path('banners/',views.BannerListAPIView.as_view()),
    # re_path('^', )
]
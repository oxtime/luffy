from django.urls import path, re_path

from rest_framework.views import APIView
from rest_framework.response import Response
from . import views


urlpatterns = [
    path('free',views.FreeCourseListAPIView.as_view()),
    path('categories',views.CategoriesListAPIView.as_view()),
    path('chapters', views.ChapterListAPIView.as_view()),
    re_path('^free/(?P<pk>\d+)$',views.FreeCourseRetrieveAPIView.as_view()),
    # re_path('^', )
]
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from . import models,serializers
from rest_framework.filters import OrderingFilter,SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CourseFilterSet,LimitFilter
from .pagination import CoursePageNumberPagination
from rest_framework.generics import RetrieveAPIView

class FreeCourseListAPIView(ListAPIView):
    queryset = models.Course.objects.filter(is_delete=False,is_show=True).order_by('-orders').all()
    serializer_class = serializers.FreeCourseListSerializers

    # 配置过滤器类
    # filter_backends = [OrderingFilter, LimitFilter]  # LimitFilter自定义过滤器
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend,LimitFilter]
    # 参与排序的字段: ordering=-price,id
    ordering_fields = ['price', 'id', 'students']
    # 参与搜索的字段: search=python  (name字段中带python就ok)
    search_fields = ['name', 'brief']
    # 参与分类筛选的字段：所有字段都可以，但是用于分组的字段更有意义
    # filter_fields = ['course_category']

    filter_class = CourseFilterSet


    pagination_class = CoursePageNumberPagination




class CategoriesListAPIView(ListAPIView):
    queryset = models.CourseCategory.objects.filter(is_show=True,is_delete=False).all()
    serializer_class = serializers.CategoriesSerializers


class FreeCourseRetrieveAPIView(RetrieveAPIView):
    queryset = models.Course.objects.filter(is_show=True, is_delete=False).order_by('-orders').all()
    serializer_class = serializers.FreeCourseListSerializers

class ChapterListAPIView(ListAPIView):
    queryset = models.CourseChapter.objects.filter(is_show=True, is_delete=False).all()
    serializer_class = serializers.ChapterListSerializers

    filter_backends = [DjangoFilterBackend]
    filter_fields = ['course']
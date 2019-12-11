from rest_framework.pagination import PageNumberPagination



class CoursePageNumberPagination(PageNumberPagination):
    # 默认一页条数
    page_size = 3
    # 选择哪一页的key
    page_query_param = 'page'
    # 用户自定义一页条数
    page_size_query_param = 'page_size'
    # 用户自定义一页最大控制条数
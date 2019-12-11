from django.urls import path, re_path


from . import views

urlpatterns = [
    path('pay', views.PayPIViewAPIView.as_view()),
    path('success', views.SuccessAPIView.as_view()),
]
from django.urls import path, re_path


from . import views

urlpatterns = [
    path('login', views.LoginAPIView.as_view()),
    path('login/mobile', views.LoginMobileAPIView.as_view()),
    path('register', views.RegisterAPIView.as_view()),
    path('sms', views.SmsAPIView.as_view()),
    path('mobile', views.MobilePIView.as_view()),
]
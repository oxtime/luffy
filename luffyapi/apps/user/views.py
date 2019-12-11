import re
from . import serializers
from . import models
from utils.response import APIResponse
from rest_framework.views import APIView
from libs.tx_sms import sms,settings
from django.core.cache import cache
from . import throttles
from rest_framework.response import Response
from django.contrib.auth import get_user_model  # 要加上这句话不然会报错（1） 2.0版本导入
User = get_user_model()
# from django.contrib.auth.models import User 1.0版本导入
#多方式登录
class LoginAPIView(APIView):
    def post(self,request,*args,**kwargs):
        serializer = serializers.LoginSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data={
            'username':serializer.user.username,
            'token':serializer.token,
            'status':0
        },status=200)

#手机号登录
class LoginMobileAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.MobileSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = cache.get(serializer.mobile)
        if not code:
            return APIResponse(1,'验证码已失效请重试')
        if serializer.code == code:
            request.user = serializer.user
        return Response(data={
            'username': serializer.user.username,
            'token': serializer.token,
            'status':0
        },status=200)



#手机验证码注册接口
from rest_framework.generics import GenericAPIView
class RegisterAPIView(APIView):
    def post(self,request,*args,**kwargs):
        # cache.set('13355556666','778899',300)
        serializer = serializers.RegisterSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.attrs)
        if serializer.attrs.get('code') != cache.get(serializer.attrs.get('mobile')):
            return APIResponse(1,'验证码错误')
        serializer.attrs.pop('code')
        User.objects.create_user(**serializer.attrs)
        return APIResponse(0,'注册成功')


#发送短信
class SmsAPIView(APIView):
    throttle_classes = [throttles.SMSRateThrottle]
    def post(self,request,*args,**kwargs):
        serializer = serializers.SmsSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = sms.get_code()
        print(serializer.mobile)
        flag = sms.send_sms(serializer.mobile,code)
        if not flag:
            return APIResponse('1','信息发送失败')
        cache.set(f'{serializer.mobile}',code,settings.EXC_TIME*60)
        return APIResponse(0,'发送验证码成功')




#手机号验证接口
class MobilePIView(APIView):
    def post(self,request,*args,**kwargs):
        mobile = request.data.get('mobile')
        if not (mobile and re.match(r'^1[3-9][0-9]{9}$', mobile)):
            return APIResponse(2,'手机号不正确')
        try:
            models.User.objects.get(mobile=mobile)
            return APIResponse(1,'手机号已注册')
        except:
            return APIResponse(0,'可以注册')

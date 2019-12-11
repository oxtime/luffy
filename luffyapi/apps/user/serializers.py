from rest_framework import serializers
from . import models
import re
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler


class LoginSerializers(serializers.ModelSerializer):
    username = serializers.CharField(max_length=16)
    password = serializers.CharField(max_length=16)

    class Meta:
        model = models.User
        fields = ['username','password']


    def validate(self, attrs):
        user_obj = self._many_login(**attrs)
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        self.user = user_obj
        self.token = token
        return attrs

    def _many_login(self,**kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        if re.match(r'.*@.*',username):
            user_obj = models.User.objects.filter(email=username).first()
        elif  re.match(r'^1[3-9][0-9]{9}$', username):
            user_obj = models.User.objects.filter(mobile=username).first()
        else:
            user_obj = models.User.objects.filter(username=username).first()
        if not user_obj:
            raise serializers.ValidationError({'username': '没有此账号'})
        is_right = user_obj.check_password(password)
        if is_right:
            user_obj.user = user_obj
            return user_obj
        else:
            raise serializers.ValidationError({'password': '密码有误'})



class SmsSerializers(serializers.ModelSerializer):

    mobile = serializers.CharField(max_length=11,write_only=True)
    class Meta:
        model = models.User
        fields = ('mobile',)

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        if not (mobile and re.match(r'^1[3-9][0-9]{9}$', mobile)):
            raise serializers.ValidationError({'mobile':'手机号有误'})
        self.mobile = mobile
        return attrs


class MobileSerializers(serializers.ModelSerializer):

    mobile = serializers.CharField(max_length=11,write_only=True)
    code = serializers.CharField(max_length=16,write_only=True)
    class Meta:
        model = models.User
        fields = ('mobile','code')

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        code = attrs.get('code')
        if not (mobile and re.match(r'^1[3-9][0-9]{9}$', mobile)):
            raise serializers.ValidationError({'mobile':'手机号有误'})
        try:
            user = models.User.objects.get(mobile=mobile)
        except:
            raise serializers.ValidationError({'mobile': '手机号未注册'})
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        self.code = code
        self.user = user
        self.token = token
        self.mobile = mobile
        return attrs


class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(max_length=11,write_only=True)
    mobile = serializers.CharField(max_length=16,write_only=True)
    code = serializers.CharField(max_length=8,write_only=True)
    class Meta:
        model = models.User
        fields = ['password','mobile','code']


    def validate_mobile(self,mobile):
        if not (mobile and re.match(r'^1[3-9][0-9]{9}$', mobile)):
            raise serializers.ValidationError({'mobile':'手机号有误'})
        user = models.User.objects.filter(mobile=mobile)
        if user:
            raise serializers.ValidationError({'mobile': '手机号已注册'})
        return mobile

    def validate(self, attrs):
        password = attrs.get('password')
        mobile = attrs.get('mobile')
        if len(password) < 6:
            raise serializers.ValidationError({'password': '密码不少于6位'})
        attrs['username'] = str(mobile)
        self.attrs = attrs
        return attrs



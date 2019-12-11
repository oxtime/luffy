from course.models import Course
from rest_framework import serializers
from . import models
import time
from libs.iPay import settings
from libs.iPay import alipay,alipay_gateway

class PaySerializers(serializers.ModelSerializer):
    goods_pks = serializers.CharField(max_length=20)
    class Meta:
        model = models.Order
        fields = [
            'subject',
            'total_amount',
            'pay_type',
            'goods_pks',
        ]

        extra_kwargs = {
            'total_amount': {
                'required': True
            }
        }

    def validate(self, attrs):
        goods_pks = attrs.pop('goods_pks')
        total_amount = attrs.get('total_amount')
        goods_lt_pks = goods_pks.split(',')
        try:
            goods_obj = [Course.objects.get(pk=pk) for pk in goods_lt_pks]
        except:
            raise serializers.ValidationError({'pk':'课程主键有误'})

        count_price = 0
        for goods in goods_obj:
            count_price+=goods.price

        if count_price!=total_amount:
            raise serializers.ValidationError({'total_amount': '价格异常'})

        order_on=self._get_order_no()
        subject = attrs.get('subject')
        order_params = alipay.api_alipay_trade_page_pay(out_trade_no=order_on,
                                                        total_amount=float(total_amount),
                                                        subject=subject,
                                                        return_url=settings.RETURN_URL,  # 同步回调的前台接口
                                                        notify_url=settings.NOTIFY_URL  # 异步回调的后台接口
                                                        )

        pay_url = alipay_gateway+order_params

        self.pay_url = pay_url

        attrs['out_trade_no'] = order_on
        request = self.context.get('request')
        attrs['user'] = request.user
        attrs['courses'] = goods_obj
        return attrs


    def create(self, validated_data):
        courses = validated_data.pop('courses')

        order = super().create(validated_data)

        # 关系表操作
        order_detail_list = []
        for course in courses:
            order_detail_list.append(models.OrderDetail(order=order, course=course, price=course.price, real_price=course.price))

        # 将多个订单详情对象，批量入库
        models.OrderDetail.objects.bulk_create(order_detail_list)

        return order


    def _get_order_no(self):
        no = '%s' % time.time()
        return no.replace('.', '', 1)


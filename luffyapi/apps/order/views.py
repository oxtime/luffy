from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import serializers
from utils.logging import logger
from libs.iPay import alipay
from . import models


class PayPIViewAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        ser_obj = serializers.PaySerializers(data=request.data,context={'request':request})
        ser_obj.is_valid(raise_exception=True)
        ser_obj.save()
        return Response(ser_obj.pay_url)



class SuccessAPIView(APIView):
    def patch(self, request, *args, **kwargs):
        # print(request.query_params)
        data = request.query_params.dict()
        sign = data.pop('sign')
        result = alipay.verify(data, sign)
        if result:
            # 一般不在同步回调直接操作订单状态
            pass
            # models.Order.objects.filter(out_trade_no=data.get('out_trade_no')).update(order_status=1)
        return Response('同步回调完成')

        # 异步支付宝回调接口：公网下才能验证

    def post(self, request, *args, **kwargs):
        data = request.data.dict()  # 回调参数，是QueryDict类型，不能直接调用pop方法
        sign = data.pop('sign')  # 签名
        out_trade_no = data.get('out_trade_no')  # 订单号
        result = alipay.verify(data, sign)
        if result and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            try:
                order = models.Order.objects.get(out_trade_no=out_trade_no)
                if order.order_status != 1:
                    order.order_status = 1
                    order.save()
                    logger.warning('%s订单完成支付' % out_trade_no)
                return Response('success')
            except:
                pass
        return Response('failed')


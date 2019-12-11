import random
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from .settings import *
sender = SmsSingleSender(APP_ID, APP_KEY)
from utils.logging import logger

def get_code():
    code = ''
    for i in range(6):
        num = random.randint(0,9)
        code+= str(num)
    return code

def send_sms(mobile,code):
    try:
        response = sender.send_with_param(86, mobile,
                                        TEMPLATE_ID, params=(code,EXC_TIME), sign=SMS_SIGN, extend="", ext="")
        if response.get('result') == 0:
            return True
    except Exception as e:
        logger.error(f'信息发送失败:{e}')
        return False
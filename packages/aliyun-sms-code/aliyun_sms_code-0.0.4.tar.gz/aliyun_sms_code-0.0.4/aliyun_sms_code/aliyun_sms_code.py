import os
import json
from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient

# 必填，您的 AccessKey ID, 填写在环境变量中
ALIBABA_CLOUD_ACCESS_KEY_ID = os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID']
# 必填，您的 AccessKey Secret, 填写在环境变量中
ALIBABA_CLOUD_ACCESS_KEY_SECRET = os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
# 短信签名名称，在阿里云申请并审核通过
SIGN_NAME = os.environ['SIGN_NAME']
# 短信模板CODE，在阿里云申请并审核通过
TEMPLATE_CODE = os.environ['TEMPLATE_CODE']
# Endpoint 请参考 https://api.aliyun.com/product/Dysmsapi
ENDPOINT = f'dysmsapi.aliyuncs.com'


class AliyunSMS:
    access_key_id = ALIBABA_CLOUD_ACCESS_KEY_ID
    access_key_secret = ALIBABA_CLOUD_ACCESS_KEY_SECRET
    sign_name = SIGN_NAME
    template_code = TEMPLATE_CODE
    endpoint = ENDPOINT

    def __init__(self,  mobile: str, sms_code: str):
        # 接收短信的手机号码
        self.mobile = mobile
        # 短信模板变量对应的实际值
        self.template_param = json.dumps({"code": sms_code})

    def __create_client(self) -> OpenApiClient:
        config = open_api_models.Config(
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret
        )
        config.endpoint = ENDPOINT
        return OpenApiClient(config)

    def __create_api_info(self) -> open_api_models.Params:
        params = open_api_models.Params(
            # 接口名称,
            action='SendSms',
            # 接口版本,
            version='2017-05-25',
            # 接口协议,
            protocol='HTTPS',
            # 接口 HTTP 方法,
            method='POST',
            auth_type='AK',
            style='RPC',
            # 接口 PATH,
            pathname=f'/',
            # 接口请求体内容格式,
            req_body_type='json',
            # 接口响应体内容格式,
            body_type='json'
        )
        return params

    def send_sms(self):
        client = self.__create_client()
        params = self.__create_api_info()
        queries = {'PhoneNumbers': self.mobile, 'SignName': self.sign_name,
                   'TemplateCode': self.template_code,
                   'TemplateParam': self.template_param}
        # 设置运行时间
        runtime = util_models.RuntimeOptions()
        request = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(queries)
        )
        resp = client.call_api(params, request, runtime)
        return resp



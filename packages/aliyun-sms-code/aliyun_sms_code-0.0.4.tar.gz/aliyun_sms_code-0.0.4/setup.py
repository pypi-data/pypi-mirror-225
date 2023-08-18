import os
import setuptools

if os.path.exists('./README.md'):
    with open("README.md", encoding='utf-8') as fp:
        long_description = fp.read()

setuptools.setup(
    name="aliyun_sms_code",
    version="0.0.4",
    author="chentianbo",
    author_email="chentianbo@xmov.ai",
    description="Sending verification codes through Aliyun SMS service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "alibabacloud_tea_openapi>=0.3.6, <1.0.0",
        "alibabacloud_tea_console>=0.0.1, <1.0.0",
        "alibabacloud_openapi_util>=0.2.1, <1.0.0",
        "alibabacloud_tea_util>=0.3.8, <1.0.0"
    ]
)

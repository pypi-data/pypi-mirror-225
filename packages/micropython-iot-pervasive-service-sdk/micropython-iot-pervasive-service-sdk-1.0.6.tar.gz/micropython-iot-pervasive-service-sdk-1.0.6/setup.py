from setuptools import setup, find_packages
setup(
    name='micropython-iot-pervasive-service-sdk',
    version="1.0.6",
    description="iot-pervasive-service-sdk module customized for micropython.",
    packages=find_packages(),
    author="whu",    #作者，可以写自己的姓名
    author_email="2898534520@qq.com",    #作者联系方式，可写自己的邮箱地址
    classifiers=[
        'Development Status :: 5 - Production/Stable',
    ],
    keywords='micropython',
    include_package_data=True
    )

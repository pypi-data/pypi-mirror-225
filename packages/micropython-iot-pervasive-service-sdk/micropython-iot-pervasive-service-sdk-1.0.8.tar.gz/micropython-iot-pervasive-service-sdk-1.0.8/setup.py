import setuptools #导入setuptools打包工具
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="micropython-iot-pervasive-service-sdk", 
    version="1.0.8",    #包版本号，便于维护版本
    author="whu",    #作者，可以写自己的姓名
    author_email="2898534520@qq.com",    #作者联系方式，可写自己的邮箱地址
    description="设备端直连框架python",#包的简述
    install_requires=[  #对应依赖信息
        "micropython-umqtt.simple",
        "micropython-ulogger",
        "micropython-urequests"
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
    ],
    keywords='micropython',
)
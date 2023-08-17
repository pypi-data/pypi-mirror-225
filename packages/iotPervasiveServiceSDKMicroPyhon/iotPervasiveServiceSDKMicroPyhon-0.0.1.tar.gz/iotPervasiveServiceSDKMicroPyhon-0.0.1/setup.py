import setuptools #导入setuptools打包工具
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="iotPervasiveServiceSDKMicroPyhon", 
    version="0.0.1",    #包版本号，便于维护版本
    author="whu贾向阳团队-葛家和",    #作者，可以写自己的姓名
    author_email="2898534520@qq.com",    #作者联系方式，可写自己的邮箱地址
    description="设备端直连框架python",#包的简述
    long_description=long_description,    #包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),  # Make sure to include 'where' argument
    zip_safe=False,  # Disable zip-safe mode for easier debugging
    include_package_data=True, 
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",  
    ],
    install_requires=[  #对应依赖信息
        "micropython-umqtt.simple",
        "micropython-ulogger",
        "micropython-urequests"
    ],
)
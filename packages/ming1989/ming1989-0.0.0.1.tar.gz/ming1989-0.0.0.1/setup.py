
from setuptools import setup, find_packages

setup(
    name='ming1989',  # 包名
    version='0.0.0.1',  # 版本
    description="",  # 包简介
    long_description=open('README.md').read(),  # 读取文件中介绍包的详细内容
    include_package_data=True,  # 是否允许上传资源文件
    author='',  # 作者
    author_email='',  # 作者邮件
    maintainer='',  # 维护者
    maintainer_email='',  # 维护者邮件
    license='MIT License',  # 协议
    url='',  # github或者自己的网站地址
    packages=find_packages(),  # 包的目录
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',  # 设置编写时的python版本
    ],
    python_requires='>=3.8',  # 设置python版本要求
    install_requires=[''],  # 安装所需要的库
    entry_points={
        'console_scripts': [
            'say_hello=say_hello.py:say.hello'
        ],
    },  # 设置命令行工具(可不使用就可以注释掉)

)

'''
安装必须的包
pip install --user --upgrade setuptools wheel
pip install twine

服务端：
1. 修改上面的版本号
2. 删除项目 build dist 两个文件夹
3. 打包命令
    python setup.py sdist build
4. 上传命令
    twine upload dist/*
5. 输入账号密码
    wgm1016
    wQ

客户端升级
pip install --upgrade ming1989

'''
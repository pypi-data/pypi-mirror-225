# @Project  :pythonwork
# @File     :setup
# @Date     :2023/8/16 11:06
# @Author   :ZZL
from distutils.core import setup

setup(
    name='Demo_test0816',  # 对外模块的名字
    version='1.0.1',  # 版本号
    description='测试本地发布模块',  # 描述
    author='zzl',  # 作者
    author_email='1778552868@qq.com',
    py_modules=['Demo_test0816.mul'],  # 要发布的模块
)
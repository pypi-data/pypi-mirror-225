from setuptools import setup,find_namespace_packages

setup(
name='nonebot_plugin_matcher_block',
version='0.0.6',
description='通用指令阻断',
#long_description=open('README.md','r').read(),
author='karisaya',
author_email='1048827424@qq.com',
license='MIT license',
include_package_data=True,
packages=find_namespace_packages(include=["nonebot_plugin_matcher_block"]),
platforms='all',
install_requires=["nonebot2","nonebot-adapter-onebot",],
url='https://github.com/KarisAya/nonebot_plugin_matcher_block',
)
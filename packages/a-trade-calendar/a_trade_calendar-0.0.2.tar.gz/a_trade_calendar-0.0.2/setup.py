"""
 
:Author:  逍遥游
:Create:  2023/8/17$ 08:52$
"""
from setuptools import setup, find_packages

setup(
    name='a_trade_calendar',
    version='0.0.2',
    author='xyy',
    author_email='chatxingqiu@gmail.com',
    description='一款纯粹的交易日历工具包，适用于A股',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
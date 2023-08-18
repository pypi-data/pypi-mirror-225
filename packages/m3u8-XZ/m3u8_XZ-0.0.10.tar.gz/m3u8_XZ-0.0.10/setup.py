# -- coding:utf-8 --
# Time:2023-03-23 14:44
# Author:XZ
# File:setup.py
# IED:PyCharm
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="m3u8_XZ",
    version="0.0.10",
    author="XZ",
    author_email="345841407@qq.com",
    description="download m3u8 video by m3u8 url or by local m3u8 file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests", "aiohttp", "pycryptodome"],
)

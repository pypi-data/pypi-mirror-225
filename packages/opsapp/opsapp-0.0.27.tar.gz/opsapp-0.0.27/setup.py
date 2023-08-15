from setuptools import setup, find_packages 
import codecs
import os
import re

def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts), "r",encoding='utf-8').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^VERSION = ['\"]([^'\"]*)['\"]", version_file, re.M
    )
    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find version string.")

setup(
    name='opsapp',
    version=find_version("opsapp","app","settings","config.py"),
    description="This is the ml opsapp",
    author='zhys513',#作者
    author_email="254851907@qq.com",
    url="https://gitee.com/zhys513/opsapp",
    packages=find_packages(exclude=['ops','pipe']), # 排除不生效？
    # 任何包如果包含 *.txt or *.rst 文件都加进去，可以处理多层package目录结构 
    package_data={'': ['*.js','*.css','*.map'],},
    install_requires=['requests'], # 未添加依赖
    python_requires='>=3.6', 
)


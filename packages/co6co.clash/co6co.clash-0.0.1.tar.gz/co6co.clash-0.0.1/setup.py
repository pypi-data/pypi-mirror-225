from setuptools import setup, find_packages

import co6co_clash
VERSION = co6co_clash.__version__

# read readmeFile contents
from os import path
currentDir = path.abspath(path.dirname(__file__))
with open(path.join(currentDir, 'README.md'), encoding='utf-8') as f: long_description = f.read()


setup(
    name="co6co.clash",
    version=VERSION,
    description="Clash 基础模块",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[ "Programming Language :: Python :: 3", "Programming Language :: Python :: 3.6" ],
    include_package_data=True, zip_safe=True,
    #依赖哪些模块
    install_requires=[ ],
    #package_dir= {'utils':'src/log','main_package':'main'},#告诉Distutils哪些目录下的文件被映射到哪个源码
    author='Clash',
    author_email ='Clash@qq.com',
    url="http://git.hub.com/Clash",
    data_file={
        ('',"*.txt"),
        ('',"*.md"),
    },
    package_data={
        '':['*.txt','*.md'],
        'bandwidth_reporter':['*.txt']
    }
)
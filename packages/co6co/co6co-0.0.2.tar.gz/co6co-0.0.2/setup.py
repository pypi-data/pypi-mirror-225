from setuptools import setup, find_packages

# read readmeFile contents
from os import path
currentDir = path.abspath(path.dirname(__file__))
with open(path.join(currentDir, 'README.md'), encoding='utf-8') as f: long_description = f.read()


VERSION = '0.0.2'
setup(
    name="co6co",
    version=VERSION,
    description="基础模块",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[ "Programming Language :: Python :: 3", "Programming Language :: Python :: 3.6" ],
    include_package_data=True, zip_safe=True,
    #依赖哪些模块
    install_requires=[ ],
    #package_dir= {'':'src'},#告诉Distutils哪些目录下的文件被映射到哪个源码
    author='co6co',
    author_email ='co6co@qq.com',
    url="http://git.hub.com/co6co",
    data_file={
        ('',"*.txt"),
        ('',"*.md"),
    },
    package_data={
        '':['*.txt','*.md'],
        'bandwidth_reporter':['*.txt']
    }
)
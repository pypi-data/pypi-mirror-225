import io
import os
import setuptools

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.md'), encoding='UTF-8') as f:
    long_description = '\n' + f.read()


setuptools.setup(
    name="nacos-python-sdk",
    version="0.2",
    description="nacos-python-sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://codeup.aliyun.com/612cb27957e7cd986dfaf21f/nacos-python-sdk",
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8"
    ],
    keywords=['nacos', 'nacos-python-sdk'],
    install_requires=[],
    license="Apache License 2.0",
    packages=setuptools.find_packages(),
)
import setuptools

setuptools.setup(
    name = "lemon-gtm",
    version = "1.0.0",
    author = "lemonorangeapple",
    description = "A Global Tracking Model for Python",
    long_description_content_type = "text/markdown",
    url = "https://github.com/lemonorangeapple/lemon-gtm",
    install_requires = ['jieba'],
    packages = ["lemonGTM"],
    long_description = """
# LemonGTM

Lemon Global Tracking Model


## Install

```shell
pip install lemon-gtm
```


## Usage

```python
from lemonGTM import *
c = core("<Data-Filename>")
print(c.analysis("<Word>")[0])
```


## Data Format

```plain
data1
data2
data3
data4
...
```
    """,
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires = ">=3"
)
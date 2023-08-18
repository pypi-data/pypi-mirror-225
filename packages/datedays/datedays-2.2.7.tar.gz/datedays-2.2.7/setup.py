import setuptools

requires = [
    "openpyxl>=3.0.10",
    "xlrd>=2.0.1",
    "pycryptodomex>=3.15.0",
    "python-dateutil>=2.8.2",
]
with open("README-EN.md", "r") as f:
    readme = f.read()

setuptools.setup(
    name="datedays",
    version="2.2.7",
    author="JiuLiang",
    author_email="jiuliange@foxmail.com",
    description="Python Date Tools",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/liang1024/datedays",
    packages=setuptools.find_packages(),
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

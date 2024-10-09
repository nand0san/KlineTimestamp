from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kline_timestamp",  # Nombre del paquete en minúsculas
    version="0.1.1",
    author="nand0san",
    author_email="",
    description="KlineTimestamp is a Python library designed to efficiently handle timestamps within discrete time intervals, commonly known as klines or candlesticks, often used in financial data analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nand0san/kline_timestamp",
    packages=find_packages(),
    install_requires=[
        "pytz",
        "pandas"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

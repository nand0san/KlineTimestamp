from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kline_timestamp",  # Nombre del paquete en minúsculas
    version="0.1.0",
    author="nand0san",
    author_email="",
    description="Una librería Python para manejar eficientemente timestamps dentro de klines (velas).",
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

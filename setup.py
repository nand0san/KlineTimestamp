from setuptools import setup, find_packages
from pathlib import Path

# Obtener el directorio donde se encuentra setup.py
this_directory = Path(__file__).parent

# Leer README.md para el long_description
readme_path = this_directory / "README.md"
with open(readme_path, "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Leer requirements.txt para obtener las dependencias
requirements_path = this_directory / "requirements.txt"
with open(requirements_path, encoding="utf-8") as f:
    required_packages = f.read().splitlines()

setup(
    name="kline_timestamp",  # Nombre del paquete en minúsculas
    version="0.1.4",
    author="nand0san",
    author_email="",
    description="KlineTimestamp is a Python library designed to efficiently handle timestamps within discrete time intervals, commonly known as klines or candlesticks, often used in financial data analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nand0san/kline_timestamp",
    packages=find_packages(),
    include_package_data=True,  # Asegura que se respete MANIFEST.in
    install_requires=required_packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

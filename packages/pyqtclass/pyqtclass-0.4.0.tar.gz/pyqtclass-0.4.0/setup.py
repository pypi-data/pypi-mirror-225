# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyqtclass",
    version="0.4.0",
    author="innovata",
    author_email="iinnovata@gmail.com",
    description='PyQt 기반으로 동작하는 객체들의 베이스클래스 모음 패키지',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/innovata/PyQtClasses",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"":"src"},
    packages=setuptools.find_packages('src'),
    python_requires=">=3.8",
    install_requires=['PyQt5', 'ipylib'],
)

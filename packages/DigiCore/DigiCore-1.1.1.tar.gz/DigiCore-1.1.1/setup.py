# _*_ coding: utf-8 _*_
# @Time : 2023/5/19
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc :

from pathlib import Path

from setuptools import find_packages, setup

here = Path(__file__).resolve().parent
README = (here / "README.md").read_text(encoding="utf-8")

excluded_packages = ["tests", "tests.*"]


# this module can be zip-safe if the zipimporter implements iter_modules or if
# pkgutil.iter_importer_modules has registered a dispatch for the zipimporter.
try:
    import pkgutil
    import zipimport

    zip_safe = (
        hasattr(zipimport.zipimporter, "iter_modules")
        or zipimport.zipimporter in pkgutil.iter_importer_modules.registry.keys()
    )
except AttributeError:
    zip_safe = False

requires = [
"async-timeout>=4.0.2",
"certifi>=2023.5.7",
"chardet>=5.1.0",
"charset-normalizer>=3.1.0",
"colorama>=0.4.6",
"confluent-kafka>=2.1.1",
"crypto>=1.4.1",
"DBUtils>=3.0.3",
"dnspython>=2.3.0",
"et-xmlfile>=1.1.0",
"idna>=3.4",
"loguru>=0.7.0",
"lz4>=4.3.2",
"Naked>=0.1.32",
"numpy>=1.24.3",
"openpyxl>=3.1.2",
"orjson>=3.8.12",
"package-name>=0.1",
"pandas>=2.0.1",
"pycryptodome>=3.18.0",
"pycryptodomex>=3.18.0",
"pydantic>=1.10.7",
"pymongo>=4.3.3",
"PyMySQL>=1.0.3",
"python-dateutil>=2.8.2",
"pytz>=2023.3",
"PyYAML>=6.0",
"redis>=4.5.5",
"requests>=2.30.0",
"shellescape>=3.8.1",
"six>=1.16.0",
"typing_extensions>=4.5.0",
"tzdata>=2023.3",
"urllib3>=2.0.2",
"win32-setctime>=1.1.0"
]

setup(
    name="DigiCore",
    version="1.1.1",
    description="DigiCore是一个基于Python的数字化支持部第三方库，旨在为数据处理和开发提供完备的工具集和服务。",
    long_description=README,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="digicore是服务于道诚集团数字化支持部的自建第三方库项目",
    author="yarm",
    author_email="yangyang@doocn.com",
    license="MIT License",
    packages=find_packages(exclude=excluded_packages),
    install_requires=requires,
    platforms=["any"],
    zip_safe=zip_safe,
    python_requires=">=3.7",
)

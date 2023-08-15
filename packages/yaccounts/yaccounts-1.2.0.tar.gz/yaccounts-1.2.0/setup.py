from setuptools import setup

setup(
    name="yaccounts",
    packages=["yaccounts"],
    version="1.2.0",
    description="Parsing scripts for BYU's transaction details",
    author="Jeff Goeders",
    author_email="jeff.goeders@gmail.com",
    license="MIT",
    # url="https://github.com/byu-cpe/ygrader",
    install_requires=["pandas", "openpyxl", "xlsxwriter", "matplotlib", "pyyaml"],
)

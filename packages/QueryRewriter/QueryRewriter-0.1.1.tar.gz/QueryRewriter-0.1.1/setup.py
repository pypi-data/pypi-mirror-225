from setuptools import setup, find_packages

setup(
    name='QueryRewriter',
    author="Tinh Luong",
    version='0.1.1',
    install_requires=['langdetect', 'openai'],
    package_dir={"": "src"},
    packages=find_packages()
)
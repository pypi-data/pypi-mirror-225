from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fault_analyzer',
    version='0.1.0',
    description='A Python library for Pump failure Analyzer',
    author='Hu Nan',
    author_email='709043890@qq.com',
    url='https://github.com/MRHU2015114057/pump_model',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
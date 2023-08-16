from setuptools import setup, find_packages
from docs import generate_pypi_readme

setup(
    name='0xf0f-codenode',
    version='1.0rc1',
    packages=[
        'codenode',
        'codenode.nodes',
        'codenode_utilities',
    ],
    url='https://github.com/0xf0f/codenode',
    license='MIT',
    author='0xf0f',
    author_email='0xf0f.dev@gmail.com',
    long_description=generate_pypi_readme.run(),
    long_description_content_type='text/markdown',
    description='a simple framework for code generation',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)

from setuptools import setup

with open('README.md') as file:
    readme = file.read()

setup(
    name='codenode-python',
    version='1.0',
    packages=['codenode_python'],
    install_requires=['0xf0f-codenode'],
    url='https://github.com/0xf0f/codenode-python',
    license='MIT',
    author='0xf0f',
    author_email='0xf0f.dev@gmail.com',
    description='helpers for generating python using codenode',
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

import pastewin
from setuptools import setup, find_packages

setup(
    name='pastewin',
    author='Truman Purnell',
    author_email='truman.purnell@gmail.com',
    version=pastewin.__version__,
    description='A package to upload files to public s3 bucket',
    url='https://github.com/bb-labs/pastewin',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'awyes'
    ],
    entry_points={'console_scripts': ['pastewin=pastewin.pastewin:main']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='file public serve',
)

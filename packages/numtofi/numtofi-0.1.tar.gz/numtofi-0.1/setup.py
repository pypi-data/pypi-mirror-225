
from setuptools import setup, find_packages

setup(
    name='numtofi',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'numtofi=numtofi.cli:main',
        ],
    },
    author='Marko T. Manninen',
    author_email='elonmedia@gmail.com',
    description='A package to convert numbers to Finnish textual representation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/markomanninen/numtofi',
)

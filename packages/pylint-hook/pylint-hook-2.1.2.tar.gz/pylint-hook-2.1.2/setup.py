from setuptools import setup, find_packages

setup(
    name='pylint-hook',
    version='2.1.2',
    description='A Git hook that works based on Pylint evaluation',
    author='Alla Makhotka',
    author_email='all.mahotka2012@yandex.ru',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pylint-hook=pkg.main:main',
        ],
    },
    install_requires=[
        'pylint',
    ],
)
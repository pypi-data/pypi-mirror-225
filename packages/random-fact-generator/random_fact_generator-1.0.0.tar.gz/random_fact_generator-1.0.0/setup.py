from setuptools import setup, find_packages

setup(
    name='random_fact_generator',
    version='1.0.0',
    author='killermanik',
    author_email='adriankusy7@gmail.com',
    description='A module for generating random and interesting facts',
    packages=find_packages(),
    install_requires=[
        'requests',  
    ],
)
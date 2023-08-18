from setuptools import setup, find_packages

setup(
    name='netwix',
    version='0.1.0',
    license='MIT',
    description='Netwix is a python client for Netflix. With netwix by simply entering the Netflix ID the user can access data related to movies and tv shows available on Netflix',
    author='new92',
    author_email='new92github@gmail.com',
    maintainer='new92',
    maintainer_email='new92github@gmail.com',
    url='https://www.github.com/new92/netwix',
    packages=find_packages(),
    install_requires=[
        "requests",
        "bs4"
    ]
)
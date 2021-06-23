
# not a PyPi package

from setuptools import setup


def install_requirements():
    return [package_string.strip() for package_string in open('requirements.txt', 'r')]


setup(
    name='holymining',
    version='0.0.1',
    description='package of biblical mining',
    author='Kwan-Yuet Ho',
    author_email='stephenhky@yahoo.com.hk',
    packages=[
        'holymining',
        'holymining.books'
    ]
)
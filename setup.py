from setuptools import setup

setup(
    name='ZeroconfRegisterService',
    version='0.1',
    author='Meenakshi Sundaram',
    author_email='vms20591@gmail.com',
    packages=['ZeroconfRegisterService'],
    url='https://github.com/vms20591/ZeroconfRegisterService',
    description='A simple module for services to register themselves with Zeroconf for easy advertisement',
    license='GPL V3',
    long_description=open('README.md').read(),
    extras_require={
        "netifaces": ["netifaces"],
        "zeroconf": ["zeroconf"],
    },
)

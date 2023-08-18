from setuptools import setup, find_packages

with open("README.rst", "r") as f:
    long_description = f.read()

setup(
    name='dde-dnms',
    version='0.1',
    author='suncong',
    author_email='csun@elemparticle.com',
    description='给希望使用deep-time.org中注册数据用户提供的sdk',
    long_description=long_description,
    packages=find_packages(),
    license='BSD License',
    install_requires=[
        'requests'
    ]
)

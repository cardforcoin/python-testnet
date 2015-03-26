from setuptools import setup
import pkg_resources


def read(path):
    with open(pkg_resources.resource_filename(__name__, path)) as f:
        return f.read()

setup(
    name='bitcoin_testnet',
    version='0.4',
    author='Chris Martin',
    author_email='ch.martin@gmail.com',
    packages=['bitcoin_testnet'],
    url='https://github.com/cardforcoin/testnet-python',
    license='MIT',
    description='Utilities related to testnet bitcoin',
    long_description='',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=read('requirements.txt').split('\n'),
    tests_require=read('test_requirements.txt').split('\n'),
)

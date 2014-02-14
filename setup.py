# coding: utf-8
import os
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


amazon_sns = __import__('amazon_sns', {}, {}, [''])


def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-amazon-sns',
    version=amazon_sns.__version__,
    author='Vinicius Cainelli',
    author_email='',
    description=('django-amazon-sns'),
    license='MIT',
    keywords='django-amazon-sns',
    url='https://github.com/viniciuscainelli/django-amazon-sns/',
    packages=['amazon_sns'],
    long_description=read_file('README.md'),
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[r for r in read_file('requirements.txt').split('\n') if r],
    zip_safe=False,
)

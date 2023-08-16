
from setuptools import setup, find_packages

setup(
    name='passwordless-27',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Matthew Fiallos',
    author_email='matthew.fiallos@randstadusa.com',
    description='A client library for Bitwarden''s Passwordless.dev API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    #url='https://github.com/yourusername/passwordless-client',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
)

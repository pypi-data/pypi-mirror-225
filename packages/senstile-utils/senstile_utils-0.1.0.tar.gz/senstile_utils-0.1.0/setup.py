from setuptools import setup, find_packages

setup(
    name='senstile_utils',
    version='0.1.0',
    packages=find_packages(exclude=['user_tests*', "test*","test.*"]),
    install_requires=[
    ],
    extras_require={
        'dev': [
            'pytest',
            'requests',
            'pytest-asyncio'
        ]
    },
    python_requires='>=3.6',
    author='Jose Alejandro Concepcion Alvarez',
    author_email='pepe@senstile.com',
    description='A set of common utils modules and functions for Senstile Python Api development',
)

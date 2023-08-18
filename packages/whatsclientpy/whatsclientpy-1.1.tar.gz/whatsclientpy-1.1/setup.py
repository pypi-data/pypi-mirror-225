from setuptools import setup, find_packages

setup(
    name='whatsclientpy',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'annotated-types',
        'bidict',
        'certifi',
        'charset-normalizer',
        'idna',
        'pydantic',
        'pydantic_core',
        'python-engineio',
        'python-socketio',
        'requests',
        'typing_extensions',
        'urllib3',
        'websocket-client'
    ],
    author='Jesus Enrique De Alba Gaytan',
    author_email='enrique.dealba@focograficomx.com',
)
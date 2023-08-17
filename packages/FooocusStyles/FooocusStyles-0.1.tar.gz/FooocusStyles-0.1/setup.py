from setuptools import setup, find_packages

setup(
    name='FooocusStyles',
    version='0.1', 
    packages=find_packages(),
    install_requires=[
        'Pillow==8.3.2',
        'requests==2.26.0',
    ],
    entry_points={
        'console_scripts': [
            'fooocus-styles=my_package.main:main',
        ],
    },
)

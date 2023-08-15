from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='neuronautics',
    version='0.1.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'neuronautics = neuronautics.main:main',
        ],
    },
    install_requires=requirements,
)

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='neuronautics',
    version='0.1.7',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'neuronautics = neuronautics.main:main'
        ]
    },
    author='Daniel de Santos Sierra',
    author_email='desantossierra@gmail.com',
    description='Description of your project',
    #license='MIT',  # Or any other license you prefer
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
)
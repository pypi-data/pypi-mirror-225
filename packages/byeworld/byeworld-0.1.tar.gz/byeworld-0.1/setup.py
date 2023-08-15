from setuptools import setup, find_packages

setup(
    name='byeworld',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'byeworld = byeworld:say_bye',
        ],
    }
)

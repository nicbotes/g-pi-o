from setuptools import setup, find_packages

setup(
    name='7segment',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'RPi.GPIO',
    ],
    entry_points={
        'console_scripts': [
            '7segment=7segment.display:main',
        ],
    },
)

from setuptools import setup, find_packages

with open('requirements.txt', 'r', encoding='utf-8') as fh:
    requirements = fh.read()

setup(
    name='acvsn-checker',
    version='0.1.5',
    description="Checks if a standard name follows the ACVSN conventions",
    packages=find_packages(),
    package_data={
        'acvsn_checker': [
            'data/*.json'
        ]
    },
    include_package_data=True,
    python_requires='>=3.4',
    install_requires=[requirements],
    entry_points={
        'console_scripts': [
            'checker = acvsn_checker.checker:main',
        ]
    }
)

from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='datawhistle',
    version='0.1.dev',
    packages=find_packages(),
    url='https://github.com/akeanewow/DataWhistle',
    download_url='https://github.com/akeanewow/DataWhistle',
    license='GPL-3.0',
    entry_points={'console_scripts': [
        'datawhistle = datawhistle.__main__:main'
    ]},
    install_requires=requirements
)

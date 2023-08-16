from setuptools import setup, find_packages

setup(
    name='mineCube',
    version='0.1.3',
    author='Abdellatif Ahammad',
    description='MineCube a lib for creating process cubes in offline, streaming or even mixed modes.',
    packages=find_packages(),
    install_requires=[
        "pandas",
        "Flask",
        "Flask-Cors"
    ],
)

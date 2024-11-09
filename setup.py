import pathlib
import setuptools
import pkg_resources

with open('README.md', 'r') as f:
    long_description = f.read()

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setuptools.setup(
    name = 'nexxt',
    version = '0.1',
    description = 'TODO',
    long_description = long_description,
    author = 'GeekedSquad',
    author_email= 'robertcnst02@gmail.com',
    packages = [ 'nexxt' ],
    install_requires = install_requires
)

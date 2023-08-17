import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()
REQUIRES = (HERE / "requirements.txt").read_text()
REQUIRES = [s.strip() for s in REQUIRES.splitlines()]

setup(
    name='airtech-shared-libery',
    version='0.0.1',
    description='Minha biblioteca compartilhada',
    license='MIT',
    author='Airtech',
    long_description=README,
    packages=find_packages(exclude=['tests']),
    install_requires=REQUIRES,
    include_package_data=True,
    zip_safe=False,
)

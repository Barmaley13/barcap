"""
Packaging this baby...
"""

from setuptools import setup, find_packages

from barcap import __version__


with open('README.md') as f:
    readme = f.read()


with open('LICENSE') as f:
    license = f.read()


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='barcap',
    version=__version__,
    description='Extract any barcode using your web camera',
    long_description=readme,
    author='Kirill V. Belyayev',
    author_email='kbelyayev@gmail.com',
    url='https://github.com/Barmaley13/BarcodeCapture',
    license=license,
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': ['barcode_capture = barcap.main:main']},
    install_requires=requirements
)

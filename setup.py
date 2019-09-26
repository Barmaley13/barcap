"""
Packaging this baby...
"""

import os
from setuptools import setup, find_packages

from barcap import __version__
import barcap.device_list.setup as dev_setup


if __name__ == '__main__':
    # Add device setup only on Windows
    dep_links = []
    if os.name == 'nt':
        dev_path = os.path.dirname(os.path.abspath(dev_setup.__file__))
        dep_links.append(f'file:/{dev_path}')

    # Add our standard setup
    # # FIXME: Markdown is broken for some reason
    # with open('README.md', encoding='utf-8') as f:
    #     readme = f.read()

    with open('LICENSE') as f:
        license = f.read()

    with open('requirements.txt') as f:
        requirements = f.read().splitlines()

    setup(
        name='barcap',
        version=__version__,
        description='Extract any barcode using your web camera',
        # long_description=readme,
        # long_description_content_type='text/markdown',
        author='Kirill V. Belyayev',
        author_email='kbelyayev@gmail.com',
        url='https://github.com/Barmaley13/BarcodeCapture',
        license=license,
        packages=find_packages(),
        include_package_data=True,
        entry_points={'console_scripts': ['barcode_capture = barcap.main:main']},
        dependency_links=dep_links,
        install_requires=requirements
    )

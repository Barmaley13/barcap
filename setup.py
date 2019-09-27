"""
Packaging this baby...
"""

import os
import re
import codecs
from setuptools import setup, find_packages


base_path = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(base_path, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


if __name__ == '__main__':
    # Add our standard setup
    readme = read('README.md')
    requirements = read('requirements.txt').splitlines()

    # Add device setup only on Windows
    dep_links = []
    if os.name == 'nt':
        dev_path = os.path.join(base_path, 'barcap', 'device_list')
        dep_links.append(f'file:/{dev_path}')
        # Forcing wheel installation
        dep_links.append('https://files.pythonhosted.org/packages/3d/14/97bf8e36fb58965415e3c7d8f95cfd6375cb0b5464ae9dbc0a48f7f9ab19/pyzbar-0.1.8-py2.py3-none-win_amd64.whl')
        dep_links.append('https://files.pythonhosted.org/packages/91/8a/4694f3214da07dc488c422c355415a860024126b2714d8f4bf1f73419587/pylibdmtx-0.1.9-py2.py3-none-win_amd64.whl')
        requirements.append('WindowsDevices')

    setup(
        name='barcap',
        version=find_version('barcap', '__init__.py'),
        description='Extract any barcode using your web camera',
        long_description=readme,
        long_description_content_type='text/markdown',
        author='Kirill V. Belyayev',
        author_email='kbelyayev@gmail.com',
        python_requires='>=3.6.0',
        url='https://github.com/Barmaley13/BarcodeCapture',
        license='MIT',
        packages=find_packages(),
        include_package_data=True,
        entry_points={'console_scripts': ['barcode_capture = barcap.main:main']},
        dependency_links=dep_links,
        install_requires=requirements,
        zip_safe=False
    )

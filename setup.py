"""
Packaging this baby...
"""

import io
import os
from setuptools import setup, find_packages, Extension

from barcap import __version__


# Find base path
base_path = os.path.abspath(os.path.dirname(__file__))

# Adding README.md as package description
readme_path = os.path.join(base_path, 'README.md')
with io.open(readme_path, encoding='utf-8') as f:
    readme = f.read()

# Adding requirements
requirements_path = os.path.join(base_path, 'requirements.txt')
with io.open(requirements_path, encoding='utf-8') as f:
    requirements = f.read().splitlines()

# Add device setup only on Windows
dep_links = []
ext_modules = []
if os.name == 'nt':
    # Forcing wheel installation
    dep_links.append('https://files.pythonhosted.org/packages/3d/14/97bf8e36fb58965415e3c7d8f95cfd6375cb0b5464ae9dbc0a48f7f9ab19/pyzbar-0.1.8-py2.py3-none-win_amd64.whl')
    dep_links.append('https://files.pythonhosted.org/packages/91/8a/4694f3214da07dc488c422c355415a860024126b2714d8f4bf1f73419587/pylibdmtx-0.1.9-py2.py3-none-win_amd64.whl')

    # # Adding WindowsDevice extension (optional)
    # dev_path = os.path.join('barcap', 'device_list', 'device.cpp')
    # ext_modules.append(
    #     Extension(
    #         'device',
    #         sources=[dev_path],
    #         library_dirs=[r'G:\Program Files\Microsoft SDKs\Windows\v6.1\Lib']
    #     )
    # )

# And finally setup script
setup(
    name='barcap',
    version=__version__,
    description='Extract any barcode using your web camera',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Kirill V. Belyayev',
    author_email='kbelyayev@gmail.com',
    python_requires='>=3.6.0',
    url='https://github.com/Barmaley13/barcap',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': ['barcode_capture = barcap.main:main']},
    dependency_links=dep_links,
    install_requires=requirements,
    ext_modules=ext_modules,
    zip_safe=False
)

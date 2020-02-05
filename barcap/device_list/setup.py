"""
https://github.com/yushulx/python-capture-device-list
"""

import io
import os
from distutils.core import setup, Extension

with io.open('README.md', encoding='utf-8') as f:
    readme = f.read()

dev_path = os.path.dirname(os.path.abspath(__file__))
module_device = Extension(
    'device',
    sources=[f'{dev_path}{os.path.sep}device.cpp'],
    library_dirs=[r'G:\Program Files\Microsoft SDKs\Windows\v6.1\Lib']
)

setup(
    name='WindowsDevices',
    version='1.0.1',
    description='Get device list with DirectShow',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',
    ext_modules=[module_device]
)

"""
https://github.com/yushulx/python-capture-device-list
"""

import os
from distutils.core import setup, Extension

dev_path = os.path.dirname(os.path.abspath(__file__))
module_device = Extension(
    'device',
    sources=[f'{dev_path}{os.path.sep}device.cpp'],
    library_dirs=['G:\Program Files\Microsoft SDKs\Windows\v6.1\Lib']
)

setup(
    name='WindowsDevices',
    version='1.0',
    description='Get device list with DirectShow',
    ext_modules=[module_device]
)

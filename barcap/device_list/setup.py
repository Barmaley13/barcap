"""
https://github.com/yushulx/python-capture-device-list
"""

import os
from distutils.core import setup, Extension

# # FIXME: Markdown is broken for some reason
# with open('README.md', encoding='utf-8') as f:
#     readme = f.read()

with open('LICENSE') as f:
    license = f.read()

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
    # long_description=readme,
    # long_description_content_type='text/markdown',
    license=license,
    ext_modules=[module_device]
)

"""
Path finder to append outside modules

Allows to run module as an executable like so
```bash
python barcode.py
python ocr.py
python ocr_plus.py
```

Also, allows to run package as an executable like so
```bash
python -m barcap
```
"""

import os
import sys

barcap_path = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(barcap_path)
sys.path.append(base_path)

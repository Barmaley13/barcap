"""
Capture OCR Algorithm

Algorithm does half of the work. The other half of the work is having proper setup!
Having higher resolution camera with automatic focus is a key.
(I've used 720p resolution on my Android and it worked pretty well!)
Use a stand for your camera! Shaky hands will introduce error readings!!!
"""

import logging

import cv2
import pytesseract

if __name__ == '__main__':
    import path_finder

from barcap.capture import CaptureProcess


# Constants
TESS_CMD = 'tesseract'
# TESS_CMD = r'"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"'
TESS_DATA = r'"C:\Program Files (x86)\Tesseract-OCR\tessdata"'
# TESS_CONF = f'--tessdata-dir {TESS_DATA} --oem 1 --psm 11'
TESS_CONF = f'--oem 1 --psm 11'

DEFAULT_WINDOW_NAME = 'OCR Capture'


class OCRCapture(CaptureProcess):
    """ OCR Capture Process based on Process class """
    def __init__(self, **kwargs):
        # Set default window name (if needed)
        if 'name' not in kwargs or kwargs['name'] is None:
            kwargs['name'] = DEFAULT_WINDOW_NAME

        super(OCRCapture, self).__init__(**kwargs)

        # Save name for the frame capture
        self._save_name = 'ocr.jpg'

        # Set OCR specific kwargs
        self.tess_cmd = TESS_CMD
        if 'tess_cmd' in kwargs:
            self.tess_cmd = kwargs['tess_cmd']

        self.tess_conf = TESS_CONF
        if 'tess_conf' in kwargs:
            self.tess_conf = kwargs['tess_conf']

        self.lang = 'eng'
        if 'lang' in kwargs:
            self.lang = kwargs['lang']

        # Setup pytesseract
        pytesseract.pytesseract.tesseract_cmd = self.tess_cmd

    def process_frame(self, frame):
        """ This method does all the frame processing work """
        # Convert to RGB format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Analyze the frame
        results = pytesseract.image_to_string(frame, lang=self.lang, config=self.tess_conf)

        # Save results of the OCR
        if len(results) > 0:
            self.save_capture(results)


if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(level=logging.DEBUG, format=f'%(levelname)s: %(message)s')

    # Default camera index
    camera_index = 0

    # Start capture
    capture = OCRCapture(camera=camera_index)

    # Note: Running loop directly here. Use start method to run as a process
    capture.run()

"""
Capture Barcode Algorithm

Algorithm does half of the work. The other half of the work is having proper setup!
Having higher resolution camera with automatic focus is a key.
(I've used 720p resolution on my Android and it worked pretty well!)
Use a stand for your camera! Shaky hands will introduce error readings!!!
"""

import logging

import cv2
from pyzbar import pyzbar
from pylibdmtx import pylibdmtx

if __name__ == '__main__':
    import path_finder

from barcap.capture import CaptureProcess


# Constants
DEFAULT_WINDOW_NAME = 'Barcode Capture'


class BarcodeCapture(CaptureProcess):
    """ Barcode Capture Process based on CaptureProcess class """
    def __init__(self, **kwargs):
        # Set default window name (if needed)
        if 'name' not in kwargs or kwargs['name'] is None:
            kwargs['name'] = DEFAULT_WINDOW_NAME

        super(BarcodeCapture, self).__init__(**kwargs)

        # Save name for the frame capture
        self._save_name = 'barcode.jpg'

        # Set barcode specific kwargs
        self.invert = False
        if 'invert' in kwargs:
            self.invert = kwargs['invert']

    def process_frame(self, frame):
        """ This method does all the frame processing work """
        # Convert to gray
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Invert colors (if needed)
        if self.invert is True:
            frame = cv2.bitwise_not(frame)

        # Figure out dimensions of the frame
        height, width = frame.shape[:2]

        # Analyze the frame
        results = []
        results += pyzbar.decode((frame.tobytes(), width, height))
        results += pylibdmtx.decode((frame.tobytes(), width, height), timeout=100)

        if len(results):
            # logging.debug(f'results: {results}')
            for result in results:
                # Save result of the barcode capture
                self.save_capture(result.data)

        return frame


if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(level=logging.DEBUG, format=f'%(levelname)s: %(message)s')

    # Default camera index
    camera_index = 0

    # Start capture
    capture = BarcodeCapture(camera=camera_index)

    # Note: Running loop directly here. Use start method to run as a process
    capture.run()

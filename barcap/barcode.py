"""
Capture Barcode Algorithm

Algorithm does half of the work. The other half of the work is having proper setup!
Having higher resolution camera with automatic focus is a key.
(I've used 720p resolution on my Android and it worked pretty well!)
Use a stand for your camera! Shaky hands will introduce error readings!!!
"""

import cv2
from pyzbar import pyzbar
from pylibdmtx import pylibdmtx

from capture import CaptureProcess


# Constants
DEFAULT_WINDOW_NAME = 'Barcode Capture'


class BarcodeCapture(CaptureProcess):
    """ Barcode Capture Process based on CaptureProcess class """
    def __init__(self, **kwargs):
        if 'name' not in kwargs or kwargs['name'] is None:
            # Set default window name
            kwargs['name'] = DEFAULT_WINDOW_NAME

        super(BarcodeCapture, self).__init__(**kwargs)

        # Save name for the frame capture
        self._save_name = 'barcode.jpg'

    def process_frame(self, frame):
        """ This method does all the frame processing work """
        # Convert to gray
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Invert colors (if needed)
        if self.invert:
            frame = cv2.bitwise_not(frame)

        # Display the resulting frame
        cv2.imshow(self.name, frame)

        # Figure out dimensions of the frame
        height, width = frame.shape[:2]

        # Analyze the frame
        results = []
        results += pyzbar.decode((frame.tobytes(), width, height))
        results += pylibdmtx.decode((frame.tobytes(), width, height), timeout=100)

        if len(results):
            # print(f'results: {results}')
            for result in results:
                # Save result of the barcode capture
                self.save_capture(result.data)


if __name__ == '__main__':
    # Default camera index
    camera_index = 0

    # Start capture
    capture = BarcodeCapture(camera=camera_index)

    # Note: Running loop directly here. Use start method to run as a process
    capture.run()

"""
Capture OCR Algorithm (with pre-processing)

This is "improved" OCR with some pre-processing applied
"""

import logging

import cv2
import pytesseract

if __name__ == '__main__':
    import path_finder

from barcap.ocr import OCRCapture


# Constants
DEFAULT_WINDOW_NAME = 'OCR Plus Capture'


class OCRPlusCapture(OCRCapture):
    """ OCRPlusCapture based on OCRCapture class """
    def __init__(self, **kwargs):
        # Set default window name (if needed)
        if 'name' not in kwargs or kwargs['name'] is None:
            kwargs['name'] = DEFAULT_WINDOW_NAME

        super(OCRPlusCapture, self).__init__(**kwargs)

        # Save name for the frame capture
        self._save_name = 'ocr_plus.jpg'

    def process_frame(self, frame):
        """ This method does all the frame processing work """
        # Convert to gray
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # # Adaptive Gaussian Thresholding
        # frame = cv2.adaptiveThreshold(
        #     frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 31, 2)

        # # Median blur
        # frame = cv2.medianBlur(frame, 3)

        # Gaussian blur
        frame = cv2.GaussianBlur(frame, (5, 5), 0)

        # # Truncate thresholding
        # frame = cv2.threshold(frame, 230, 255, cv2.THRESH_TRUNC)[-1]

        # Otsu's thresholding
        frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[-1]

        # NiBlack Thresholding
        # frame = cv2.ximgproc.niBlackThreshold(frame, 255, cv2.THRESH_BINARY, 55, 0.5)

        # Analyze the frame
        results = pytesseract.image_to_string(frame, lang='eng', config=self.tess_conf)

        # Save results of the OCR
        if len(results) > 0:
            self.save_capture(results)

        return frame


if __name__ == '__main__':
    # # Manual command (for your reference)
    # tesseract ocr.jpg stdout -l eng --oem 3 --psm 11 -c tessedit_write_images=true

    # Setup logging
    logging.basicConfig(level=logging.DEBUG, format=f'%(levelname)s: %(message)s')

    # Default camera index
    camera_index = 0

    # Start capture
    capture = OCRPlusCapture(camera=camera_index)
    # capture = OCRPlusCapture(camera=camera_index, width=1600, height=1200)

    # Note: Running loop directly here. Use start method to run as a process
    capture.run()

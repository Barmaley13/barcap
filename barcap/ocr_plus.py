"""
Capture OCR Algorithm (with pre-processing)

This is "improved" OCR with some pre-processing applied
"""

import cv2
import pytesseract

from capture import CaptureProcess


# Constants
TESS_CMD = 'tesseract.exe'
# TESS_CMD = r'"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"'
TESS_DATA = r'"C:\Program Files (x86)\Tesseract-OCR\tessdata"'
TESS_CONFIG = f'--tessdata-dir {TESS_DATA} --oem 1 --psm 11'

DEFAULT_WINDOW_NAME = 'OCR Plus Capture'


# Pytesseract setup
pytesseract.pytesseract.tesseract_cmd = TESS_CMD


class OCRCapture(CaptureProcess):
    """ OCR Capture Process based on Process class """
    def __init__(self, **kwargs):
        if 'name' not in kwargs or kwargs['name'] is None:
            # Set default window name
            kwargs['name'] = DEFAULT_WINDOW_NAME

        super(OCRCapture, self).__init__(**kwargs)

    def process_frame(self, frame):
        """ This method does all the frame processing work """
        # Convert to gray
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Invert colors (if needed)
        if self.invert:
            frame = cv2.bitwise_not(frame)

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

        # Display the resulting frame
        cv2.imshow(self.name, frame)

        # Analyze the frame
        results = pytesseract.image_to_string(frame, lang='eng', config=TESS_CONFIG)

        # Save results of the OCR
        if len(results) > 0:
            self.save_capture(results)


if __name__ == '__main__':
    # # Manual command (for your reference)
    # tesseract ocr.jpg stdout -l eng --oem 3 --psm 11 -c tessedit_write_images=true

    # Default camera index
    camera_index = 1

    # Start capture
    capture = OCRCapture(camera=camera_index)
    # capture = OCRCapture(camera=camera_index, width=1600, height=1200)

    # Note: Running loop directly here. Use start method to run as a process
    capture.run()

"""
Capture Barcode Algorithm

Algorithm does half of the work. The other half of the work is having proper setup!
Having higher resolution camera with automatic focus is a key.
(I've used 720p resolution on my Android and it worked pretty well!)
Use a stand for your camera! Shaky hands will introduce error readings!!!
"""

import os
import time
from multiprocessing import Process, Value, Array

import cv2

from pyzbar import pyzbar
from pylibdmtx import pylibdmtx


DEFAULT_WINDOW_NAME = 'Barcode Capture'
DEFAULT_ARRAY_LEN = 255


class BarcodeCapture(Process):
    """ Capture bar code Process based on Process class """
    def __init__(
            self,
            camera: int = 0,
            name: str = None,
            width: int = None,
            height: int = None,
            invert: bool = False,
            debug: bool = True
    ):
        super(BarcodeCapture, self).__init__()

        if name is None:
            name = DEFAULT_WINDOW_NAME

        self.camera = camera
        self.name = name
        self.width = width
        self.height = height
        self.invert = invert
        self.debug = debug

        self._output = Array('b', [0]*DEFAULT_ARRAY_LEN)
        self._new = Value('b', False)
        self._stop = Value('b', False)
        self._last_epoch = Value('f')

    def run(self):
        if os.name == 'nt':
            cap = cv2.VideoCapture(self.camera, cv2.CAP_DSHOW)
        else:
            cap = cv2.VideoCapture(self.camera)

        # Trying to set resolution (1600 x 1200)
        if self.width is not None:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)

        if self.height is not None:
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        if self.debug:
            print(f'current width: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}')
            print(f'current height: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}')

        while cap.isOpened():
            # Capture frame-by-frame
            ret, frame = cap.read()

            if ret is True:
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
                        output = result.data

                        # Debugging
                        if self.debug:
                            _output = output.decode('utf-8')
                            print(f'output: {_output}')

                        if len(output) <= DEFAULT_ARRAY_LEN:
                            # Copy barcode into array
                            self._output[:len(output)] = output[:]
                            # Null the rest of the array
                            self._output[len(output):] = [0]*(DEFAULT_ARRAY_LEN-len(output))
                            # Record the time
                            self._last_epoch.value = time.time()
                            # Set new capture flag
                            self._new.value = True
                        else:
                            raise OverflowError('Shared array is too small to represent this barcode!')

                # Capture key press
                command = cv2.waitKey(delay=20)

                # Parse command
                if command > 0:
                    command = chr(command)

                    if self.debug:
                        print(f'command: {command}')

                    # Save frame for the code recognition (Manual capture)
                    if command in ('s', 'S'):
                        cv2.imwrite('barcode.jpg', frame)

                    # Close Video capture
                    elif command in ('q', 'Q', '\x1b'):
                        break

                # Capture Window close using 'X' button
                try:
                    if cv2.getWindowProperty(self.name, cv2.WND_PROP_VISIBLE) < 1:
                        break
                except cv2.error:
                    break

                # Stop via explicit command
                if self._stop.value:
                    break

            else:
                break

        # When everything is done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    @property
    def output(self) -> str:
        self._new.value = False
        _output = bytearray(self._output[:])
        _output = _output.decode('utf-8')
        _output = _output.replace('\x00', '')
        return _output

    @property
    def last_epoch(self) -> float:
        return self._last_epoch.value

    @property
    def new(self) -> bool:
        return self._new.value

    def stop(self):
        self._stop.value = True


if __name__ == '__main__':
    # Default camera index
    camera_index = 0

    # Start capture
    capture = BarcodeCapture(camera=camera_index)

    # Note: Running loop directly here. Use start method to run as a process
    capture.run()

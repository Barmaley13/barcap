"""
CaptureProcess base class.

This class overloads python's built-in `Process` class from
multiprocessing package.

The idea is to run this process and capture frames from a web camera.
Next, those frames will be processed to get desired output.

You could use this class to build your own capturing algorithm.
For examples, look closely at `barcode.py`, `ocr.py` and `ocr_plus.py`.

And finally, the user of the capture process would start a process and
get results via shared memory. Look closely at `main.py` to get a complete example.

Finally, `device_list.py` facilitates in selecting right camera. In case
you might have multiple cameras connected to your computer.
"""

import os
import time
import logging

from typing import Union
from abc import ABC, abstractmethod
from multiprocessing import Process, Value, Array

import cv2
import numpy


# Constants
DEFAULT_ARRAY_LEN = 1024


class CaptureProcess(Process, ABC):
    """ CaptureProcess based on Process class """
    def __init__(
            self,
            camera: int = 0,
            name: str = None,
            width: int = None,
            height: int = None,
            display: bool = True,
            **kwargs
    ):
        # Init Process
        super(CaptureProcess, self).__init__()

        # Init public members
        self.camera = camera
        self.name = name
        self.width = width
        self.height = height
        self.display = display

        # Init private members
        self._save_name = 'capture.jpg'

        # Set shared memory members
        self._output = Array('b', [0] * DEFAULT_ARRAY_LEN)
        self._new = Value('b', False)
        self._stop = Value('b', False)
        self._last_epoch = Value('f')

    # Internal methods
    def run(self):
        """ This is main loop of the capture process """
        if os.name == 'nt':
            cap = cv2.VideoCapture(self.camera, cv2.CAP_DSHOW)
        else:
            cap = cv2.VideoCapture(self.camera)

        # Trying to set resolution (1600 x 1200)
        if self.width is not None:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)

        if self.height is not None:
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        logging.debug(f'current width: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}')
        logging.debug(f'current height: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}')

        while cap.isOpened():
            # Capture frame-by-frame
            ret, frame = cap.read()

            if ret is True:
                _frame = self.process_frame(frame)

                # Update frame for display (if needed)
                if _frame is not None:
                    frame = _frame

                # Display the resulting frame (if enabled)
                if self.display:
                    cv2.imshow(self.name, frame)

                # Capture key press
                command = cv2.waitKey(delay=20)

                # Parse command
                if command > 0:
                    command = chr(command)

                    logging.debug(f'command: {command}')

                    # Save frame for the code recognition (Manual capture)
                    if command in ('s', 'S'):
                        cv2.imwrite(self._save_name, frame)

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

    @abstractmethod
    def process_frame(self, frame) -> Union[None, numpy.ndarray]:
        """ This method does all the frame processing work """
        pass

    def save_capture(self, data: Union[str, bytes]):
        """ This method saves captured data to output buffer """
        # Convert data
        if type(data) is str:
            data_str = data
            # Encode to utf-8
            data_bytes = data.encode('utf-8')
        elif type(data) is bytes:
            data_bytes = data
            # Decode to utf-8
            data_str = data.decode('utf-8')
        else:
            raise TypeError(f"Unsupported type '{type(data)}' for save_capture method!")

        # Debugging
        logging.debug(f'output: {data_str}')

        # Save data to output buffer
        data_len = len(data_bytes)
        if data_len <= DEFAULT_ARRAY_LEN:
            # Copy capture into array
            self._output[:data_len] = bytes(data_bytes)

            # Null the rest of the array
            self._output[data_len:] = [0] * (DEFAULT_ARRAY_LEN - data_len)

            # Record the time
            self._last_epoch.value = time.time()

            # Set new capture flag
            self._new.value = True

        else:
            raise OverflowError('Output buffer is too small to fit this capture!')

    # External methods
    @property
    def output(self) -> str:
        """ This property returns latest output from the capturing process """
        # Clear new capture flag
        self._new.value = False

        # Convert output byte array to sting
        _output = bytes(self._output.get_obj())
        _output = _output.decode('utf-8')
        _output = _output.replace('\x00', '')

        return _output

    @property
    def last_epoch(self) -> float:
        """ This property returns epoch of the last capture """
        return self._last_epoch.value

    @property
    def new(self) -> bool:
        """
        This flag is set to `True` on new data capture.
        This flag is set to `False` by reading the output of the last capture.
        """
        return self._new.value

    def stop(self):
        """ Call this method to stop capture process """
        self._stop.value = True

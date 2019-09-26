"""
Run capture as a separate process
"""

import time

from .capture import BarcodeCapture


if __name__ == '__main__':
    # Default camera index
    camera_index = 0

    # Camera selection routine
    try:
        from .device_list.test import select_camera, camera_list

        # Get camera list
        dev_list = camera_list()

        # Select a camera
        camera_index = select_camera(len(dev_list))
    except:
        print('Unable to run camera selection routine!')

    # Start capture
    # print(f'camera_index: {camera_index}')
    capture = BarcodeCapture(camera=camera_index)
    capture.start()

    # Run capture loop
    while capture.is_alive():
        output = capture.output
        if len(output):
            # # Debugging
            # print(f'output: {output}')

            # Debugging
            time_stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(capture.last_epoch))
            print(f'last capture: {time_stamp}')

            # # Stop capture on the first output reading
            # capture.stop()
            # break

        time.sleep(0.1)

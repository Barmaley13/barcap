"""
This module demonstrates how to use camera selection routines
"""

import cv2

import device


def select_camera(device_len):
    hint = 'Select a camera: '
    try:
        index = int(input(hint))
        # select = int(select)

    except Exception:
        print("It's not a number!")
        return select_camera(device_len)

    if index > device_len:
        print('Invalid number! Retry!')
        return select_camera(device_len)

    return index


def camera_list(print_list=True):
    # Fetch device list
    dev_list = []
    try:
        dev_list = device.getDeviceList()
    except:
        pass

    # Print device list
    if print_list:
        if len(dev_list):
            for index, name in enumerate(dev_list):
                print(f'{index}: {name}')

        else:
            print('No device is connected')

    return dev_list


def open_camera(index):
    cap = cv2.VideoCapture(index)
    return cap


def main():
    # print OpenCV version
    print(f'OpenCV version: {cv2.__version__}')

    # Get camera list
    dev_list = camera_list()

    # Select a camera
    camera_number = select_camera(len(dev_list))

    # Open camera
    cap = open_camera(camera_number)

    if cap.isOpened():
        # Frame Width
        width = cap.get(3)
        # Frame Height
        height = cap.get(4)
        print(f'Default width: {width}, height: {height}')

        while True:
            # Read and show image
            ret, frame = cap.read()
            cv2.imshow('frame', frame)

            # Capture key press
            command = cv2.waitKey(20)

            # Parse command
            if command > 0:
                command = chr(command)

                # Close Video capture on q, Q or ESC
                if command in ('q', 'Q', '\x1b'):
                    break

            # Capture Window close using 'X' button
            try:
                if cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) < 1:
                    break
            except cv2.error:
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

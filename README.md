# Barcode Capture

## Introduction
This code was made to extract any barcode using your web camera.
As of now it utilizes `pyzbar` and `pylibdmtx` libraries. Which have their own set of
recognizable barcodes. Mainly, we were targeting QR codes and data matrix codes. But it will
recognize other popular formats supported by those libraries.

Under the hood, this code takes each frame from the camera like so

![Web Camera Frame](https://raw.githubusercontent.com/Barmaley13/BarcodeCapture/master/images/barcode1.jpg)

And detects barcode if it present.
And finally provides output as a string like so
```
output: Wikipedia, the free encyclopedia
```

There is a probability that algorithm will fail during one of those steps. In such case the code will not 
produce any output. Also, there is a small possibility that the algorithm will provide incorrect output. So keep 
that in mind while capturing barcodes!

## Requirements
This code has been tested on Windows machine. Most likely it will work on alternative OS but we have not
tested it on any other OS.

Otherwise, you will need:

* Python 3
* OpenCV 2
* pyzbar
* pylibdmtx
* Web Camera

## Easy installation
Use pip to install this library, fast and easy!!!
```bash
pip install barcap
```

## Manual installation
### Install libraries
On Linux, you have to install some extra packages:
```bash
sudo apt-get install libzbar0
sudo apt-get install libdmtx0a
```

On MAC, that be a little different:
```bash
brew install zbar
brew install libdmtx
```

On Windows, everything should happen automatically. 
If you have any dll problems, please install 
[Visual C++ Redistributable Packages for Visual Studio 2013](https://www.microsoft.com/en-US/download/details.aspx?id=40784)
and see if that resolves those issues.

### Install python packages
You can install requirements using
```bash
pip install -r requirements.txt
```

## Further instructions
* https://pypi.org/project/pyzbar/
* https://pypi.org/project/pylibdmtx/


## Most Basic Barcode Capture
This is the simplest way to get you started. Also this is the best way to make sure that your setup works properly.
Simply run in a shell:

```bash
python -m barcap
```

Window with your default camera is going to pop up and capture algorithm will be running in a while loop.
If everything is successful you will see output periodically printed out in the shell.

### Manual Capture
Once again start while capture loop by running:
```
$ python -m barcap
```

First of all, make sure your capture window is selected.
Once, you have a good image in the window with barcode occupying most of the screen press `'s'` key to save this frame.
Open `barcode.jpg` and confirm that the frame has been written. Kill the loop by pressing `'q'` or `Esc`.

#### If it does not work...
* Do you have camera connected?
* Is computer even on?
* If nothing helps fix your hardware in the software!

All jokes aside most likely the libraries do not support this barcode or something wrong with a setup.

### Final Thoughts
At this point you probably understand how my routine works so you can try modifying it if things are not working out. 

Otherwise, **Congratulations!!! You got it working!!!**
 
## Importing Barcode Capture into your own python script
If you look closely, you will see that capture loop is inside `CaptureProcess` class based on `Process` class 
from `multiprocessing` module.

The idea is to run this process and capture frames from a web camera.
Next, those frames will be processed to get desired output.

You could use this class to build your own capturing algorithm.
For examples, look closely at `barcode.py`, `ocr.py` and `ocr_plus.py`.

And finally, the user of the capture process would start a process and
get results via shared memory.

Here is how you can take advantage of those in your own script.

To **create** a capture instance do following:
```python
from barcap.barcode import BarcodeCapture     
capture = BarcodeCapture(camera=0)
```

To **start** capturing process:
```python
capture.start()
```

To **stop** capturing process:
```python
capture.stop()
```
or
```python
capture.terminate()
```

To **check** if capturing is still happening:
```python
capture.is_alive()
```

To **read** decoded output:
```python
output = capture.ouput
print(f'output: {output}')
```

To **fetch** epoch time of the last decoding:
```python
import time

epoch = capture.last_epoch
time_stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))
print(f'last capture: {time_stamp}')
```

You can also check if **new** output is available
```python
if capture.new:
    print(f'output: {capture.output}')
```
Every time you read output it resets the `new` flag.

Look closely at `main.py` to get a complete example.

Finally, `device_list.py` facilitates in selecting right camera. In case
you might have multiple cameras connected to your computer.

## Device List
There is a little device utility that can help you discover connected cameras to the
computer. As of right now the sub package works only on Windows. Also, we decided
that this is optional addition so it won't be compiled by default.

In order to compile navigate to `setup.py` script and uncomment lines for the
`WindowsDevice` extension. Reinstall `barcap` using `setup.py` script.

## Additional Info and Questions

Shoot me email at `kirill at kbelyayev.com` if you have any questions, suggestions, improvements, additions and etc.
I would love to help you with this script if you hire me as a contractor. I might help you free of charge if 
you contribute to this distribution or ask politely. Beer donations are welcome too!

**Good luck! Happy coding and hacking!**

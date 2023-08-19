
.. image:: https://www.pco.de/fileadmin/user_upload/company/pco_logo.png
   :width: 100pt

|PyPI-Versions| |LICENCE| |Platform| |PyPI-Status|

The Python package **pco** is a powerful and easy to use high level Software Development Kit (SDK)
for working with PCO cameras. It contains everything needed for camera setup, image acquistion,
readout and color conversion.

The high-level class architecture makes it very easy to integrate PCO cameras into your own
software, while still having access to the underlying pco.sdk and pco.recorder interface for a
detailed control of all possible functionalities.

- **Documentation**: `Manual <https://www.pco.de/fileadmin/user_upload/pco-manuals/MA_PCOPYTHON.pdf>`_
- **Website**: https://www.excelitas.com/de/product-category/pco
- **Support**: support.pco@excelitas.com

Installation
============
Install from pypi (recommended)::

    $ pip install pco

Basic Usage
===========
.. code-block:: python

    import matplotlib.pyplot as plt
    import pco

    with pco.Camera() as cam:

        cam.record(mode="sequence")
        image, meta = cam.image()

        plt.imshow(image, cmap='gray')
        plt.show()

.. image:: https://www.pco.de/fileadmin/user_upload/company/screen.png

Recorder Modes
==============
Depending on your workflow you can choose between different recording modes. 

Some modes are blocking, i.e. the ``record()`` function waits until recording is finished, some are non-blocking.
Some of them are storing the images in memory, the others directly as file(s) on the disk.
However, for the recorder modes which store the images as files,
accessing the recorded images is identical with the modes which store the images in memory.

.. list-table:: record modes
  :widths: 20 10 10 60
  :header-rows: 1

  * - Mode
    - Storage
    - Blocking
    - Description
  
  * - ``sequence``
    - Memory
    - yes
    - Record a sequence of images.
  
  * - ``sequence non blocking``
    - Memory
    - no 
    - Record a sequence of images, do not wait until record is finished.
  
  * - ``ring buffer``
    - Memory
    - no 
    - Continuously record images in a ringbuffer, once the buffer is full, old images are overwritten.
  
  * - ``fifo``
    - Memory
    - no 
    - Record images in fifo mode, i.e. you will always read images sequentially and once the buffer is full, recording will pause until older images have been read.
  
  * - ``sequence dpcore``
    - Memory
    - yes
    - Same as ``sequence``, but with DotPhoton preparation enabled.
  
  * - ``sequence non blocking dpcore``
    - Memory
    - no 
    - Same as ``sequence_non_blocking``, but with DotPhoton preparation enabled.
  
  * - ``ring buffer dpcore``
    - Memory
    - no 
    - Same as ``ring_buffer``, but with DotPhoton preparation enabled.
  
  * - ``fifo dpcore``
    - Memory
    - no 
    - Same as ``fifo``, but with DotPhoton preparation enabled.
  
  * - ``tif``
    - File  
    - no 
    - Record images directly as tif files.
  
  * - ``multitif``
    - File  
    - no 
    - Record images directly as one or more multitiff file(s).
  
  * - ``pcoraw``
    - File  
    - no 
    - Record images directly as one pcoraw file.
  
  * - ``dicom``
    - File  
    - no 
    - Record images directly as dicom files.
  
  * - ``multidicom``
    - File  
    - no 
    - Record images directly as one or more multi-dicom file(s).

Image Formats
=============
All image data is always transferred as 2D or 3D numpy array.
Besides the standard 16 bit raw image data you also have the possibility to get your images in different formats,
shown in the table below.

The format is selected when calling the ``image()`` / ``images()`` / ``image_average()`` functions of the Camera class. 
The image data is stored as numpy array, which enables you to work with it in the most pythonic way.

.. list-table:: image formats
  :widths: 30 70
  :header-rows: 1

  * - Format
    - Description
  
  * - ``Mono8,mono8``
    - Get image as 8 bit grayscale data.
  
  * - ``Mono16,mono16,raw16,bw16``
    - Get image as 16 bit grayscale/raw data.
  
  * - ``BGR8,bgr``
    - Get image as 24 bit color data in bgr format.
  
  * - ``RGB8,rgb``
    - Get image as 24 bit color data in rgb format.
  
  * - ``BGRA8,bgra8,bgra``
    - Get image as 32 bit color data (with alpha channel) in bgra format.
  
  * - ``RGBA8,rgba8,rgba``
    - Get image as 32 bit color data (with alpha channel) in rgba format.
  
  * - ``BGR16,bgr16``
    - Get image as 48 bit color data in bgr format (only possible for color cameras).
  
  * - ``RGB16,rgb16``
    - Get image as 48 bit color data in rgb format (only possible for color cameras).


Logging
=======

Logging is implemented according to the python logging package (https://docs.python.org/3/library/logging.html).
Supported logging levels are:

- `ERROR`
- `WARNING`
- `INFO`
- `DEBUG`

.. code-block:: python

    logger = logging.getLogger("pco")
    logger.setLevel(logging.INFO)
    logger.addHandler(pco.stream_handler)

.. code-block:: python

    ...
    [][sdk] get_camera_type: OK.
    ...
    [2019-11-25 15:54:15.317855 / 0.016 s] [][sdk] get_camera_type: OK.


Documentation (overview)
========================
The full Documentation can be found in the `manual <https://www.pco.de/fileadmin/user_upload/pco-manuals/MA_PCOPYTHON.pdf>`_

The pco.Camera class offers the following methods:

- ``__init()__`` Opens and initializes a camera with its default configuration.
- ``__exit()__`` Closes the camera and cleans up everything (e.g. end of with-statement).
- ``close()`` Closes the camera and cleans up everything.
- ``default_configuration()`` Set default configuration to the camera
- ``record()`` Initialize and start the recording of images.
- ``stop()`` Stop the current recording.
- ``wait_for_first_image()`` Wait until the first image has been recorded.
- ``wait_for_new_image()`` Wait until a new image has been recorded.
- ``get_convert_control()`` Get current color convert settings.
- ``set_convert_control()`` Set new color convert settings.
- ``load_lut()`` Set the lut file for the convert control setting.
- ``adapt_white_balance()`` Do a white-balance according to a transferred image.
- ``image()`` Read a recorded image as numpy array.
- ``images()`` Read a series of recorded images as a list of numpy arrays.
- ``image_average()`` Read an averaged image (averaged over all recorded images) as numpy array.

The pco.Camera class has the following properties:

- ``camera_name`` gets the camera name.
- ``camera_serial`` gets the serial number of the camera.
- ``is_recording`` gets a flag to indicate if the camera is currently recording.
- ``is_color`` gets a flag to indicate if the camera is a color camera.
- ``recorded_image_count`` gets the number of currently recorded images.
- ``configuration`` gets/sets the camera configuration.
- ``description`` gets the (static) camera description parameters.
- ``exposure_time`` gets/sets the exposure time (in seconds).
- ``delay_time`` gets/sets the delay time (in seconds).

The pco.Camera class holds the following objects:

- ``sdk`` offers direct access to all underlying functions of the pco.sdk.
- ``rec`` offers direct access to all underlying functions of the pco.recorder.
- ``conv`` offers direct access to all underlying functions of the pco.convert according to the selected image format.


.. |PyPI-Versions| image:: https://img.shields.io/pypi/pyversions/pco.svg
   :target: https://pypi.python.org/pypi/pco

.. |LICENCE| image:: https://img.shields.io/badge/License-MIT-green.svg
   :target: https://opensource.org/licenses/MIT

.. |Platform| image:: https://img.shields.io/badge/platform-win_x64%20%7C%20linux_x64-green.svg
   :target: https://pypi.python.org/pypi/pco
   
.. |PyPI-Status| image:: https://img.shields.io/pypi/v/pco.svg
  :target: https://pypi.python.org/pypi/pco


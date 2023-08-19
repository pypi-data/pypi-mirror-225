# pylibCZIrw - Python wrapper for libCZI

This project provides a simple and easy-to-use Python wrapper for [libCZI](https://github.com/ZEISS/libczi) - a cross-platform C++ library intended for providing read and write access to CZI image documents.

## Important Remarks

* At the moment, **pylibCZIrw** completely abstracts away the subblock concept, both in the reading and in the writing APIs.
* If pylibCZIrw is extended in the future to support subblock-based access (e.g. accessing acquisition tiles), this API must not be altered.
* The core concept of pylibCZIrw is focussing on reading and writing 2D image planes by specifying the dimension indices and its location in order to only read or write **what is really needed**.

## Example Usage

The basic usage can be inferred from this sample notebook:  

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zeiss-microscopy/OAD/blob/master/jupyter_notebooks/pylibCZIrw/pylibCZIrw_3_3_0.ipynb)  

For more detailed information refer to the pylibCZIrw-documentation.html shipped with the source distribution of this package (see the **Download files** section).  

## Installation
In case there is no wheel available for your system configuration, you can:  
- try to install from the provided source distribution  
  **For Windows**:
  - try to [keep paths short on systems with maximum path lengths](https://github.com/pypa/pip/issues/3055)
  - make [Win10 accept file paths over 260 characters](https://www.howtogeek.com/266621/how-to-make-windows-10-accept-file-paths-over-260-characters/)
- reach out to the maintainers of this project to add more wheels

## Disclaimer

The library and the notebook are free to use for everybody. Carl Zeiss Microscopy GmbH undertakes no warranty concerning the use of those tools. Use them at your own risk.

**By using any of those examples you agree to this disclaimer.**

Version: 2022.04.06

Copyright (c) 2023 Carl Zeiss AG, Germany. All Rights Reserved.

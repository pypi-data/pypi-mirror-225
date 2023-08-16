# code: utf-8
# author: Pierre-Luc Asselin

"""
Contains a variety of utilitary functions
using dicom_sr_builder features.
"""

import logging
import os
from typing import Union

import pydicom

_logger = logging.getLogger(__name__)


def read_dicom(file_or_ds: Union[str, pydicom.FileDataset]) -> pydicom.FileDataset:
    """Takes a filepath or pydicom.FileDataset et always returns a pydicom.FileDataset"""
    if isinstance(file_or_ds, pydicom.FileDataset):
        return file_or_ds

    if isinstance(file_or_ds, str):
        if os.path.isfile(file_or_ds):
            return pydicom.dcmread(file_or_ds)

    raise ValueError('file_or_ds is nether a pydicom.FileDataset object or a dicom file path')

"""Utility submodule to make SR"""
from typing import Union

import pydicom

from . import utils
from .builder import SRBuilder
from .terminologies import dicom_terminologies


def make_sr(
        content_sequence: dict,
        dicom_to_refer: Union[
            str, pydicom.FileDataset,
            list[Union[str, pydicom.FileDataset]]
        ] = None,
        purpose_of_reference_code: Union[dict, list[dict]] = None) -> pydicom.FileDataset:
    """Creates a DICOM SR object

    Args:
        content_sequence: Content sequence, ex.
            {'ValueType': ...,
             'Value': 'some text', 'ConceptNameCodeSequence': {
                'CodeValue': '1233',
                'CodeMeaning': 'Test',
                'CodingSchemeDesignator': 'DCM',
            },
            'SomeOtherTag' : 'Some additionnal information'}
        dicom_to_refer: File path or pydicom.FileDataset object or list of those objects of
            the source DICOM file to use to assemble the DICOMSR object
        purpose_of_reference_code: Dictionary or list of directory with information tags on
            why the target file is used to generate the DICOM SR. For example:
            {
               "CodeValue": "SEG",
               "CodeMeaning": "Segmentation",
               "CodingSchemeDesignator": "DCM",
            }

    Returns:
        A DICOM SR object (pydicom.FileDataset)
    """
    if dicom_to_refer is not None and purpose_of_reference_code is None:
        # If the dicom_to_refer is not None, the purpose_of_reference_code has to be provided.
        # If not provided, use the default

        # Ensure that dicom_to_refer is a list
        if not isinstance(dicom_to_refer, list):
            dicom_to_refer = [dicom_to_refer]

        # Ensure that dicom_to_refer are pydicom.FileDataset
        dicom_to_refer = [utils.read_dicom(dicom) for dicom in dicom_to_refer]

        purpose_of_reference_code = _make_default_purpose_of_reference_codes(dicom_to_refer)

    # Building DICOM SR file based on the study
    sr_builder = SRBuilder(
        dicom_to_refer=dicom_to_refer,
        purpose_of_reference_code=purpose_of_reference_code
    )

    # Adding content_sequence, populating DICOM SR file an extracting
    sr_builder.add_content_sequence(content_sequence)
    sr_builder.build()

    finalize_dicom_sr = sr_builder.dicom_sr

    # Returning the DiCOM SR File in DICOM format
    return finalize_dicom_sr


def make_sr_from_text(
        text: str,
        dicom_to_refer: [
            str, pydicom.FileDataset,
            list[Union[str, pydicom.FileDataset]]
        ] = None,
        purpose_of_reference_code: Union[dict, list[dict]] = None) -> pydicom.FileDataset:
    """Create a DICOM SR file containing the text given in parameter.

    Args:
        text: string of the text to add
        dicom_to_refer: File path or pydicom.FileDataset object or list of those objects of
            the source DICOM file to use to assemble the DICOMSR object
        purpose_of_reference_code: Dictionary or list of directory with information tags on
            why the target file is used to generate the DICOM SR. For example:
            {
               "CodeValue": "SEG",
               "CodeMeaning": "Segmentation",
               "CodingSchemeDesignator": "DCM",
            }

    Returns:
        A DICOM SR object (pydicom.FileDataset)
    """
    content_sequence = {
        "ValueType": "CONTAINER",
        "ConceptNameCodeSequence": {
            "CodeValue": "DOC",
            "CodeMeaning": "Document",
            "CodingSchemeDesignator": "DCM",
        },
        "ContinuityOfContent": "SEPARATE",
        "Value": [
            {
                "RelationshipType": "HAS PROPERTIES",
                "ValueType": "TEXT",
                "ConceptNameCodeSequence": {
                    "CodeValue": "113012",
                    "CodeMeaning": "Key Object Description",
                    "CodingSchemeDesignator": "DCM",
                },
                "Value": text,
            }
        ],
    }

    return make_sr(
        content_sequence=content_sequence,
        dicom_to_refer=dicom_to_refer,
        purpose_of_reference_code=purpose_of_reference_code
    )


def _make_default_purpose_of_reference_codes(
        dicoms_to_refer: list[pydicom.FileDataset]) -> list[dict]:
    purpose_of_reference_code = []

    for dicom in dicoms_to_refer:
        purpose_of_reference_code.append({
            'CodeValue': dicom.Modality,
            'CodeMeaning': dicom_terminologies.find_code_meaning(dicom.Modality),
            'CodingSchemeDesignator': 'DCM',
        })

    return purpose_of_reference_code

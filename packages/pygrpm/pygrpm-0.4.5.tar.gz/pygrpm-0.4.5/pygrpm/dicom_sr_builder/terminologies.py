"""Terminologies sub module"""
# pylint: disable=W0707
import os

import pandas

DATA_DIRECTORY = f'{os.path.dirname(os.path.realpath(__file__))}/data'
DICOM_TERMINOLOGIES_PATH = f'{DATA_DIRECTORY}/DCM_2023c_20230704.csv'


class DicomTerminologies:
    """This class is a singleton that load the DICOM terminologies a single time

    The terminologies can be found at : https://bioportal.bioontology.org/ontologies/DCM
    """

    def __init__(self, terminologies_path: str):
        self.terminologies_path = terminologies_path
        self._terminologies = None

    @property
    def terminologies(self) -> pandas.DataFrame:
        """DCM Terminologies, instantiated only once"""
        if self._terminologies is None:
            self._terminologies = pandas.read_csv(self.terminologies_path)

        return self._terminologies

    def find_code_meaning(self, notation: str) -> str:
        """Find the code meaning from notation code"""
        try:
            return self.terminologies[
                self.terminologies['notation'] == notation
            ]['preferred label'].iloc[0]
        except IndexError:
            raise ValueError(f'Notation "{notation}" not found in DICOM terminologies')


dicom_terminologies = DicomTerminologies(DICOM_TERMINOLOGIES_PATH)

#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from enum import Enum

__all__ = [
    "ModelTypes",
    "DecodingMethods",
]


class ModelTypes(Enum):
    """Supported foundation models."""
    FLAN_T5_XXL = "google/flan-t5-xxl"
    FLAN_UL2 = "google/flan-ul2"
    MT0_XXL = "bigscience/mt0-xxl"
    GPT_NEOX = 'eleutherai/gpt-neox-20b'
    MPT_7B_INSTRUCT2 = 'ibm/mpt-7b-instruct2'


class DecodingMethods(Enum):
    """Supported decoding methods for text generation."""
    SAMPLE = "sample"
    GREEDY = "greedy"

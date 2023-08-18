from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSoundEncoding(Enum):
    """
    <summary>
        The encoding format for the sample data.
    </summary>
    """
    Raw = 0
    Signed = 1
    MuLaw = 2
    ALaw = 3


from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class PdfSoundChannels(Enum):
    """
    <summary>
        The number of sound channels.
    </summary>
    """
    Mono = 1
    Stereo = 2


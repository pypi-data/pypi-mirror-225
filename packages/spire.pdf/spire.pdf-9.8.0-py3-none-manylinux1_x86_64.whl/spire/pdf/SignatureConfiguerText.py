from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class SignatureConfiguerText(Enum):
    """
    <summary>
        Configuer Text,Show Sign content
    </summary>
    """
    Name = 1
    Location = 2
    DistinguishedName = 4
    Logo = 8
    Date = 16
    Reason = 32
    ContactInfo = 64
    Labels = 128


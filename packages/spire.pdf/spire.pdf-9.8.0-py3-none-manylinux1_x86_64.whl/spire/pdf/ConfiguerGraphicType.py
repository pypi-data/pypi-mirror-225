from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class ConfiguerGraphicType(Enum):
    """
    <summary>
        Signture Configuer Graphic type
    </summary>
    """
    No = 0
    Picture = 1
    Text = 2
    PictureSignInformation = 3
    TextSignInformation = 4
    SignInformationPicture = 5


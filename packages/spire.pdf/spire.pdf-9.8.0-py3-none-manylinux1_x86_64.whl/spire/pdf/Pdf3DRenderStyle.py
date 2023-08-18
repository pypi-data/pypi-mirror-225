from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class Pdf3DRenderStyle(Enum):
    """
    <summary>
        Specifies the available rendering style of the 3D artwork. 
    </summary>
    """
    Solid = 0
    SolidWireframe = 1
    Transparent = 2
    TransparentWireframe = 3
    BoundingBox = 4
    TransparentBoundingBox = 5
    TransparentBoundingBoxOutline = 6
    Wireframe = 7
    ShadedWireframe = 8
    HiddenWireframe = 9
    Vertices = 10
    ShadedVertices = 11
    Illustration = 12
    SolidOutline = 13
    ShadedIllustration = 14


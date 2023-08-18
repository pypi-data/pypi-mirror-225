from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class IPdfSignatureAppearance (abc.ABC) :
    """
    <summary>
        Provide a custom signature appearance interface
    </summary>
    """

    @abc.abstractmethod
    def Generate(self ,g:'PdfCanvas'):
        """
    <summary>
        Generate custom signature appearance by a graphics context.
    </summary>
    <param name="g">A graphics context of signature appearance.</param>
        """
        pass



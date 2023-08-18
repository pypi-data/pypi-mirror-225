from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class ITSAService (abc.ABC) :
    """
    <summary>
        Timestamp provider interface.
    </summary>
    """
#
#    @abc.abstractmethod
#    def Generate(self ,signature:'Byte[]')->List['Byte']:
#        """
#    <summary>
#        Generate timestamp token.
#    </summary>
#    <param name="signature">
#            The value of signature field within SignerInfo.
#            The value of messageImprint field within TimeStampToken shall be the hash of signature.
#            Refrence RFC 3161 APPENDIX A.
#    </param>
#    <returns>timestamp which must conform to RFC 3161</returns>
#        """
#        pass
#



from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class IUofCompressAdapter (abc.ABC) :
    """
    <summary>
        interface for compression adapter
    </summary>
<author>linwei</author>
    """
    @abc.abstractmethod
    def Transform(self)->bool:
        """
    <summary>
        compress or decompress
    </summary>
    <returns>true if succeeded</returns>
    <returns>false if failed</returns>
<exception cref="T:System.Exception">exceptions happen</exception>
        """
        pass


    @property

    @abc.abstractmethod
    def InputFilename(self)->str:
        """
    <summary>
        input file name
    </summary>
        """
        pass


    @InputFilename.setter
    @abc.abstractmethod
    def InputFilename(self, value:str):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def OutputFilename(self)->str:
        """
    <summary>
        output file name
    </summary>
        """
        pass


    @OutputFilename.setter
    @abc.abstractmethod
    def OutputFilename(self, value:str):
        """

        """
        pass



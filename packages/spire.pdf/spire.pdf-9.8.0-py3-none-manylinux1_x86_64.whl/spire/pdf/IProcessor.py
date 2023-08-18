from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class IProcessor (abc.ABC) :
    """
    <summary>
        This is the interface of pre and post processors
    </summary>
<author>linwei</author>
    """
    @abc.abstractmethod
    def transform(self)->bool:
        """

        """
        pass


    @property

    @abc.abstractmethod
    def InputFilename(self)->str:
        """

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

        """
        pass


    @OutputFilename.setter
    @abc.abstractmethod
    def OutputFilename(self, value:str):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def OriginalFilename(self)->str:
        """

        """
        pass


    @OriginalFilename.setter
    @abc.abstractmethod
    def OriginalFilename(self, value:str):
        """

        """
        pass


    @property

    @abc.abstractmethod
    def ResourceDir(self)->str:
        """

        """
        pass


    @ResourceDir.setter
    @abc.abstractmethod
    def ResourceDir(self, value:str):
        """

        """
        pass



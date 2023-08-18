from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class IUOFTranslator (abc.ABC) :
    """
    <summary>
        This interface defines the exposed interface of Translator
    </summary>
<author>linwei</author>
    """
#
#    @abc.abstractmethod
#    def AddProgressMessageListener(self ,listener:'EventHandler'):
#        """
#
#        """
#        pass
#


#
#    @abc.abstractmethod
#    def AddFeedbackMessageListener(self ,listener:'EventHandler'):
#        """
#
#        """
#        pass
#



    @abc.abstractmethod
    def UofToOox(self ,inputStream:'Stream',outputStream:'Stream'):
        """

        """
        pass



    @abc.abstractmethod
    def OoxToUof(self ,inputStream:'Stream',outputStream:'Stream'):
        """

        """
        pass



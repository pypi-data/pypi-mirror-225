from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.pdf.common import *
from spire.pdf import *
from ctypes import *
import abc

class ImgData (abc.ABC) :
    """

    """
    @property
    @abc.abstractmethod
    def TileWidth(self)->int:
        """

        """
        pass


    @property
    @abc.abstractmethod
    def TileHeight(self)->int:
        """

        """
        pass


    @property
    @abc.abstractmethod
    def NomTileWidth(self)->int:
        """

        """
        pass


    @property
    @abc.abstractmethod
    def NomTileHeight(self)->int:
        """

        """
        pass


    @property
    @abc.abstractmethod
    def ImgWidth(self)->int:
        """

        """
        pass


    @property
    @abc.abstractmethod
    def ImgHeight(self)->int:
        """

        """
        pass


    @property
    @abc.abstractmethod
    def NumComps(self)->int:
        """

        """
        pass


    @property
    @abc.abstractmethod
    def TileIdx(self)->int:
        """

        """
        pass


    @property
    @abc.abstractmethod
    def TilePartULX(self)->int:
        """

        """
        pass


    @property
    @abc.abstractmethod
    def TilePartULY(self)->int:
        """

        """
        pass


    @property
    @abc.abstractmethod
    def ImgULX(self)->int:
        """

        """
        pass


    @property
    @abc.abstractmethod
    def ImgULY(self)->int:
        """

        """
        pass



    @abc.abstractmethod
    def getCompSubsX(self ,c:int)->int:
        """

        """
        pass



    @abc.abstractmethod
    def getCompSubsY(self ,c:int)->int:
        """

        """
        pass



    @abc.abstractmethod
    def getTileCompWidth(self ,t:int,c:int)->int:
        """

        """
        pass



    @abc.abstractmethod
    def getTileCompHeight(self ,t:int,c:int)->int:
        """

        """
        pass



    @abc.abstractmethod
    def getCompImgWidth(self ,c:int)->int:
        """

        """
        pass



    @abc.abstractmethod
    def getCompImgHeight(self ,c:int)->int:
        """

        """
        pass



    @abc.abstractmethod
    def getNomRangeBits(self ,c:int)->int:
        """

        """
        pass



    @abc.abstractmethod
    def setTile(self ,x:int,y:int):
        """

        """
        pass


    @abc.abstractmethod
    def nextTile(self):
        """

        """
        pass



    @abc.abstractmethod
    def getTile(self ,co:'Coord')->'Coord':
        """

        """
        pass



    @abc.abstractmethod
    def getCompULX(self ,c:int)->int:
        """

        """
        pass



    @abc.abstractmethod
    def getCompULY(self ,c:int)->int:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def getNumTiles(self ,co:Coord)->Coord:
        """

        """
        pass


    @dispatch
    @abc.abstractmethod
    def getNumTiles(self)->int:
        """

        """
        pass



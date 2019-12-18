import logging
import abc
from enum import Enum

logger = logging.getLogger("wkt.WKT")
 

class WKT(object):
    __metaclass__  = abc.ABCMeta

    def __init__(self, geogcsName, datumName, sphereoidName, radius, inverseFlattening, authorityName, authorityCode):
        """
        Creates a new WKT

        :param geogcsName: the CRS name
        :param datumName: the datum name
        :param sphereoidName: the spheroid name
        :param radius: the radius in meter
        :param inverseFlattening: the inverseFlattening or 0 for a sphere
        :param authorityName: the authority name that is responsible of defining this kiond of CRS
        :param authorityCode: the authority code that identifies this CRS in the authority name namespace
        :type geogcsName: str
        :type datumName: str
        :type sphereoidName: str
        :type radius: float
        :type inverseFlattening: float
        :type authorityName: str
        :type authorityCode: str

        .. seealso:: setLongitudeAxis(), setProjection()
        """

        logger.debug("Entering in WKT constructor with geogcsName=%s, datumName=%s, sphereoidName=%s, radius=%s, "
                     "inverseFlattening=%s, authorityName=%s, authorityCode=%s" % (
                         geogcsName, datumName, sphereoidName, radius, inverseFlattening, authorityName, authorityCode
                     ))
        assert isinstance(geogcsName, str), "WKT.__init__: geogcsName must be a string for geogcsName=%s" % geogcsName
        assert isinstance(datumName, str), "WKT.__init__: datumName must be a string for geogcsName=%s" % geogcsName
        assert isinstance(sphereoidName,
                          str), "WKT.__init__: sphereoidName must be a string for geogcsName=%s" % geogcsName
        assert isinstance(radius,
                          (int, float)), "WKT.__init__: radius must be an int ot float for geogcsName=%s" % geogcsName
        assert radius > 0, "WKT.__init__: radius=%s, it must be > 0 for geogcsName=%s" % (radius, geogcsName)
        assert isinstance(inverseFlattening, (
            float, int)), "WKT.__init__: inverseFlattening must be a string for geogcsName=%s" % geogcsName

        #assert inverseFlattening >= 0, "WKT.__init__: inverseFlattening=%s, it must be >=0 for geogcsName=%s" % (
        #    inverseFlattening, geogcsName
        #)

        assert isinstance(authorityName,
                          str), "WKT.__init__: authorityName must be a string for geogcsName=%s" % geogcsName
        assert isinstance(authorityCode,
                          str), "WKT.__init__: authorityCode must be a string for geogcsName=%s" % geogcsName

        self.__geogcsName = geogcsName
        self.__datumName = datumName
        self.__sphereoidName = sphereoidName
        self.__radius = radius
        self.__semiMinorRadius = None
        self.__inverseFlattening = inverseFlattening
        self.__authorityName = authorityName
        self.__authorityCode = authorityCode
        logger.debug("Exiting from WKT constructor")

    class LongitudeAxis(Enum):
        """Enumerated class to show if the longitude is counted positively to West/East"""
        WEST = "west"
        EAST = "east"

    class Rotation(Enum):
        DIRECT = "Direct"
        RETROGRADE = "Retrograde"

    class CRS(Enum):
        OCENTRIC = "Ocentric"
        OGRAPHIC = "Ographic"
        PROJECTED_OCENTRIC = "Projected ocentric"
        PROJECTED_OGRAPHIC = "Projected ographic"

    def getGeoGcsName(self):
        """
        Returns the geogcsName
        :return: the geogcsName
        :rtype: str
        """
        return self.__geogcsName

    def getDatumName(self):
        """
        Returns the datumName
        :return: the datumName
        :rtype: str
        """
        return self.__datumName

    def getSpheroidName(self):
        """
        Returns the spheroidName
        :return: the spheroidName
        :rtype: str
        """
        return self.__sphereoidName

    def getRadius(self):
        """
        Returns the radius of the spheroid in meter
        :return: the radius
        :rtype: float
        """
        return self.__radius

    def getInverseFlattening(self):
        """
        Returns the inverse flattening of the spheroid.

        0 means we have a sphere
        :return: the inverse flattening of the spheroid
        :rtype: float
        """
        return self.__inverseFlattening

    def getAuthorityName(self):
        """
        Returns the authority name of the spheroid
        :return: the authority name
        :rtype: str
        """
        return self.__authorityName

    def getAuthorityCode(self):
        """
        Returns the authority code of the spheroid
        :return: the authority code
        :rtype: str
        """
        return self.__authorityCode

    def setSemiMinorAxisForOcentric(self, theC):
        """
        One way to approximate ocentric latitudes on an elliptical body is to define the body as a sphere.
        For equatorial projections we would simply use the semi-major as a sphere and for polar projections we would use
        the semi-minor radius as a sphere. This is the current method for GDAL to translate a PDS/ISIS3 ocentric
        elliptical body to say a GeoTiff.

        :param theC: semi-major radius in meter
        :type theC: float
        """
        self.__semiMinorRadius = theC

    @staticmethod
    def getLongitudeOrderFromRotation(rotation) :
        """
        Returns the longitude order according to the rotation in ographic case without exception
        :param rotation: str
        :type rotation: str 
        :return: the order (EAST, WEST)
        :rtype: LongitudeAxis       
        """
        if rotation == WKT.Rotation.DIRECT.value:
            result = WKT.LongitudeAxis.WEST
        elif rotation == WKT.Rotation.RETROGRADE.value:
            result = WKT.LongitudeAxis.EAST
        else:
            raise Exception("Unexpected value for rotation : "+rotation)
        return result

    @abc.abstractmethod
    def getWKT(self):
        """
        Returns the WKT

        :return: the WKT
        :rtype: str

        :Example: WKT based on a CRS longitude/latitude
        >>> wkt = WKT("unnamed ellipse","unknown","unnamed",60000,12,"unnamed authority","unnamed code")
        >>> wkt.getWkt()
        'GEOGCS["unnamed ellipse",DATUM["unknown",SPHEROID["unnamed",60000,12]],PRIMEM["Reference_Meridian",0.0],UNIT["Degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["unnamed authority","unnamed code"]]'


        :Example: WKT based on a projectedCRS
        >>> wkt = WKT("unnamed ellipse","unknown","unnamed",60000,12,"unnamed authority","unnamed code")
        >>> wkt.setProjection("unnamed projection", WKT.Projection.EQUIRECTANGULAR_0,"unnamed authority proj","unnamed authority code proj")
        >>> wkt.getWkt()
        'PROJCS["unnamed projection",GEOGCS["unnamed ellipse",DATUM["unknown",SPHEROID["unnamed",60000,12]],PRIMEM["Reference_Meridian",0.0],UNIT["Degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["unnamed authority","unnamed code"]],PROJECTION["Equirectangular"],PARAMETER["False_Easting",0],PARAMETER["Standard_Parallel_1",0],PARAMETER["Central_Meridian",180],PARAMETER["False_Northing",0],UNIT["Meter",1, AUTHORITY["EPSG","9001"]],AUTHORITY["unnamed authority proj","unnamed authority code proj"]]'
        """
        raise NotImplementedError

    @abc.abstractmethod
    def getRecord(self):
        raise NotImplementedError    

    @staticmethod
    def computeInverseFlattening(semiMajorAxis, semiMinorAxis):
        """
        Compute the inverse flattening
        :param semiMajorAxis: semi-major axis
        :param semiMinorAxis: semi-minor axis
        :type semiMajorAxis:str
        :type semiMinorAxis:str
        :rtype: float
        """
        flattening = ((float(semiMajorAxis) - float(semiMinorAxis)) / float(semiMajorAxis))
        if WKT.isDifferent(flattening, 0):
            flattening = 1.0 / flattening
        return flattening

    @staticmethod
    def isEqual(number1, number2, allowed_error=1e-9):        
        """ Returns True when number1=number2 otherwide False

        :param number1: number to test
        :param number2: number to test
        :param allowed_error: the error for which the numbers are equals
        :return: True when number1=number2 otherwide False
        :type number1: float
        :type number2: float
        :type allowed_error: float
        :rtype: bool
        """

        logger.debug(
            "Entering in isEqual with number1=%s number2=%s allowed_error=%s" % (number1, number2, allowed_error))

        assert isinstance(number1, (int, float)), "WKT.isEqual: %s must be a float or int" % number1
        assert isinstance(number2, (int, float)), "WKT.isEqual: %s must be a float or int" % number2
        assert isinstance(allowed_error, (int, float)), "WKT.isEqual: %s must be a float or int" % allowed_error
        result = abs(number1 - number2) <= allowed_error

        logger.debug("Exiting from isEqual with %s" % result)
        return result

    @staticmethod
    def isDifferent(number1, number2, allowed_error=1e-9):
        """
        Returns True when number1<>number2 otherwise False

        :param number1: number to test
        :param number2: number to test
        :param allowed_error: the error for which the two numbers are equals
        :return: True when number1<>number2 otherwise False
        :type number1: float
        :type number2: float
        :type allowed_error: float
        :rtype: bool
        """
        return not WKT.isEqual(number1, number2, allowed_error)    

    @staticmethod
    def isTriaxial(a, b, c):
        """
        Returns True when the body is triaxial otherwise False

        :param a: semi-major axis
        :param b: semi-minor axis
        :param c: axis b
        :type a: float
        :type b: float
        :type c: foat
        :rtype: bool
        """
        return WKT.isDifferent(a, b) and WKT.isDifferent(a, c)      


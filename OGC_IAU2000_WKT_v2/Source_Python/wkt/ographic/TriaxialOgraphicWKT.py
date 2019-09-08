import logging
from ..WKT import WKT
from enum import Enum

logger = logging.getLogger("wkt.triaxialOgraphicWKT")

class TriaxialOgraphicMetadata(Enum):    
    GEO_GCS_NAME = "geogcsName"
    DATUM_NAME = "datumName"
    ELLIPSOIDE_NAME = "ellpsoideName"
    SEMI_MAJOR = "semiMajor"
    SEMI_MINOR = "semiMinor"
    AXIS_B = "axisb"
    AUTHORITY_NAME = "authorityName"
    AUTHORITY_CODE = "authorityCode"
    LONGITUDE_ORDER = "longitudeOrder"
    CITATION = "citation"

class TriaxialOgraphicWKT(WKT):
    """
    Constructs a new WKT that describes an ographic CRS with a triaxial datum

    The WKT describing an ographic CRS with an ellipsoid datum is displayed as follow:
    GEOGCRS["<geogcsName>",
        DATUM["<datumName>",
            TRIAXIAL["<ellipsoidName>",<semi-major>,<semi-median>,<semi-minor>,
                    LENGTHUNIT["metre", 1.0, ID["EPSG", 9001]]
            ]
        ],
        PRIMEM["Reference_Meridian",0.0],
        CS[spherical,3],
        AXIS["lat", north, ORDER[1]],
        AXIS["long", <direction>, ORDER[2]],
        ANGLEUNIT["Degree",0.0174532925199433,
            AUTHORITY["EPSG","9122"]
        ],           
        AUTHORITY["<authorityName>","<authorityCode>"],
        REMARK[<citation>]"
    ] 

    Constants
    ---------
    GEOGCRS_TRIAXIAL: WKT template for a ographic CRS based on longitude/latitude and a triaxial body   

    """
    GEOGCRS_TRIAXIAL = "GEOGCRS[\"%s\"," \
             "DATUM[\"%s\"," \
             "TRIAXIAL[\"%s\", %r, %r, %r, LENGTHUNIT[\"metre\", 1.0, ID[\"EPSG\", 9001]]]," \
             "]," \
             "PRIMEM[\"Reference_Meridian\", 0.0]," \
             "CS[ellipsoidal,2]," \
             "AXIS[\"lat\", north, ORDER[1]]," \
             "AXIS[\"long\", \"%s\", ORDER[2]]," \
             "ANGLEUNIT[\"Degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]]," \
             "AUTHORITY[\"%s\",\"%s\"]," \
             "REMARK[\"IAU report 2015 : doi://10.1007/s10569-017-9805-5\"]" \
             "]"     

    def __init__(self, tgr):
        """
        :param tgr: Planetary triaxial ographic metadata
        :type tgr: WKTRecord
        """
        logger.debug("Entering in triaxialOgraphicWKT constructor")     

        super(TriaxialOgraphicWKT, self).__init__(
            tgr.getElement(TriaxialOgraphicMetadata.GEO_GCS_NAME),
            tgr.getElement(TriaxialOgraphicMetadata.DATUM_NAME),
            tgr.getElement(TriaxialOgraphicMetadata.ELLIPSOIDE_NAME),
            1.0,
            0.0,
            tgr.getElement(TriaxialOgraphicMetadata.AUTHORITY_NAME),
            tgr.getElement(TriaxialOgraphicMetadata.AUTHORITY_CODE)
        )

        assert tgr.getElement(TriaxialOgraphicMetadata.LONGITUDE_ORDER) == WKT.LongitudeAxis.WEST or tgr.getElement(TriaxialOgraphicMetadata.LONGITUDE_ORDER) == WKT.LongitudeAxis.EAST
        self.__longitudeAxisOrder = tgr.getElement(TriaxialOgraphicMetadata.LONGITUDE_ORDER)  
        self.__majorAxis = tgr.getElement(TriaxialOgraphicMetadata.SEMI_MAJOR)
        self.__minorAxis = tgr.getElement(TriaxialOgraphicMetadata.SEMI_MINOR)
        self.__axisB = tgr.getElement(TriaxialOgraphicMetadata.AXIS_B)
        logger.debug("Exiting from triaxialOgraphicWKT constructor")     


    def getWKT(self):
        """
        Returns the CRS based on longitude/latitude

        :return: the WKT
        :rtype: str
         """
        logger.debug("Entering in triaxialOgraphicWKT.getWkt")

        # building WKT string
        wkt = TriaxialOgraphicWKT.GEOGCRS_TRIAXIAL % (
            self.getGeoGcsName(), self.getDatumName(), self.getSpheroidName(), self.__majorAxis, self.__axisB, self.__minorAxis,
            self.__longitudeAxisOrder.value, self.getAuthorityName(), self.getAuthorityCode()
        )

        logger.debug("Exiting from triaxialOgraphicWKT.getWkt")
        return wkt          

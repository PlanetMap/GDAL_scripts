import logging
from ..WKT import WKT
from enum import Enum

logger = logging.getLogger("wkt.ographicWKT")

class OgraphicMetadata(Enum):
    GEO_GCS_NAME = "geogcsName"
    DATUM_NAME = "datumName"
    ELLIPSOIDE_NAME = "ellpsoideName"
    RADIUS = "radius"
    INVERSE_FLATTENING = "inverseFlattening"
    AUTHORITY_NAME = "authorityName"
    AUTHORITY_CODE = "authorityCode"
    LONGITUDE_ORDER = "longitudeOrder"
    CITATION = "citation" 


class OgraphicWKT(WKT) :
    """
    Class that allows to build a simple WKT.

    Constants
    ---------
    GEOGCRS: WKT template for a ographic CRS based on longitude/latitude

    """
    GEOGCRS = "GEOGCRS[\"%s\"," \
             "DATUM[\"%s\"," \
             "ELLIPSOID[\"%s\", %r, %r, LENGTHUNIT[\"metre\", 1.0, ID[\"EPSG\", 9001]]]," \
             "]," \
             "PRIMEM[\"Reference_Meridian\", 0.0]," \
             "CS[ellipsoidal,2]," \
             "AXIS[\"lat\", north, ORDER[1]]," \
             "AXIS[\"long\", %s, ORDER[2]]," \
             "ANGLEUNIT[\"Degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]]," \
             "AUTHORITY[\"%s\",\"%s\"]," \
             "REMARK[\"IAU report 2015 : doi://10.1007/s10569-017-9805-5\"]" \
             "]"     
    def __init__(self, pgr):
        """
        Constructs a new WKT that describes an ographic CRS with an ellipsoid datum

        The WKT describing an ographic CRS with an ellipsoid datum is displayed as follow:
        GEOGCRS["<geogcsName>",
            DATUM["<datumName>",
                ELLIPSOID["<ellipsoidName>",<radius>,<inverseFlattening>,
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

        :param pgr: Planetary ographic metadata
        :type pgr: WKTRecord

        """    
        logger.debug("Entering in ographicWKT constructor") 
        super(OgraphicWKT, self).__init__(
            pgr.getElement(OgraphicMetadata.GEO_GCS_NAME),
            pgr.getElement(OgraphicMetadata.DATUM_NAME),
            pgr.getElement(OgraphicMetadata.ELLIPSOIDE_NAME),
            pgr.getElement(OgraphicMetadata.RADIUS),
            pgr.getElement(OgraphicMetadata.INVERSE_FLATTENING),
            pgr.getElement(OgraphicMetadata.AUTHORITY_NAME),
            pgr.getElement(OgraphicMetadata.AUTHORITY_CODE)
        )
        assert pgr.getElement(OgraphicMetadata.LONGITUDE_ORDER) == WKT.LongitudeAxis.WEST or pgr.getElement(OgraphicMetadata.LONGITUDE_ORDER) == WKT.LongitudeAxis.EAST, "Wrong value for %s=%s"%(OgraphicMetadata.LONGITUDE_ORDER,pgr.getElement(OgraphicMetadata.LONGITUDE_ORDER))

        self.__longitudeAxisOrder = pgr.getElement(OgraphicMetadata.LONGITUDE_ORDER)  
        logger.debug("Exiting from ographicWKT constructor")     


    def getWKT(self):
        """
        Returns the CRS based on longitude/latitude

        :return: the WKT
        :rtype: str
         """
        logger.debug("Entering in ographicWKT.getWkt")

        # building WKT string
        wkt = OgraphicWKT.GEOGCRS % (
            self.getGeoGcsName(), self.getDatumName(), self.getSpheroidName(), self.getRadius(), self.getInverseFlattening(),
            self.__longitudeAxisOrder.value, self.getAuthorityName(), self.getAuthorityCode()
        )

        logger.debug("Exiting from ographicWKT.getWkt")
        return wkt   

    def getRecord(self):
        """
        Returns the record format 

        :return: the WKT
        :rtype: str
         """
        logger.debug("Entering in ocentricWKT.getRecord")


        record = {
            'type':'OGRAPHIC',
            OgraphicMetadata.GEO_GCS_NAME.value: self.getGeoGcsName(),
            OgraphicMetadata.DATUM_NAME.value: self.getDatumName(),
            OgraphicMetadata.ELLIPSOIDE_NAME.value: self.getSpheroidName(),
            OgraphicMetadata.RADIUS.value: self.getRadius(),
            OgraphicMetadata.INVERSE_FLATTENING.value: self.getInverseFlattening(),
            OgraphicMetadata.AUTHORITY_NAME.value: self.getAuthorityName(),
            OgraphicMetadata.AUTHORITY_CODE.value: self.getAuthorityCode(),  
            OgraphicMetadata.LONGITUDE_ORDER.value: self.__longitudeAxisOrder.value
        }

        logger.debug("Exiting from ocentricWKT.getRecord")
        return record              
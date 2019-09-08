import logging
from ..WKT import WKT
from enum import Enum

logger = logging.getLogger("wkt.ocentricWKT")

class OcentricMetadata(Enum):
    GEO_GCS_NAME = "geogcsName"
    DATUM_NAME = "datumName"
    ELLIPSOIDE_NAME = "ellpsoideName"
    RADIUS = "radius"
    INVERSE_FLATTENING = "inverseFlattening"
    AUTHORITY_NAME = "authorityName"
    AUTHORITY_CODE = "authorityCode"
    CITATION = "citation"    


class OcentricWKT(WKT) :
    """
    Class that allows to build an ocentric WKT with an ellipsoid datum.

    The WKT describing an ocentric CRS with an ellipsoid datum is displayed as follow:
    GEODCRS["<geogcsName>",
        DATUM["<datumName>",
            ELLIPSOID["<ellipsoidName>",<radius>,<inverseFlattening>,
                    LENGTHUNIT["metre", 1.0, ID["EPSG", 9001]]
            ]
        ],
        PRIMEM["Reference_Meridian",0.0],
        CS[spherical,3],
        AXIS["lat", north, ORDER[1]],
        AXIS["long", east, ORDER[2]],
        AXIS["distance (r)", <radius>, ORDER[3],LENGTHUNIT["meter",1000]],           
        ANGLEUNIT["Degree",0.0174532925199433,
            AUTHORITY["EPSG","9122"]
        ],             
        AUTHORITY["<authorityName>","<authorityCode>"],
        REMARK[<citation>]"
    ]    

    Constants
    ---------
    GEODCRS: WKT template for a ocentric CRS based on longitude/latitude

    """
    GEODCRS = "GEODCRS[\"%s\"," \
             "DATUM[\"%s\"," \
             "ELLIPSOID[\"%s\",%r,%r, LENGTHUNIT[\"metre\", 1.0, ID[\"EPSG\", 9001]]]," \
             "]," \
             "PRIMEM[\"Reference_Meridian\", 0.0]," \
             "CS[spherical,3]," \
             "AXIS[\"lat\", north, ORDER[1]]," \
             "AXIS[\"long\", east, ORDER[2]]," \
             "AXIS[\"distance (r)\",%r , ORDER[3], LENGTHUNIT[\"meter\", 1]]," \
             "ANGLEUNIT[\"Degree\", 0.0174532925199433, AUTHORITY[\"EPSG\",\"9122\"]]," \
             "AUTHORITY[\"%s\",\"%s\"]," \
             "REMARK[\"IAU report 2015 : doi://10.1007/s10569-017-9805-5\"]" \
             "]"

    def __init__(self, por):
        """
        Constructs a new WKT that describes an ocentric CRS with an ellipsoid datum

        :param por: planetary ocentric metadata
        :type por: WKTRecord

        """   
        logger.debug("Entering in ocentricWKT constructor")     
        super(OcentricWKT, self).__init__(
            por.getElement(OcentricMetadata.GEO_GCS_NAME),
            por.getElement(OcentricMetadata.DATUM_NAME),
            por.getElement(OcentricMetadata.ELLIPSOIDE_NAME),
            por.getElement(OcentricMetadata.RADIUS),
            por.getElement(OcentricMetadata.INVERSE_FLATTENING),
            por.getElement(OcentricMetadata.AUTHORITY_NAME),
            por.getElement(OcentricMetadata.AUTHORITY_CODE)
        )   
        logger.debug("Exiting from ocentricWKT constructor")        


    def getWKT(self):
        """
        Returns the CRS based on longitude/latitude

        :return: the WKT
        :rtype: str
         """
        logger.debug("Entering in ocentricWKT.getWkt")

        # building WKT string
        wkt = OcentricWKT.GEODCRS % (
            self.getGeoGcsName(), self.getDatumName(), self.getSpheroidName(), self.getRadius(), self.getInverseFlattening(),
            self.getRadius(), self.getAuthorityName(), self.getAuthorityCode()
        )

        logger.debug("Exiting from ocentricWKT.getWkt")
        return wkt 
        
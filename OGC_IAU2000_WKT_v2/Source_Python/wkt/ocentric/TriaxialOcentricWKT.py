import logging
from ..WKT import WKT
from enum import Enum

logger = logging.getLogger("wkt.triaxialOcentricWKT")

class TriaxialOcentricMetadata(Enum):
    GEO_GCS_NAME = "geogcsName"
    DATUM_NAME = "datumName"
    ELLIPSOIDE_NAME = "ellpsoideName"
    MEAN = "radius"
    SEMI_MAJOR = "semiMajor"
    SEMI_MINOR = "semiMinor"
    AXIS_B = "axisb"
    AUTHORITY_NAME = "authorityName"
    AUTHORITY_CODE = "authorityCode"
    LONGITUDE_ORDER = "longitudeOrder"
    CITATION = "citation"


class TriaxialOcentricWKT(WKT):
    """
    Class that allows to build an ocentric WKT with a triaxial datum.

    The WKT describing an ocentric CRS with an triaxial datum is displayed as follow:
    GEODCRS["<geogcsName>",
        DATUM["<datumName>",
            TRIAXIAL["<ellipsoidName>",<semi-major>,<semi-median>,<semi-minor>,
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
    GEODCRS_TRIAXIAL: WKT template for a ocentric CRS based on longitude/latitude and a triaxial body

    """ 

    GEODCRS_TRIAXIAL = "GEODCRS[\"%s\"," \
             "DATUM[\"%s\"," \
             "TRIAXIAL[\"%s\", %r, %r, %r, LENGTHUNIT[\"metre\", 1.0, ID[\"EPSG\", 9001]]]," \
             "]," \
             "PRIMEM[\"Reference_Meridian\", 0.0]," \
             "CS[spherical,3]," \
             "AXIS[\"lat\", north, ORDER[1]]," \
             "AXIS[\"long\", east, ORDER[2]]," \
             "AXIS[\"distance (r)\", %r, ORDER[3],LENGTHUNIT[\"meter\",1000]]," \
             "ANGLEUNIT[\"Degree\", 0.0174532925199433, AUTHORITY[\"EPSG\",\"9122\"]]," \
             "AUTHORITY[\"%s\",\"%s\"]," \
             "REMARK[\"IAU report 2015 : doi://10.1007/s10569-017-9805-5\"]" \
             "]"    

    def __init__(self, tcr):
        """
        Constructs a new WKT that describes an ocentric CRS with an ellipsoid datum

        :param tcr: Planetary triaxial ocentric metadata
        :type tcr: WKTRecord
        """
        logger.debug("Entering in TriaxialOcentricWKT constructor")     
        super(TriaxialOcentricWKT, self).__init__(
            tcr.getElement(TriaxialOcentricMetadata.GEO_GCS_NAME),
            tcr.getElement(TriaxialOcentricMetadata.DATUM_NAME),
            tcr.getElement(TriaxialOcentricMetadata.ELLIPSOIDE_NAME),
            tcr.getElement(TriaxialOcentricMetadata.MEAN),
            0.0,
            tcr.getElement(TriaxialOcentricMetadata.AUTHORITY_NAME),
            tcr.getElement(TriaxialOcentricMetadata.AUTHORITY_CODE)
        )        
        self.__majorAxis = tcr.getElement(TriaxialOcentricMetadata.SEMI_MAJOR)
        self.__minorAxis = tcr.getElement(TriaxialOcentricMetadata.SEMI_MINOR)
        self.__axisB = tcr.getElement(TriaxialOcentricMetadata.AXIS_B)
        logger.debug("Exiting from TriaxialOcentricWKT constructor")     


    def getWKT(self):
        """
        Returns the WKT format

        :return: the WKT
        :rtype: str
         """
        logger.debug("Entering in TriaxialOcentricWKT.getWkt")
        # building WKT string
        wkt = TriaxialOcentricWKT.GEODCRS_TRIAXIAL % (
            self.getGeoGcsName(), self.getDatumName(), self.getSpheroidName(), self.__majorAxis, self.__axisB, self.__minorAxis,
            self.getRadius(), self.getAuthorityName(), self.getAuthorityCode()
        )
        logger.debug("Exiting from TriaxialOcentricWKT.getWkt")
        return wkt    

    def getRecord(self):
        """
        Returns the CSV format 

        :return: the WKT
        :rtype: str
         """
        logger.debug("Entering in ocentricWKT.getRecord")


        record = {
            'type':'TRIAXIAL_OCENTRIC',
            TriaxialOcentricMetadata.GEO_GCS_NAME.value: self.getGeoGcsName(),
            TriaxialOcentricMetadata.DATUM_NAME.value: self.getDatumName(),
            TriaxialOcentricMetadata.ELLIPSOIDE_NAME.value: self.getSpheroidName(),
            TriaxialOcentricMetadata.SEMI_MAJOR.value: self.getRadius(),
            TriaxialOcentricMetadata.AXIS_B.value: self.__axisB,
            TriaxialOcentricMetadata.SEMI_MINOR.value: self.__minorAxis,
            TriaxialOcentricMetadata.MEAN.value: self.getRadius(),
            TriaxialOcentricMetadata.AUTHORITY_NAME.value: self.getAuthorityName(),
            TriaxialOcentricMetadata.AUTHORITY_CODE.value: self.getAuthorityCode()            
        }
        logger.debug("Exiting from ocentricWKT.getRecord")
        return record                     

    
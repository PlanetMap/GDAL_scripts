import logging
from ..WKT import WKT
from ..models.record import WKTRecord
from ..models.record import Metadata
from ..ocentric.TriaxialOcentricWKT import TriaxialOcentricWKT
from ..ocentric.TriaxialOcentricWKT import TriaxialOcentricMetadata
from ..ocentric.OcentricWKT import OcentricWKT
from ..ocentric.OcentricWKT import OcentricMetadata

logger = logging.getLogger("wkt.ocentricFactory")

class OcentricFactory(object):
    """
    Factory to create an ocentric CRS.

    The ocentric can be based either on the ellipsoid datum or on the triaxial datum

    The WKT describing an ocentric CRS is displayed as follow:
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

    or

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
    """

    @staticmethod
    def create(recordIAU, pubYear, authorityName):        
        """
        Creates a WKT describing an ocentric CRS.
        The ocentric can be based either on the ellipsoid datum or on the triaxial datum

        :param recordIAU: IAU record
        :param pubYear: publication year of the IAU report
        :param authorityName: authority name

        :type recordIAU: WKTRecord   
        :type pubYear: int
        :type authorityName: str

        :return: ographic CRS
        :rtype: WKT    
        """
        logger.debug("Entering in OcentricFactory.create")
        result = None
        gisCode = int(recordIAU.getElement(Metadata.NAIF_ID)) * 100
        if WKT.isTriaxial(float(recordIAU.getElement(Metadata.SEMI_MAJOR)), float(recordIAU.getElement(Metadata.SEMI_MINOR)), float(recordIAU.getElement(Metadata.AXIS_B))):
            logger.debug("Triaxial datum for ocentric CRS is selected for %s" % recordIAU.getElement(Metadata.BODY))
            planetaryOcentricTriaxial = WKTRecord(TriaxialOcentricMetadata)
            planetaryOcentricTriaxial.addRecord(TriaxialOcentricMetadata.GEO_GCS_NAME, recordIAU.getElement(Metadata.BODY) + " " + str(pubYear) + " ocentric")
            planetaryOcentricTriaxial.addRecord(TriaxialOcentricMetadata.DATUM_NAME, "D_" + recordIAU.getElement(Metadata.BODY) + "_" + str(pubYear))
            planetaryOcentricTriaxial.addRecord(TriaxialOcentricMetadata.ELLIPSOIDE_NAME, recordIAU.getElement(Metadata.BODY) + "_" + str(pubYear) + "_" + authorityName)
            planetaryOcentricTriaxial.addRecord(TriaxialOcentricMetadata.MEAN, float(recordIAU.getElement(Metadata.MEAN)))
            planetaryOcentricTriaxial.addRecord(TriaxialOcentricMetadata.AUTHORITY_NAME, authorityName)
            planetaryOcentricTriaxial.addRecord(TriaxialOcentricMetadata.AUTHORITY_CODE, str(pubYear) + ":" + str(gisCode))
            planetaryOcentricTriaxial.addRecord(TriaxialOcentricMetadata.SEMI_MAJOR, float(recordIAU.getElement(Metadata.SEMI_MAJOR)))
            planetaryOcentricTriaxial.addRecord(TriaxialOcentricMetadata.SEMI_MINOR, float(recordIAU.getElement(Metadata.SEMI_MINOR)))
            planetaryOcentricTriaxial.addRecord(TriaxialOcentricMetadata.AXIS_B, float(recordIAU.getElement(Metadata.AXIS_B)))            
            result = TriaxialOcentricWKT(planetaryOcentricTriaxial)  
        else:
            logger.debug("Ellipsoid datum for ocentric CRS is selected for %s" % recordIAU.getElement(Metadata.BODY))
            planetaryOcentric = WKTRecord(OcentricMetadata)
            planetaryOcentric.addRecord(OcentricMetadata.GEO_GCS_NAME, recordIAU.getElement(Metadata.BODY) + " " + str(pubYear) + " ocentric")
            planetaryOcentric.addRecord(OcentricMetadata.DATUM_NAME, "D_" + recordIAU.getElement(Metadata.BODY) + "_" + str(pubYear))
            planetaryOcentric.addRecord(OcentricMetadata.ELLIPSOIDE_NAME, recordIAU.getElement(Metadata.BODY) + "_" + str(pubYear) + "_" + authorityName)
            planetaryOcentric.addRecord(OcentricMetadata.RADIUS, float(recordIAU.getElement(Metadata.MEAN)))
            planetaryOcentric.addRecord(OcentricMetadata.INVERSE_FLATTENING, WKT.computeInverseFlattening(recordIAU.getElement(Metadata.SEMI_MAJOR), recordIAU.getElement(Metadata.SEMI_MINOR)))
            planetaryOcentric.addRecord(OcentricMetadata.AUTHORITY_NAME, authorityName)
            planetaryOcentric.addRecord(OcentricMetadata.AUTHORITY_CODE, str(pubYear) + ":" + str(gisCode))
            result = OcentricWKT(planetaryOcentric) 

        logger.debug("Exitin from OcentricFactory.create")
        return result    

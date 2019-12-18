import logging
from ..WKT import WKT
from ..models.record import WKTRecord
from ..models.record import Metadata
from ..ographic.TriaxialOgraphicWKT import TriaxialOgraphicWKT
from ..ographic.TriaxialOgraphicWKT import TriaxialOgraphicMetadata
from ..ographic.OgraphicWKT import OgraphicWKT
from ..ographic.OgraphicWKT import OgraphicMetadata

logger = logging.getLogger("wkt.graphicFactory")

class OgraphicFactory(object):
    """
    Factory to create an ographic CRS.
    """    

    @staticmethod
    def create(recordIAU, pubYear, authorityName):
        """
        Creates a ographic CRS.
        The ographic can be based on the ellipsoid datum or on the triaxial datum  

        The WKT describing an ographic CRS is displayed as follow:
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

        or

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


        :param recordIAU: IAU record
        :param pubYear: publication year of the IAU report
        :param authorityName: authority name

        :type recordIAU: WKTRecord   
        :type pubYear: int
        :type authorityName: str

        :return: ographic CRS
        :rtype: WKT     
        """

        logger.debug("Entering in OgraphicFactory.create")
        isForbidden, outputMessage = OgraphicFactory.__isForbiddenToCreateOgraphic(recordIAU)
        if isForbidden:
            raise Exception("{0} - {1}".format(recordIAU.getElement(Metadata.BODY), outputMessage))

        result = None
        gisCode = int(recordIAU.getElement(Metadata.NAIF_ID)) * 100 + 1
        if WKT.isTriaxial(float(recordIAU.getElement(Metadata.SEMI_MAJOR)), float(recordIAU.getElement(Metadata.SEMI_MINOR)), float(recordIAU.getElement(Metadata.AXIS_B))):
            logger.debug("Triaxial datum for ographic CRS is selected for %s" % recordIAU.getElement(Metadata.BODY))            
            planetaryOgraphicTriaxial  = WKTRecord(TriaxialOgraphicMetadata)
            planetaryOgraphicTriaxial.addRecord(TriaxialOgraphicMetadata.GEO_GCS_NAME, recordIAU.getElement(Metadata.BODY) + " " + str(pubYear) + " ographic")
            planetaryOgraphicTriaxial.addRecord(TriaxialOgraphicMetadata.DATUM_NAME, "D_" + recordIAU.getElement(Metadata.BODY) + "_" + str(pubYear))
            planetaryOgraphicTriaxial.addRecord(TriaxialOgraphicMetadata.ELLIPSOIDE_NAME, recordIAU.getElement(Metadata.BODY) + "_" + str(pubYear) + "_" + authorityName)
            planetaryOgraphicTriaxial.addRecord(TriaxialOgraphicMetadata.AUTHORITY_NAME, authorityName)
            planetaryOgraphicTriaxial.addRecord(TriaxialOgraphicMetadata.AUTHORITY_CODE, "IAU:" + str(pubYear) + ":" + str(gisCode))
            planetaryOgraphicTriaxial.addRecord(TriaxialOgraphicMetadata.SEMI_MAJOR, float(recordIAU.getElement(Metadata.SEMI_MAJOR)))
            planetaryOgraphicTriaxial.addRecord(TriaxialOgraphicMetadata.SEMI_MINOR, float(recordIAU.getElement(Metadata.SEMI_MINOR)))
            planetaryOgraphicTriaxial.addRecord(TriaxialOgraphicMetadata.AXIS_B, float(recordIAU.getElement(Metadata.AXIS_B))) 
            planetaryOgraphicTriaxial.addRecord(TriaxialOgraphicMetadata.LONGITUDE_ORDER, WKT.getLongitudeOrderFromRotation(recordIAU.getElement(Metadata.ROTATION)))           
            result = TriaxialOgraphicWKT(planetaryOgraphicTriaxial)  
        else:
            logger.debug("Ellipsoid datum for ographic CRS is selected for %s" % recordIAU.getElement(Metadata.BODY))
            planetaryOgraphic = WKTRecord(OgraphicMetadata)
            planetaryOgraphic.addRecord(OgraphicMetadata.GEO_GCS_NAME, recordIAU.getElement(Metadata.BODY) + " " + str(pubYear) + " ographic")
            planetaryOgraphic.addRecord(OgraphicMetadata.DATUM_NAME, "D_" + recordIAU.getElement(Metadata.BODY) + "_" + str(pubYear))
            planetaryOgraphic.addRecord(OgraphicMetadata.ELLIPSOIDE_NAME, recordIAU.getElement(Metadata.BODY) + "_" + str(pubYear) + "_" + authorityName)
            planetaryOgraphic.addRecord(OgraphicMetadata.RADIUS, float(recordIAU.getElement(Metadata.MEAN)))
            planetaryOgraphic.addRecord(OgraphicMetadata.INVERSE_FLATTENING, WKT.computeInverseFlattening(recordIAU.getElement(Metadata.SEMI_MAJOR), recordIAU.getElement(Metadata.SEMI_MINOR)))
            planetaryOgraphic.addRecord(OgraphicMetadata.AUTHORITY_NAME, authorityName)
            planetaryOgraphic.addRecord(OgraphicMetadata.AUTHORITY_CODE, "IAU:" + str(pubYear) + ":" + str(gisCode))
            planetaryOgraphic.addRecord(OgraphicMetadata.LONGITUDE_ORDER, WKT.getLongitudeOrderFromRotation(recordIAU.getElement(Metadata.ROTATION)))
            result = OgraphicWKT(planetaryOgraphic) 

        logger.debug("Exiting in OgraphicFactory.create")
        return result  
    
    @staticmethod
    def __isForbiddenToCreateWithRule1(recordIAU):
        """
        RULE1 : if no rotation direction, we do not know the direction of axis. So, an ographic CRS is forbidden
        :param recordIAU: record from the IAU report
        :type recordIAU: []
        :return True when the creation is borbidden otherwise False
        :rtype boolean
        """
        logger.debug("__isForbiddenToCreateWithRule1")
        return recordIAU.getElement(Metadata.ROTATION) is None
    
    @staticmethod
    def __isForbiddenToCreateWithRule2(recordIAU):    
        """
        RULE2 : if target is Sun or Moon (SUN and Moon are two spherical bodies with positive longitude to EAST
        by usage). So, an ographic CRS is forbidden
        :param recordIAU: record from the IAU report
        :type recordIAU: []
        :return True when the creation is borbidden otherwise False
        :rtype boolean        
        """
        logger.debug("__isForbiddenToCreateWithRule2")
        return recordIAU.getElement(Metadata.BODY).upper() in ["SUN", "MOON"]

    @staticmethod
    def __isForbiddenToCreateWithRule3(recordIAU):          
        """
        RULE3 : if inverse_flattening = 0 (= a sphere) and a RETROGRADE rotation (positive longitude to EAST).
        So, an ograhic CRS is forbidden
        :param recordIAU: record from the IAU report
        :type recordIAU: []
        :return True when the creation is borbidden otherwise False
        :rtype boolean        
        """
        logger.debug("__isForbiddenToCreateWithRule3")
        flattening = WKT.computeInverseFlattening(recordIAU.getElement(Metadata.SEMI_MAJOR), recordIAU.getElement(Metadata.SEMI_MINOR))
        return WKT.isEqual(flattening, 0) and recordIAU.getElement(Metadata.ROTATION) == WKT.Rotation.RETROGRADE.value

    @staticmethod
    def __isForbiddenToCreateOgraphic(recordIAU):
        """
        Test if the ographic do not need to be created because it is the same as ocentric CRS
        :param recordIAU: record from the IAU report
        :param outputMessage: reason for which the ographic CRS is forbidden
        :type recordIAU: []
        :type outputMessage: str
        :return True when the creation is borbidden otherwise False
        :rtype [bool, str]        
        """             
        if OgraphicFactory.__isForbiddenToCreateWithRule1(recordIAU):
            outputMessage = "RULE1 : Forbidden to create ographic CRS for {0}".format(recordIAU.getElement(Metadata.BODY))
            result = True
        elif OgraphicFactory.__isForbiddenToCreateWithRule2(recordIAU):
            outputMessage = "RULE2 : Forbidden to create ographic CRS for {0}".format(recordIAU.getElement(Metadata.BODY))
            result = True
        elif OgraphicFactory.__isForbiddenToCreateWithRule3(recordIAU):
            outputMessage = "RULE3 : Forbidden to create ographic CRS for {0}".format(recordIAU.getElement(Metadata.BODY))
            result = True
        else:
            outputMessage = None
            result = False   
        return [result, outputMessage]

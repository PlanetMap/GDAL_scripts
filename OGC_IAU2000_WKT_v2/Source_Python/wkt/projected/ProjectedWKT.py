import logging
from ..WKT import WKT
from enum import Enum

logger = logging.getLogger("wkt.projectedWKT")


class ProjectedMetadata(Enum):
    PROJECTION_ENUM = "projectionCrsName"
    PROJECTION_NAME = "projectionName"
    AUTHORITY_NAME = "authorityName"
    AUTHORITY_CODE = "authorityCode"

class ProjectedWKT(WKT) :
    """
    Class that allows to build a projected WKT.

    Constants
    --------- 
    PROJCS : WKT template for Porjected CRS

    """                        

    PROJCS = "PROJCS[\"%s\"," \
             "%s," \
             "%s" \
             "]"    

    def __init__(self, ppr, planetWKT):
        """
            Creates a projected CRS.

            The WKT is displayed as follow:
            PROJCS["<projectionName>",
                <GEODCRS>|<GEOGCRS>
                <projection parameters>
            ]    

            <projection parameters> are defined in the ProjectedWKT.Projection class.
            The projection can be set in setProjection method  

            :param pgr: Planetary projceted record
            :type ppr: PlanetaryProjectedRecord      
        """   
        logger.debug("Entering in projectedWKT constructor")     

        super(ProjectedWKT, self).__init__(planetWKT.getGeoGcsName(), planetWKT.getDatumName(), planetWKT.getSpheroidName(), planetWKT.getRadius(), planetWKT.getInverseFlattening(), planetWKT.getAuthorityName(), planetWKT.getAuthorityCode())
        self.__planetProjected = ppr
        self.__planetWKT = planetWKT 

        logger.debug("Exiting from projectedWKT constructor")     


    class Projection(Enum):
        """List of supported projections.

        It exists two kind of projections :
        - the classical ones
        - the auto that allow the user to also submit the projection parameters

        Each projection value is a hash that contains:
        - code for ocentric CRS
        - url of the projection
        - the projection name
        - the projection parameters

        """
        EQUIRECTANGULAR_0 = {  # Equirectangular, clon=0
            "code": 10,
            "url": "https://proj4.org/operations/projections/eqc.html",
            "projection": "Equirectangular",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Central_Meridian": 0,
                "latitude_Of_Origin": 0
            },
            "isPolar": False
        }
        EQUIRECTANGULAR_180 = {  # Equirectangular, clon=180
            "code": 12,
            "url": "https://proj4.org/operations/projections/eqc.html",
            "projection": "Equirectangular",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Central_Meridian": 180,
                "Latitude_Of_Origin": 0
            },
            "isPolar": False
        }
        SINUSOIDAL_0 = {  # Sinusoidal, clon=0
            "code": 14,
            "url": "https://proj4.org/operations/projections/sinu.html",
            "projection": "Sinusoidal",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Longitude_Of_Center": 0
            },
            "isPolar": False
        }
        SINUSOIDAL_180 = {  # Sinusoidal, clon=180
            "code": 16,
            "url": "https://proj4.org/operations/projections/sinu.html",
            "projection": "Sinusoidal",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Longitude_Of_Center": 180
            },
            "isPolar": False
        }
        STEREOGRAPHIC_NORTH = {  # North Polar, clon=0
            "code": 18,
            "url": "https://proj4.org/operations/projections/stere.html",
            "projection": "Stereographic",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Central_Meridian": 0,
                "Scale_Factor": 1,
                "Latitude_Of_Origin": 90
            },
            "isPolar": True
        }
        STEREOGRAPHIC_SOUTH = {  # South Polar, clon=0
            "code": 20,
            "url": "https://proj4.org/operations/projections/stere.html",
            "projection": "Stereographic",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Central_Meridian": 0,
                "Scale_Factor": 1,
                "Latitude_Of_Origin": -90
            },
            "isPolar": True
        }
        MOLLWEIDE_0 = {  # Mollweide, clon=0
            "code": 22,
            "url": "https://proj4.org/operations/projections/moll.html",
            "projection": "Mollweide",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Central_Meridian": 0
            },
            "isPolar": False
        }
        MOLLWEIDE_180 = {  # Mollweide, clon=180
            "code": 24,
            "url": "https://proj4.org/operations/projections/moll.html",
            "projection": "Mollweide",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Central_Meridian": 180
            },
            "isPolar": False
        }
        ROBINSON_0 = {  # Robinson, clon=0
            "code": 26,
            "url": "https://proj4.org/operations/projections/robin.html",
            "projection": "Robinson",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Longitude_Of_Center": 0
            },
            "isPolar": False
        }
        ROBINSON_180 = {  # Robinson, clon=180
            "code": 28,
            "url": "https://proj4.org/operations/projections/robin.html",
            "projection": "Robinson",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Longitude_Of_Center": 180
            },
            "isPolar": False
        }
        AUTO_SINUSOIDAL = {  # Auto Sinusoidal
            "code": 60,
            "url": "https://proj4.org/operations/projections/sinu.html",
            "projection": "Sinusoidal",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Longitude_Of_Center": 0
            },
            "isPolar": False
        }
        AUTO_STEREOGRAPHIC = {  # Auto Stereographic, clon=0
            "code": 62,
            "url": "https://proj4.org/operations/projections/stere.html",
            "projection": "Stereographic",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Central_Meridian": 0,
                "Scale_Factor": 1,
                "Latitude_Of_Origin": 0
            },
            "isPolar": False
        }
        AUTO_TRANSVERSE_MERCATOR = {  # Auto Transverse Mercator
            "code": 64,
            "url": "https://proj4.org/operations/projections/tmerc.html",
            "projection": "Transverse_Mercator",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Central_Meridian": 0,
                "Scale_Factor": 0.9996,
                "Latitude_Of_Origin": 0
            },
            "isPolar": False
        }
        AUTO_ORTHOGRAPHIC = {  # Auto Orthographic
            "code": 66,
            "url": "https://proj4.org/operations/projections/ortho.html",
            "projection": "Orthographic",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Central_Meridian": 0,
                "Latitude_Of_Origin": 90
            },
            "isPolar": True
        }
        AUTO_EQUIRECTANGULAR = {  # Auto Equidistant_Cylindrical
            "code": 68,
            "url": "https://proj4.org/operations/projections/eqc.html",
            "projection": "Equirectangular",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Central_Meridian": 180,
                "Latitude_Of_Origin": 0
            },
            "isPolar": False
        }
        AUTO_LAMBERT_CONFORMAL_CONIC = {  # Auto Lambert_Conformal_Conic
            "code": 70,
            "url": "https://proj4.org/operations/projections/lcc.html",
            "projection": "Lambert_Conformal_Conic_2SP",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Central_Meridian": 0,
                "Standard_Parallel_1": -20,
                "Standard_Parallel_2": 20,
                "Latitude_Of_Origin": 0
            },
            "isPolar": False
        }
        AUTO_LAMBERT_AZIMUTHAL_EQUAL = {  # Auto Lambert_Azimuthal_Equal_Area
            "code": 72,
            "url": "https://proj4.org/operations/projections/laea.html",
            "projection": "Lambert_Azimuthal_Equal_Area",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Longitude_Of_Center": 0,
                "Latitude_Of_Center": 90
            },
            "isPolar": True
        }
        AUTO_MERCATOR = {  # Auto Mercator
            "code": 74,
            "url": "https://proj4.org/operations/projections/merc.html",
            "projection": "Mercator_1SP",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Central_Meridian": 0,
                "Scale_Factor": 1
            },
            "isPolar": False
        }
        AUTO_ALBERS = {  # Auto Albers
            "code": 76,
            "url": "https://proj4.org/operations/projections/aea.html",
            "projection": "Albers_Conic_Equal_Area",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Longitude_Of_Center": 0.0,
                "Standard_Parallel_1": 60.0,
                "Standard_Parallel_2": 20.0,
                "Latitude_Of_Center": 40.0
            },
            "isPolar": False
        }
        # # It seems it is OK the next GDAL release : https://github.com/OSGeo/gdal/pull/101
        # # Need to check projection parameters when fixed in GDAL
        # AUTO_OBLIQUE_CYLINDRICAL = {  # Auto Oblique Cylindrical Equal Area -- Problem for this projection
        #     "code": 78,
        #     "projection": "Oblique_Cylindrical_Equal_Area",
        #     "parameters": {
        #         "False_Easting": 0,
        #         "False_Northing": 0,
        #         "Central_Meridian": 0.0,
        #         "Standard_Parallel_1": 0.0
        #     }
        # }
        AUTO_MOLLWEIDE = {  # Auto Mollweide
            "code": 80,
            "url": "https://proj4.org/operations/projections/moll.html",
            "projection": "Mollweide",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Central_Meridian": 0.0
            },
            "isPolar": False
        }
        AUTO_ROBINSON = {  # Auto Robinson
            "code": 82,
            "url": "https://proj4.org/operations/projections/robin.html",
            "projection": "Robinson",
            "parameters": {
                "False_Easting": 0,
                "False_Northing": 0,
                "Longitude_of_center": 0.0
            },
            "isPolar": False
        }

    
    def getProjectionEnum(self):
        """
        Returns the used projection
        :return: None when no defined projection otherwise the Projection object
        :rtype: None or WKT.Projection
        """
        return self.__planetProjected.getElement(ProjectedMetadata.PROJECTION_ENUM)

    def getProjectionName(self):
        """
        Returns the projection name
        :return: None when no defined projection otherwise the projection name
        :rtype: None or str
        """
        return self.__planetProjected.getElement(ProjectedMetadata.PROJECTION_NAME)

    def getAuthorityName(self):
        """
        Returns the projection authority name
        :return: None when no defined projection otherwise the projection authority name
        :rtype: None or str
        """
        return self.__planetProjected.getElement(ProjectedMetadata.AUTHORITY_NAME)

    def getAuthorityCode(self):
        """
        Returns the projection authority code of the spheroid
        :return: None when no defined projection otherwise the projection authority code
        :rtype: None or str
        """
        return self.__planetProjected.getElement(ProjectedMetadata.AUTHORITY_CODE)
        
    
    def getWKT(self):
        """
        Returns the projected CRS.

        :return: the WKT
        :rtype: str
        """
        logger.debug("Entering in projectedWKT.getWKT")

        # defines the projection name in the WKT
        projParams = "PROJECTION[\"" + self.getProjectionEnum().value["projection"] + "\"]"

        # defines the projection parameters in the WKT
        for param in self.getProjectionEnum().value['parameters'].keys():
            projParams += ",PARAMETER[\"%s\",%r]" % (param, self.getProjectionEnum().value['parameters'][param])

        # defines the projection authority
        projParams += ",UNIT[\"Meter\",1, AUTHORITY[\"EPSG\",\"9001\"]],AUTHORITY[\"%s\",\"%s\"]" % (
            self.getAuthorityName(), self.getAuthorityCode())

        # building WKT
        wkt = ProjectedWKT.PROJCS % (
            self.getProjectionName(), self.__planetWKT.getWKT(), projParams
        )

        logger.debug("Exiting from projectedWKT.getWKT")
        return wkt   

    def getRecord(self):
        """
        Returns the Record format 

        :return: the WKT
        :rtype: str
         """
        logger.debug("Entering in ocentricWKT.getRecord")

        record = self.__planetWKT.getRecord()
        record[ProjectedMetadata.PROJECTION_NAME] = self.getProjectionName()
        record[ProjectedMetadata.PROJECTION_ENUM] = self.getProjectionEnum().name
        record[ProjectedMetadata.AUTHORITY_CODE] = self.getAuthorityCode()
        record[ProjectedMetadata.AUTHORITY_NAME] = self.getAuthorityName()
        record['type'] = record['type']+"_PROJECTED"

        logger.debug("Exiting from ocentricWKT.getRecord")
        return record             
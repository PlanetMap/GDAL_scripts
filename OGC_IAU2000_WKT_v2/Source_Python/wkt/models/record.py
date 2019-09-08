import logging
from enum import Enum

logger = logging.getLogger("wkt.record")

class WKTRecord(object):
    """
    Data model
    """
    def __init__(self, metadataEnum) :
        """
        Constructs the data model based on attributes from the metadataEnum
        param metadataEnum: attributes of the data model
        type metadataEnum: Enumerate
        """
        self.__metadata = {}
        for attribute in metadataEnum:
            self.__metadata[attribute] = None 

    def addRecord(self, key, value) :
        """
        Add a record based on the key from the metadataEnum
        param key: key to add
        type key: str
        param value: value
        type value: str
        """
        self.__metadata[key] = value


    def setRecord(self, values, mapping):
        """
        Set the collection
        param values: collection
        type values:{}
        """
        logger.debug("Entering in setRecord")
        for key, value in mapping.items() :
            if values[value] in ["", "-1"]:
                logger.debug("%s has value \"\" or -1 => set the value to None" % (key))
                values[value] = None            
            self.__metadata[key] = values[value]
            logger.debug("Set in data model %s = %s"%(key, values[value]))
        logger.debug("Data model is created for %s" % self.__metadata[Metadata.BODY])
        logger.debug("Exiting from setRecord")
    

    def getElement(self, metadataEnum) :
        """
        Returns an element from an enumerate
        param metadataEnum: Enumeration
        type metadataEnum: Enum
        return: An element from the collection
        rtype: str
        """
        return self.__metadata[metadataEnum]

class Metadata(Enum):
    """Enumerated class that describes the attributes of the IAU catalog"""
    NAIF_ID = "Naif_id"
    BODY = "Body"
    MEAN = "Mean"
    SEMI_MAJOR = "Semimajor"
    AXIS_B = "Axisb"
    SEMI_MINOR = "Semiminor"
    ROTATION = "rotation"
    ORIGIN_LONG_NAME = "origin_long_name"
    ORIGIN_LONG_POS = "origin_lon_pos"

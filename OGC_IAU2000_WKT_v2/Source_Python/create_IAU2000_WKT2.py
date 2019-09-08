#!/usr/bin/python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#  Name: create_IAU2000_WKT2.py
#  Author: Trent Hare, Jean-Christophe Malapert
#  Original: Jan 2006
# Feb 2016:
# ---- update to report IAU Mean from reports,
# ---- Asteroids and IAU reported Comets,
# ---- and two new projections (Mollweide and Robinson)
# March 2016:
# ---- added IAU authority, cleaned code, added refs and updated albers to stndPar_1,2=60,20
# July 2016:
# ---- changed Decimal_Degree to just Degree
# Sep 2016:
# ---- Removed extra " before GEOGCS in map projected string
# July 2017:
# ---- Updated for Python v3 and support for -1 NoData values in table
# Aug 2018:
# ---- Updated for 2015 IAU report and change 2009 to IAU from IAU_IAG
# ---- Code refactoring (logging, class, enumerations, removed repetition of WKT string, command line parser)
# ---- Added creation capabilities for prj and iniFile for proj4
# ---- Added rotation direction consideration for ocentric and ographic CRS
# ---- Improved WKT (towgs84 string for datum shifting)
# ---- Fixed bug about projection parameter (Fully compliant with gdal)
# ---- Fixed bug about Halley WKT (radius was -1)
# ---- Changed algorithm for triaxial ellipsoids
# ---- Added WKT validation
# ---- Avoided WKT duplication when ocentric CRS has the same signature as ographic CRS
# ---- Exported PRJ/PROJ for no ellisoid body
# Feb 2019:
# ---- Set Primem to Reference_Meridian, 0.0
# ---- Fixed a bug with subprocess
# ---- Use semi-minor radius as a sphere for polar projections for ocentric coordinates system
# Sep 2019
# ---- Use either triaxial or ellipsoid datum for ocentric/ographic CRS
# ---- Use WKT V2
# ---- Refactoring of the WKT code
#
#  Description: This Python script creates a IAU2000/2009/2015 WKT projection strings for WMS services. prj and
#               initFile for proj4 can be created
#
# License: Public Domain
#
# INPUT: (naifcodes_radii_m_wAsteroids_IAU2000.csv or naifcodes_radii_m_wAsteroids_IAU2015.csv)
#
# Example file format:
# Naif_id,Body,IAU2015_Mean,IAU2015_Semimajor,IAU2015_Axisb,IAU2015_Semiminor,rotation,origin_long_name,origin_lon_pos
# 10,Sun,695700000.00,695700000.00,695700000.00,695700000.00,Direct,,
# 199,Mercury,2439400.00,2440530.00,2440530.00,2438260.00,Direct,Hun Kal,20
# 299,Venus,6051800.00,6051800.00,6051800.00,6051800.00,Retrograde,Ariadne,0
# 399,Earth,6371008.40,6378136.60,6378136.60,6356751.90,Direct,Greenwich,0
# 301,Moon,1737400.00,1737400.00,1737400.00,1737400.00,Direct,,
# 499,Mars,3389500.00,3396190.00,3396190.00,3376200.00,Direct,Airy-0,0
# 401,Phobos,11080.00,13000.00,11400.00,9100.00,Direct,,
# 402,Deimos,6200.00,7800.00,6000.00,5100.00,Direct,,
# ...
#
# OUTPUT:
#   Example: WMS#,GEOGCS["Mars 2000",DATUM["D_Mars_2000",SPHEROID["Mars_2000_IAU_IAG",3396190.0,169.8944472236118]],PRIMEM["Reference_Meridian",0],UNIT["Degree",0.0174532925199433],AUTHORITY["IAU2000","49900"]]
#
# ------------------------------------------------------------------------------
#
#

import logging
import os
import sys
import argparse
import time
import functools
from enum import Enum

try:
    import coloredlogs
except:
    print("please install coloredlogs package to get logs in color")

assert sys.version_info >= (2, 7), "Install python version >= 2.7"


from wkt.ocentric.OcentricWKT import OcentricWKT
from wkt.ocentric.OcentricWKT import OcentricMetadata
from wkt.ocentric.OcentricFactory import OcentricFactory

from wkt.ographic.OgraphicWKT import OgraphicWKT
from wkt.ographic.OgraphicWKT import OgraphicMetadata
from wkt.ographic.OgraphicFactory import OgraphicFactory

from wkt.projected.ProjectedWKT import ProjectedWKT
from wkt.projected.ProjectedWKT import ProjectedMetadata

from wkt.WKT import WKT

from wkt.models.record import WKTRecord
from wkt.models.record import Metadata



class IAUCatalog:
    """
    IAUCatelog processes a CSV file in order to convert it in a interoperable format

    Constants
    ---------
    REFERENCES: Source of CSV file
    """
    # References - block of text for start of files
    REFERENCES = {
        "IAU2000": """#IAU2000 WKT Codes
# This file derived from the naif ID Codes.txt file distributed by
# USGS for NASA/IAU/NAIF (http://naif.jpl.nasa.gov/)
#
#
#     The sources for the constants listed in this file are:
#
#        [1]  Seidelmann, P.K., Abalakin, V.K., Bursa, M., Davies, M.E.,
#              Bergh, C. de, Lieske, J.H., Oberst, J., Simon, J.L.,
#              Standish, E.M., Stooke, P., and Thomas, P.C. (2002).
#              "Report of the IAU/IAG Working Group on Cartographic
#              Coordinates and Rotational Elements of the Planets and
#              Satellites: 2000," Celestial Mechanics and Dynamical
#              Astronomy, v.82, Issue 1, pp. 83-111.
#
""",
        "IAU2009": """#IAU2009 WKT Codes
# This file derived from the naif ID Codes.txt file distributed by
# USGS for NASA/IAU/NAIF (http://naif.jpl.nasa.gov/)
#
#
#     The sources for the constants listed in this file are:
#
#        [2]  Archinal, B. A., M. F. A'Hearn, E. Bowell, A. Conrad,
#              G. J. Consolmagno, R. Courtin, T. Fukushima, D. Hestroffer,
#              J. L. Hilton, G. A. Krasinsky, G. Neumann, J. Oberst,
#              P. K. Seidelmann, P. Stooke, D. J. Tholen, P. C. Thomas,
#              I. P. Williams (2011), "Report of the IAU Working Group
#              on Cartographic Coordinates and Rotational Elements of the
#              Planets and Satellites: 2011," Celestial Mechanics and Dynamical
#              Astronomy, v.109, Issue 2, pp. 101-135.
#
""",
        "IAU2015": """#IAU2015 WKT Codes
# This file derived from the naif ID Codes.txt file distributed by
# USGS for NASA/IAU/NAIF (http://naif.jpl.nasa.gov/)
#
#
#     The sources for the constants listed in this file are:
#
#        [3] Archinal, B. A., C. H. Acton, M. F. A'Hearn, A. Conrad,
#             G. J. Consolmagno, T. Duxbury, D. Hestroffer, J. L. Hilton,
#             R. L. Kirk, S. A. Klioner, D. McCarthy, J. Oberst, J. Ping,
#             P. K. Seidelmann, D. J. Tholen, P. C. Thomas,
#             I. P. Williams (2018), "Report of the IAU Working Group
#             on Cartographic Coordinates and Rotational Elements of the
#             Planets and Satellites: 2015," Celestial Mechanics and Dynamical
#             Astronomy, 130: 22. https://doi.org/10.1007/s10569-017-9805-5.
#
"""
    }

    def __init__(self, file):
        """
        Creates a IAU catalog

        :param file: CSV file
        :type file: str
        """

        if 'logger' in globals():
            # ok logger is debug, we can log event
            pass
        else:
            # logger is not defined, we define it and we make it disabled
            global logger
            logger = logging.getLogger()
            logger.disabled = True

        logger.debug("Entering in constructor with file=%s" % file)

        assert isinstance(file, str), "IAUCatalog.__init__: file must be a string"
        self.__file = file
        self.__theYear = self.__ckeckFileNameAndGetYear(file)

        # Before 2015, the longitude of all CRS was positive to East (this was not conform to IAU definition).
        # In this version, the longitude is conform to IAU definition
        if float(self.__theYear) < 2015:
            raise Exception("This program is not valid before 2015")

        self.__initGroupAndRefsIAU(self.__theYear)

        self.__mapping = {
            Metadata.NAIF_ID : 0,
            Metadata.BODY : 1,
            Metadata.MEAN : 2,
            Metadata.SEMI_MAJOR : 3,
            Metadata.AXIS_B : 4,
            Metadata.SEMI_MINOR : 5,
            Metadata.ROTATION : 6,
            Metadata.ORIGIN_LONG_NAME : 7,
            Metadata.ORIGIN_LONG_POS : 8
        }        

        logger.debug("Exit from constructor")

    def __ckeckFileNameAndGetYear(self, file):
        """
        Checks the filename string and retrieves the year

        The year is used to get the right IAU publication.

        :param file: the filename
        :type file: str
        """
        logger.debug("Entering in __ckeckFileNameAndGetYear with file=%s" % file)

        assert isinstance(file, str), "IAUCatalog.__ckeckFileNameAndGetYear: file must be a string"
        # grab year from file name
        theYear = self.__file.split('IAU')[1].split('.')[0]
        if not self.__isInt(theYear):
            logger.debug("Exiting from __ckeckFileNameAndGetYear with error")
            raise Exception("Can't parse the year from filename: " + file)

        logger.debug("Exiting from __ckeckFileNameAndGetYear with theYear=%s" % theYear)
        return theYear

    def __initGroupAndRefsIAU(self, year):
        """
        Stores the reference to the right publication according to the year.

        :param year: the year
        :type year: str
        """
        logger.debug("Entering in __initGroupAndRefsIAU with year=%s" % year)

        assert isinstance(year, str), "IAUCatalog.__initGroupAndRefsIAU: year must be a string"

        if year == "2000":
            self.__group = "IAU_IAG"
            self.__refsIAU = IAUCatalog.REFERENCES["IAU2000"]
        elif year == "2009":
            self.__group = "IAU"
            self.__refsIAU = IAUCatalog.REFERENCES["IAU2009"]
        elif year == "2015":
            self.__group = "IAU"
            self.__refsIAU = IAUCatalog.REFERENCES["IAU2015"]
        else:
            logger.debug("Exiting from __initGroupAndRefsIAU with error")
            raise Exception("Warning: No reference for the this year: " + year)

        logger.debug("Exiting from __initGroupAndRefsIAU")

    def __isInt(self, string):
        """
        Returns True when the string is an integer otherwise False

        :param string: string to test
        :return: True when the string is an integer otherwise False
        :type string: str
        :rtype: bool
        """

        logger.debug("Entering in __isInt with string=%s" % string)

        try:
            int(string)
            is_int = True
        except:
            is_int = False

        logger.debug("Exiting from __isInt with %s" % is_int)
        return is_int

    def __isNumber(self, a):
        """ Returns True when a is a number otherwise False

        :param a: string to test
        :return: True when a is a number otherwise False
        :type a: str
        :rtype bool
        """

        logger.debug("Entering in __isNumber with a=%s" % a)

        try:
            float(a)
            bool_a = True
        except:
            bool_a = False

        logger.debug("Exiting from __isNumber with %s" % bool_a)
        return bool_a

    def __processLine(self, tokens):
        """
        Process a line of the catalog

        :param tokens: the parameters of the catalog
        :return: the crs list
        :type tokens: list
        :rtype: list
        """
        logger.debug("Entering in __processLine with tokens=%s" % tokens)

        crs = []
        record = WKTRecord(Metadata)
        record.setRecord(tokens, self.__mapping)    

        # create an ocentric CRS
        # From IAU, all CRS can be defined as ocentric with the longitude counted positively to East
        ocentric = OcentricFactory.create(record, self.__theYear, self.__group)
        crs.append({
            "target": record.getElement(Metadata.BODY),
            "wkt": ocentric,
            "type": WKT.CRS.OCENTRIC
        })

        # create an ographic CRS
        # From IAU, the longitude direction (EAST/WEST) depends on the rotation direction. When the catalog does not
        # have the rotation direction, then the ographic CRS is not created
        try:
            ographic = OgraphicFactory.create(record, self.__theYear, self.__group)
            crs.append({
                "target": record.getElement(Metadata.BODY),
                "wkt": ographic,
                "type": WKT.CRS.OGRAPHIC
            })            
        except Exception as error:
            logger.debug(tokens)
            logger.warning(str(error))
            ographic = None

        # create a projected CRS for each defined Projection on both ocentric and ographic CRS
        projectedCrss = self.__createProjectedCrs(record, ocentric, ographic)
        crs.extend(projectedCrss)

        logger.debug("Exiting from __processLine with crs=%s" % crs)
        return crs


    def __createProjectedCrs(self, recordIAU, ocentric, ographic):
        """Creates projected Crs for all defined projections

        :param recordIAU: the record from IAU document
        :return: a list that contains all projected CRS
        :type recordIAU: IAURecord
        :rtype: a list that contains all projected CRS
        """

        logger.debug("Entering in __createProjectedCrs with IAURecord=%s, ocentric=%s, ographic=%s" % (
            recordIAU, ocentric, ographic
        ))

        crs = []
        # iter on each defined projection
        for projectionEnum in ProjectedWKT.Projection:  
            gisCode = int(recordIAU.getElement(Metadata.NAIF_ID)) * 100 + projectionEnum.value['code']
            planetaryProjected = WKTRecord(ProjectedMetadata)
            planetaryProjected.addRecord(ProjectedMetadata.PROJECTION_ENUM, projectionEnum)
            planetaryProjected.addRecord(ProjectedMetadata.PROJECTION_NAME, recordIAU.getElement(Metadata.BODY) + "_" + projectionEnum.value['projection'])
            planetaryProjected.addRecord(ProjectedMetadata.AUTHORITY_NAME, self.__group)
            planetaryProjected.addRecord(ProjectedMetadata.AUTHORITY_CODE, self.__theYear + ":" + str(gisCode))           
            ocentricProjection = ProjectedWKT(planetaryProjected, ocentric)
            # save projection
            crs.append({
                "target": recordIAU.getElement(Metadata.BODY),
                "wkt": ocentricProjection,
                "type": WKT.CRS.PROJECTED_OCENTRIC
            })

            # define ographic projection when ographic CRS is defined
            if ographic is not None:
                gisCode = gisCode + 1
                ographicProjection = ProjectedWKT(planetaryProjected, ographic)
                # save projection
                crs.append({
                    "target": recordIAU.getElement(Metadata.BODY),
                    "wkt": ographicProjection,
                    "type": WKT.CRS.PROJECTED_OGRAPHIC
                })

        logger.debug("Exiting from __createProjectedCrs with %s" % crs)
        return crs

    def getRefsIAU(self):
        """
        Returns ref IAU
        :return:  the ref IAU
        :rtype: str
        """
        return self.__refsIAU

    def processFile(self):
        """
        Process the catalog

        :return: A list that contains all CRS
        :rtype: float
        """

        logger.debug("Entering in processFile")
        data = []
        for line in open(self.__file):
            tokens = line.rstrip().split(',')
            if not self.__isInt(tokens[0]) or (WKT.isEqual(float(tokens[2]), -1)
                                               or WKT.isEqual(float(tokens[3]), -1)
                                               or WKT.isEqual(float(tokens[5]), -1)):
                logger.warning("%s is ignored for one of these reasons : no ID, no mean, no semi-major, no semi-minor radius", tokens)
            else:                
                # Then Radii values exist in input table and naif is a number                
                try:
                    data.extend(self.__processLine(tokens))
                except Exception as error:
                    logger.error("Error when procesing line : %s", str(error))

        logger.debug("Exiting from processFile with %s CRS" % len(data))
        return data

    @staticmethod
    def saveAsWKT(crss, filename=None):
        """ Save the list of CRS in a file

        :param crss: the list that contains all CRS
        :param filename: output filename
        """
        if filename is None:
            filename = crss[0]['wkt'].getAuthorityName() + "_v4.wkt"

        if filename and filename is not sys.stdout:
            fileToOutput = open(filename, 'w')
        else:
            fileToOutput = filename

        try:
            target = ""
            authorityName = crss[0]['wkt'].getAuthorityName()
            authorityCode = crss[0]['wkt'].getAuthorityCode()
            year = authorityCode.split(':')[0]
            authority = authorityName+year
            fileToOutput.write("%s\n" % IAUCatalog.REFERENCES[authority])

            for crs in crss:
                wktObj = crs['wkt']
                if crs['target'] != target:
                    fileToOutput.write("\n\n#%s WKT Codes for %s\n" % (wktObj.getAuthorityName(), crs['target']))
                    target = crs['target']

                # Get the authority of the projection if it exists other this one from the datum
                fileToOutput.write("%s,%s\n\n" % (wktObj.getAuthorityCode(), wktObj.getWKT()))

        finally:
            if fileToOutput is not sys.stdout:
                fileToOutput.close()


    @staticmethod
    def saveAs(crss, filename=None, format="WKT"):
        """ Save the list of CRS in a file

        :param crss: the list that contains all CRS
        :param filename:
        :param format: Output format. It can be WKT (default WKT)
        """
        if format == "WKT":
            IAUCatalog.saveAsWKT(crss, filename)
        else:
            raise Exception("Unknown output format")


class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)


def initLogger(logger, LEVEL_LOG):
    """
    Init the logger.

    The info level format of the logger is set to "%(asctime)s :: %(levelname)s :: %(message)s"  and the debug
    level format is set to "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s". The logs output is set
    to the console

    :param logger: logger
    :param LEVEL_LOG: logger level
    """

    FORMAT_INFO = "%(asctime)s :: %(levelname)s :: %(message)s"
    FORMAT_DEBUG = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    # fh = logging.FileHandler('get_iau2000.log')
    logging.StreamHandler()
    if LEVEL_LOG == logging.INFO:
        logging.basicConfig(format=FORMAT_INFO)
    else:
        logging.basicConfig(format=FORMAT_DEBUG)
    # logger.addHandler(fh)
    logger.setLevel(LEVEL_LOG)
    try:
        coloredlogs.install()
    except:
        pass


def timeSpend(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        startTime = time.time()
        result = func(*args, **kwargs)
        elapsedTime = time.time() - startTime
        logger.info("function [{}] finished in {} ms".format(
            func.__name__, int(elapsedTime * 1000)
        ))
        return result

    return newfunc


@timeSpend
def loadAndProcessCatalog(data):
    """
    Load and process the IAU CSV file
    :param data: IAU CSV file
    :return: the list of WKT
    """
    iauData = IAUCatalog(data)
    return iauData.processFile()


@timeSpend
def saveAs(wktList, outputFile, format):
    IAUCatalog.saveAs(wktList, outputFile, format=format)


def main(argv):
    parser = argparse.ArgumentParser(description="Converts IAU CSV file into WKT format, for example: "
                                                 "python %s naifcodes_radii_m_wAsteroids_IAU2015.csv\n" % (
                                                     os.path.basename(sys.argv[0])
                                                 ),
                                     formatter_class=SmartFormatter,
                                     epilog="Authors: Trent Hare (USGS), Jean-Christophe Malapert (CNES)"
                                            " - License : Public Domain ",
                                     )
    parser.add_argument('csv', metavar='csv_file', nargs=1, help='data from IAU as CSV file')
    parser.add_argument('--output', metavar='output', nargs=1, help="output file (default is stdout)")
    parser.add_argument('--format', choices=['WKT'], help="output format (default is WKT)")
    parser.add_argument('--verbose', choices=['OFF', 'INFO', 'DEBUG'],
                        help="R|select the verbose mode on stdout (INFO is default) where:\n"
                             " OFF : do not display error,\n"
                             " INFO : display error,\n"
                             " DEBUG: display each input/output of each method\n")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s V1.0 (28/08/2018)',
                        help="show program's version number and exit.")
    args = parser.parse_args()

    # handling positional argument
    data = None
    if args.csv:
        data = args.csv[0]
        if not os.path.isfile(data):
            parser.error("File not found")

    # handling outputFile argument
    if args.output:
        outputFile = args.output[0]
    else:
        outputFile = sys.stdout

    # handling format argument
    if args.format:
        format = args.format
    else:
        format = "WKT"

    # handling verbose argument
    if args.verbose:
        if args.verbose != "OFF":
            verbose = logging.getLevelName(args.verbose)
            logger.setLevel(verbose)
        else:
            verbose = "OFF"
    else:
        verbose = logging.INFO
        logger.setLevel(verbose)

    if verbose == "OFF":
        logger.disabled = True
    else:
        logger.disabled = False

    try:
        wktList = loadAndProcessCatalog(data)
        logger.info("%s WKTs loaded from %s" % (len(wktList), data))
        saveAs(wktList, outputFile, format)
    except Exception as message:
        logger.error("Error: %s" % message)
        sys.exit(2)


if __name__ == "__main__":
    LEVEL_LOG = logging.INFO
    logger = logging.getLogger()
    logger.disabled = False
    initLogger(logger, LEVEL_LOG)
    sys.exit(main(sys.argv))

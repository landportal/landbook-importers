'''
Created on 13/01/2014

@author: Dani
'''

import os
import sys
import traceback
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir), 'CountryReconciler'))
sys.path.append(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir), "LandPortalEntities"))
sys.path.append(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir), "ModelToXml"))

from ConfigParser import ConfigParser
import logging
from es.weso.landmatrix.extractor.LandMatrixExtractorXML import LandMatrixExtractorXML
from es.weso.landmatrix.translator.land_matrix_translator import LandMatrixTranslator


def configure_log():
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(filename='land_matrix_extractor.log', level=logging.DEBUG, 
                        format=FORMAT)


def run():
    configure_log()
    log = logging.getLogger("lmextractor")
    config = ConfigParser()
    config.read("./config/configuration.ini")
    look_for_historical = config.getboolean("TRANSLATOR", "historical_mode")
    try:
        #xml_extractor = LandMatrixExtractorXML(log, config)
        #xml_extractor.run()
        pass
    except BaseException as execpp:
        log.error("While downloading data: " + execpp.message)
        raise RuntimeError()

    try:
        translator = LandMatrixTranslator(log, config, look_for_historical=look_for_historical)
        translator.run()
    except BaseException as execpp:
        #log.error("While trying to incorporate raw info into our model: " + execpp.message)
        e = sys.exc_info()[0]
        print "Error: %s" % e
	traceback.print_exc(file=sys.stdout)
        raise RuntimeError()



if __name__ == '__main__':
    try:
        run()
        print 'Done!'
    except BaseException as ex:
        print "Execution finalized with errors. Check log."
        e = sys.exc_info()[0]
        print "Error: %s" % e
    traceback.print_exc(file=sys.stdout)

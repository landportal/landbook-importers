'''
Created on 15/01/2014

@author: Dani
'''

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir), 'CountryReconciler'))
sys.path.append(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir), "LandPortalEntities"))
sys.path.append(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir), "ModelToXml"))

import logging
from es.weso.faostat.extractor.faostat_extractor import FaostatExtractor
from es.weso.faostat.translator.faostat_translator import FaostatTranslator
from ConfigParser import ConfigParser


def configure_log():
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(filename='faostat-asti.log', level=logging.INFO, 
                        format=FORMAT)


def run():
        config = ConfigParser()
        config_path = "./files/configuration-ASTI_Research_Spending.ini"
        config_path_org = "./files/configuration-FAO-ASTI.ini"
        config.read([config_path, config_path_org])
        log = logging.getLogger('faostat-asti-log')
        configure_log()
        look_for_historical = config.getboolean("TRANSLATOR", "historical_mode")
        try:
            csv_extractor = FaostatExtractor(log, config)
            csv_extractor.run()
        except BaseException as e:
            log.error("While tracking file: " + e.message)
            raise RuntimeError()

        try:
            csv_translator = FaostatTranslator(log, config, look_for_historical)
            csv_translator.run()
        except BaseException as e:
            log.error("While trying to turn raw info into xml: " + e.message)
            raise RuntimeError()

        with open(config_path, 'w') as configfile:
            config.write(configfile)




if __name__ == '__main__':
    try:
        run()
        print "Done!"
    except:
        print "Execution finalized with errors. Check logs. "
        e = sys.exc_info()[0]
        print "Error: %s" % e

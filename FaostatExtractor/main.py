'''
Created on 15/01/2014

@author: Dani
'''
import sys, getopt, traceback, os

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
    logging.basicConfig(filename='faostat.log', level=logging.INFO, 
                        format=FORMAT)

def main(argv):
   config_file = ''
   try:
      opts, args = getopt.getopt(argv,"hc:",["cfile="])
   except getopt.GetoptError:
      print 'main.py -c <inputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'main.py -c <inputfile>'
         sys.exit()
      elif opt in ("-c", "--config"):
         config_file = arg
   run(config_file)

def run(config_file):
	basepath = os.path.dirname(__file__)
	config_path = os.path.abspath(os.path.join(basepath, config_file)) #"./files/configuration-ASTI_Research_Spending.ini"
        config_path_org = os.path.abspath(os.path.join(basepath, "files/configuration-org-FAOSTAT.ini"))
        config = ConfigParser()
        config.read([config_path, config_path_org])
        log = logging.getLogger('faostat-log')
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
	    traceback.print_exc(file=sys.stdout)
            raise RuntimeError()

	# write the new configFile (content merged)
	new_config_path = os.path.abspath(os.path.join(basepath, config_file+".new"))
        with open(new_config_path, 'w') as configfile:
            config.write(configfile)




if __name__ == '__main__':
    try:
        main(sys.argv[1:])
        print "Done!"
    except:
        print "Execution finalized with errors. Check logs. "
        e = sys.exc_info()[0]
        print "Error: %s" % e
	traceback.print_exc(file=sys.stdout)

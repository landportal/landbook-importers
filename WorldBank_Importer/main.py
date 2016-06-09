import ConfigParser
import logging
import sys, traceback, os
import getopt

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir), "CountryReconciler"))
sys.path.append(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir), "LandPortalEntities"))
sys.path.append(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir), "ModelToXml"))

from es.weso.worldbank.parser.parser import Parser

__author__ = 'BorjaGB'

def configure_log():
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(filename='WorldBank.log', level=logging.INFO,
                        format=FORMAT)

def update_ini_file(config, config_path, importer, log):
    log.info("Updating ini file")
    config.set("TRANSLATOR", 'obs_int', importer._obs_int)
    config.set("TRANSLATOR", 'sli_int', importer._sli_int)
    config.set("TRANSLATOR", 'dat_int', importer._dat_int)
    config.set("TRANSLATOR", 'igr_int', importer._igr_int)
    
    if hasattr(importer, '_historical_year'):
        config.set("TRANSLATOR", 'historical_year', importer._historical_year)
    new_config_path = config_path+".new"
    with open(new_config_path, 'wb') as configfile:
        config.write(configfile)


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
    configure_log()
    log = logging.getLogger("worldbanklog")
    basepath = os.path.dirname(__file__)
    config_path = os.path.abspath(os.path.join(basepath, config_file))
    config_path_org = os.path.abspath(os.path.join(basepath, "config/configuration-org-WB.ini"))
    config = ConfigParser.RawConfigParser()
    config.read([config_path, config_path_org])

    try:
        wb_importer = Parser(config, log)
        wb_importer.run()
        update_ini_file(config, config_path, wb_importer, log)        
        log.info("Done!")
    
    except Exception as detail:
        log.error("OOPS! Something went wrong %s" %detail)

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
        print "Done!"
    except:
        print "Execution finalized with errors. Check logs. "
        e = sys.exc_info()[0]
        print "Error: %s" % e
traceback.print_exc(file=sys.stdout)


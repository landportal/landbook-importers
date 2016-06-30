import sys, getopt, traceback, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir), 'CountryReconciler'))
sys.path.append(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir), "LandPortalEntities"))
sys.path.append(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir), "ModelToXml"))
import logging

from es.weso.raw.importer.raw_importer import RawImporter

def configure_log():
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(filename='simple_xls_importer.log', level=logging.INFO, format=FORMAT)

def main(argv):
   input_file = ''
   try:
      opts, args = getopt.getopt(argv,"hi:",["cfile="])
   except getopt.GetoptError:
      print 'main.py -i <inputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'main.py -i <inputfile>'
         sys.exit()
      elif opt in ("-i", "--input"):
         input_file = arg
   run(input_file)

def run(input_file):
    configure_log()
    log = logging.getLogger("raw_importer")
 
    basepath = os.path.dirname(__file__)
    input_path = os.path.abspath(os.path.join(basepath, input_file))

    try:
        raw_importer = RawImporter(log, input_path)
        raw_importer.run()
    except BaseException as execpp:
        #log.error("While trying to incorporate raw info into our model: " + execpp.message)
        e = sys.exc_info()[0]
        print "Error: %s" % e
	traceback.print_exc(file=sys.stdout)
        raise RuntimeError()

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
        print "Done!"
    except:
        print "Execution finalized with errors. Check logs. "
        e = sys.exc_info()[0]
        print "Error: %s" % e
traceback.print_exc(file=sys.stdout)


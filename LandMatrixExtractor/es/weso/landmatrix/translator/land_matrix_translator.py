'''
Created on 22/01/2014

@author: Dani
'''

#from ConfigParser import ConfigParser
import codecs
import os, sys, traceback
import json
from lpentities.observation import Observation
from lpentities.value import Value
from lpentities.indicator import Indicator
from lpentities.computation import Computation
from lpentities.instant import Instant
from lpentities.measurement_unit import MeasurementUnit
from lpentities.dataset import Dataset
from lpentities.user import User
from lpentities.data_source import DataSource
from lpentities.license import License
from lpentities.organization import Organization
from es.weso.landmatrix.translator.deals_analyser import DealsAnalyser
from es.weso.landmatrix.translator.deals_builder import DealsBuilder
from .keys_dicts import KeyDicts
from datetime import datetime
from lpentities.year_interval import YearInterval
from model2xml.model2xml import ModelToXMLTransformer

try:
    import xml.etree.cElementTree as ETree
except:
    import xml.etree.ElementTree as ETree


class LandMatrixTranslator(object):
    '''
    classdocs
    '''

    INFO_NODE = "item"




    def __init__(self, log, config, look_for_historical):
        """
        Constructor

        """
        self._log = log
        self._config = config
        self._look_for_historical = look_for_historical

        #Initializing variable ids
        self._org_id = self._config.get("TRANSLATOR", "org_id")
        if self._look_for_historical:
            self._obs_int = 0
            self._sli_int = 0
            self._dat_int = 0
            self._igr_int = 0
        else:
            self._obs_int = int(self._config.get("TRANSLATOR", "obs_int"))
            self._sli_int = int(self._config.get("TRANSLATOR", "sli_int"))
            self._dat_int = int(self._config.get("TRANSLATOR", "dat_int"))
            self._igr_int = int(self._config.get("TRANSLATOR", "igr_int"))

        #Indicators's dict
        self._indicators_dict = self._build_indicators_dict()


        #Common objects
        self._default_user = self._build_default_user()
        self._default_organization = self._build_default_organization()
        self._default_datasource = self._build_default_datasource()
        self._default_dataset = self._build_default_dataset()
        self._default_license = self._build_default_license()
        self._default_computation = self._build_default_computation()

        self._relate_common_objects()


        self._latest_date_found = 0  # It will have a value during the executing. It will store the last date found.
    @staticmethod
    def _build_default_user():
        return User(user_login="LANDMATRIXIMPORTER")


    @staticmethod
    def _build_default_computation():
        return Computation(Computation.RAW)

    def _build_default_organization(self):
        result = Organization(chain_for_id=self._org_id)
        result.name = self._read_config_value("ORGANIZATION", "name")
        result.url = self._read_config_value("ORGANIZATION", "url")
        result.description_en = self._read_config_value("ORGANIZATION", "description_en")
        result.description_es = self._read_config_value("ORGANIZATION", "description_es")
        result.description_fr = self._read_config_value("ORGANIZATION", "description_fr")

        return result

    def _build_default_datasource(self):
        result = DataSource(chain_for_id=self._org_id,
                            int_for_id=self._config.get("DATASOURCE", "id"))
        result.name = self._config.get("DATASOURCE", "name")
        return result

    def _build_default_dataset(self):
        result = Dataset(chain_for_id=self._org_id, int_for_id=self._dat_int)
        self._dat_int += 1  # Needed increment

        for key in self._indicators_dict:
            result.add_indicator(self._indicators_dict[key])
        result.frequency = Dataset.YEARLY
        return result

    def _build_default_license(self):
        result = License()
        result.republish = self._config.get("LICENSE", "republish")
        result.description = self._config.get("LICENSE", "description")
        result.name = self._config.get("LICENSE", "name")
        result.url = self._config.get("LICENSE", "url")

        return result

    def _relate_common_objects(self):
        self._default_organization.add_user(self._default_user)
        self._default_organization.add_data_source(self._default_datasource)
        self._default_datasource.add_dataset(self._default_dataset)
        self._default_dataset.license_type = self._default_license
        #No return needed


    def run(self):
        """
        Translates the downloaded data into model objects. look_for_historical is a boolean
        that indicates if we have to consider old information or only bear in mind actual one

        """
        try:
            info_nodes = self._get_info_nodes_from_file()
	    self._log.info("Number of info_nodes read = %i" %len(info_nodes))
            deals = self._turn_info_nodes_into_deals(info_nodes)
	    self._log.info("Number of info_nodes turn into deals = %i" %len(deals))
            deal_entrys = self._turn_deals_into_deal_entrys(deals)
	    self._log.info("Number of deals turn into deal_entries = %i" %len(deal_entrys))
            observations = self._turn_deal_entrys_into_obs_objects(deal_entrys)
	    self._log.info("Number of observations generated = %i" %len(observations))
            for obs in observations:
                self._default_dataset.add_observation(obs)
        except BaseException as e:
            raise RuntimeError("Error while trying to build model objects: " + e.message)

        m2x = ModelToXMLTransformer(dataset=self._default_dataset,
                                    import_process=ModelToXMLTransformer.XML,
                                    user=self._default_user,
                                    path_to_original_file=self._path_to_original_file())
        try:
            m2x.run()
            self._actualize_config_values()
        except BaseException as e:
            raise RuntimeError("Error wuile sendig info to te receiver module: " + e.message)

    def _path_to_original_file(self):
        raw_path = self._config.get("LAND_MATRIX", "target_file")
        return os.path.abspath(raw_path)

    def _actualize_config_values(self):
        self._config.set("TRANSLATOR", "obs_int", self._obs_int)
        self._config.set("TRANSLATOR", "dat_int", self._dat_int)
        self._config.set("TRANSLATOR", "sli_int", self._sli_int)
        self._config.set("TRANSLATOR", "igr_int", self._igr_int)

        with open("./files/configuration.ini", 'wb') as config_file:
            self._config.write(config_file)


    def _turn_deal_entrys_into_obs_objects(self, deal_entrys):
        result = []
        for key in deal_entrys:
            new_obs = self._turn_deal_entry_into_obs(deal_entrys[key])
            if self._pass_filters(new_obs):
                result.append(new_obs)  # The method returns a list
        return result

    def _pass_filters(self, obs):
        if self._look_for_historical:
            return True
        if not "_target_date" in self.__dict__:
            self._target_date = self._get_current_date()
        elif self._get_year_of_observation(obs) < self._target_date:
            return False
        return True


    @staticmethod
    def _get_year_of_observation(obs):
        date_obj = obs.ref_time
        if type(date_obj) == YearInterval:
            return int(date_obj.year)
        else:
            raise RuntimeError("Unexpected object date. Impossible to build observation from it: " + type(date_obj))


    def _get_current_date(self):
        return int(self._config.get("HISTORICAL", "first_valid_year"))

    def _turn_deal_entry_into_obs(self, deal_entry):
        result = Observation(chain_for_id=self._org_id, int_for_id=self._obs_int)
        self._obs_int += 1  # Updating obs id

        #Indicator
        result.indicator = deal_entry.indicator
        #Value
        result.value = self._build_value_object(deal_entry)  # Done
        #Computation
        result.computation = self._default_computation
        #Issued
        result.issued = self._build_issued_object()  # No param needed
        #ref_time
        result.ref_time = self._build_ref_time_object(deal_entry)  # Done
        #country
        deal_entry.country.add_observation(result)  # And that establish the relationship in both directions

        return result

    @staticmethod
    def _build_issued_object():
        return Instant(datetime.now())

    def _build_ref_time_object(self, deal_entry):
        if deal_entry.date is not None:
            return YearInterval(deal_entry.date)
        else:
            return YearInterval(self._latest_date_found)


    @staticmethod
    def _build_value_object(deal_entry):
        result = Value()
        result.value = deal_entry.value
        result.value_type = Value.INTEGER
        result.obs_status = Value.AVAILABLE
        return result


    def _turn_deals_into_deal_entrys(self, deals):
        analyser = DealsAnalyser(deals, self._indicators_dict)
        result = analyser.run()
        self._latest_date_found = analyser.latest_date
        return result


    def _turn_info_nodes_into_deals(self, info_nodes):
        result = []
        for info_node in info_nodes:
            try:
		self._log.debug("Parsing deal id = " + info_node.findtext("./field[@name='deal_id']").strip())
		deal = DealsBuilder.turn_node_into_deal_object(info_node)
		self._log.debug("Parsing finished of deal = " + str(deal))
                result.append(deal)
            except BaseException as ex:
                self._log.warning("Problem while parsing a node of a deal. Deal will be ignored. Cause: " + ex.message)
		e = sys.exc_info()[0]
	        print "Error: %s" % e
		traceback.print_exc(file=sys.stdout)
        return result

    def _get_info_nodes_from_file(self):
        """
        Return a list of node objects that contains

        """
        file_path = self._config.get("LAND_MATRIX", "target_file")
        try:
            content_file = codecs.open(file_path, encoding="utf-8")
            lines = content_file.read()
            content_file.close()
            return ETree.fromstring(lines.encode(encoding="utf-8"))
        except:
            raise RuntimeError("Impossible to parse xml in path: {0}. \
                    It looks that it is not a valid xml file.".format(file_path))


    def _build_indicators_dict(self):

        # Possibilities. Putting this ugly and huge code here, or refactor it, charging properties using
        # patterns: *_name_en, *_name_fr...
        # If i do that, we will have much less code, but we must to ensure that the property names never change.
        # I am not sure of which one is the most dangerous option, but also i'm not sure about if
        # that is a question that deserves to waste time with it. So huge and ugly code.

        hectares = MeasurementUnit(name="hectares",
                                   convert_to=MeasurementUnit.SQ_KM,
                                   factor=0.01)
        units = MeasurementUnit(name="units",
                                convert_to=MeasurementUnit.UNITS)
        default_topic = 'LAND_USE'

        result = {}

        indicator_codes = json.loads(self._config.get("INDICATORS", "codes"))
        self._log.info("Init process to add %d indicators in the indicators dictionary" %len(indicator_codes))
        for indicator in indicator_codes:
            try:
              id = int(self._read_config_value(indicator, "id"))
              ind = Indicator(chain_for_id=self._org_id, int_for_id=id)
              ind.name_en = self._read_config_value(indicator, "name_en")
              ind.name_es = self._read_config_value(indicator, "name_es")
              ind.name_fr = self._read_config_value(indicator, "name_fr")
           
              ind.description_en = self._read_config_value(indicator, "desc_en")
              ind.description_es = self._read_config_value(indicator, "desc_es")
              ind.description_fr = self._read_config_value(indicator, "desc_fr")
              ind.topic = default_topic # TODO improve
              ind.preferable_tendency = Indicator.IRRELEVANT # TODO improve
              ind.measurement_unit = self._get_unit("UNITS")#TODO
              # Generate a code using the patter ITEM_CODE-ELEMENT_CODE
              generated_code = id
              result[generated_code] = ind # Add the indicator in the dictionary
    	    except:
              print("exception on id") #TODO improve exception

        self._log.info("Added %d indicators in the indicators dictionary" % len(result))
        return result


    def _read_config_value(self, section, field):
        return (self._config.get(section, field)).decode(encoding="utf-8")

    @staticmethod
    def _get_unit(unit):
        hectares = MeasurementUnit(name="hectares",
                                   convert_to=MeasurementUnit.SQ_KM,
                                   factor=0.01)
        units = MeasurementUnit(name="units",
                                convert_to=MeasurementUnit.UNITS)
	unit = unit.upper()

        if unit == "UNITS":
           return units
        elif unit == "HECTARES":
	   return hectares
        else:
           raise ValueError("No valid units value: %s" %unit)

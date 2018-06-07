from datetime import datetime

from lpentities.computation import Computation
from lpentities.data_source import DataSource
from lpentities.dataset import Dataset
from lpentities.indicator import Indicator
from lpentities.instant import Instant
from lpentities.interval import Interval
from lpentities.license import License
from lpentities.measurement_unit import MeasurementUnit
from lpentities.month_interval import MonthInterval
from lpentities.observation import Observation
from lpentities.organization import Organization
from lpentities.user import User
from lpentities.value import Value
from lpentities.year_interval import YearInterval
from model2xml.model2xml import ModelToXMLTransformer
from reconciler.country_reconciler import CountryReconciler

from es.weso.raw.ExcelManagement.excel_reader import XslReader

class RawImporter(object):

    def __init__(self, log, file_path):
        self._log = log
        self._file_path = file_path
        self._look_for_historical = True # TODO review this value
        self._reconciler = CountryReconciler()

        # Initializing variable ids
        self._ind_int = 0
        self._obs_int = 0
        self._sli_int = 0
        self._igr_int = 0

        # Building parsing instances
        self._xsl_reader = self._build_xsl_reader()
        
        # Excel data
        self._metadata_sheet_dictionary = self._load_metadata_data()
        self._org_id = self._metadata_sheet_dictionary["org_acronym"]
        self._dataset_internal_id = self._metadata_sheet_dictionary["dataset_internal_id"]
        self._indicator_internal_id = self._metadata_sheet_dictionary["indicator_internal_id"]
        self._read_as = self._metadata_sheet_dictionary["read_as"]

#        self._indicator = self._build_indicator(self._indicator_internal_id)
        
        self._organization = self._build_organization()
        self._license = self._build_license()
                
        # Building common objects
        self._default_user = self._build_default_user()
        self._datasource = self._build_default_datasource()
        self._dataset = self._build_default_dataset()
        self._relate_common_objects()
        self._default_computation = Computation(uri=Computation.RAW)

    def run(self):
        """
        Steps:

        This method is going to work as importer and object builder simultaneously:
        Steps:
         - Build common objects. (In constructor)
         - Consider every data as a member of the same dataset. (In constructor)
         - for available years, or needed years,(for every month) call to API. HERE WE START THE RUN
         - Build an observation object for each indicator tracked.
         - Add observation to dataset
         - Send it to model2xml
         - Actualize config values (ids and last checked)
        """

	self._log.info("--- Start processing file="+self._file_path)

        # Generate observations and add it to the common objects

        if self._read_as == "country_year_value":
            observations = self._load_observations_data_country_year_value()
        elif self._read_as == "indicator_country_year_value":
            observations = self._load_observations_indicator_country_year_value()
        elif self._read_as == "country_multiple_values":
            observations = self._load_observations_data_multiple_columns_by_year()
        else:
	    raise ValueError("Unkown value for read as: " + self._read_as)

        if len(observations) > 0:
            for obs in observations :
                self._dataset.add_observation(obs)
        else:
            print "No observations found"

        # Send model for its intermediate XML translation
        translator = ModelToXMLTransformer(self._dataset, "XLS", self._default_user, "FILE_PATH")
        translator.run()

        # And it is done. No return needed

	self._log.info("--- End Processing file="+self._file_path)

    def _build_xsl_reader(self):
        return XslReader()
    
    def _load_metadata_data(self):
	return self._xsl_reader.load_metadata_sheet(self._file_path)

    def _build_indicator(self, internal_id):
        self._ind_int+=1
        return Indicator(chain_for_id=self._org_id,
                         int_for_id=internal_id,
                         measurement_unit= MeasurementUnit(name= "FIXME",
                                                           convert_to = "FIXME",
                                                           )
			 )
    
    def _build_organization(self):
        return Organization(chain_for_id=self._org_id)

    def _build_license(self): # TODO remove this license
        return License()
    
    def _load_observations_indicator_country_year_value(self):
        result = []
        data = self._xsl_reader.load_xsl_indicator_country_year_value(self._file_path)
        for i in range(1, len(data)):
            indicator_internal_id = data[i]['indicator']
            indicator = self._build_indicator(indicator_internal_id)
            raw_country = data[i]['country']
            country = self._get_country(raw_country)
            if country is None:
		self._log.warning("In line=%d, unkown country=%s" %(i,raw_country))
                continue

            year = self._build_ref_time_object(data[i]['year'])

            raw_value = data[i]['value']
            if not(_is_valid_value(raw_value)):
		self._log.warning("Not valid value = " + str(raw_value))
                continue
                # TODO add some log
            value = self._build_value_object(raw_value)

	    note = None
            if 'note' in data[i]:
		note = data[i]['note']

            result.append(self._build_observation_for_cell(year, value, country, indicator, note))

        return result


    def _load_observations_data_multiple_columns_by_year(self):
        result = []
        indicator = self._build_indicator(self._indicator_internal_id)
        data = self._xsl_reader.load_xsl_country_year_value(self._file_path)
        for i in range(1, len(data)):
            country = self._get_country(data[i][0])
            if country is not None :
                for j in range(1, len(data[0])):
                    year = self._build_ref_time_object(data[0][j])
                    raw_value = data[i][j]
                    if _is_valid_value(raw_value):
                       value = self._build_value_object(raw_value)
                       # Add only if there is a value
                       result.append(self._build_observation_for_cell(year, value, country, indicator))
        return result

    def _load_observations_data_country_year_value(self):
        result = []
        indicator = self._build_indicator(self._indicator_internal_id)
        data = self._xsl_reader.load_xsl_country_year_value(self._file_path)

        for i in range(1, len(data)):
            raw_country = data[i]['country']
            country = self._get_country(raw_country)
            if country is None:
		self._log.warning("In line=%d, unkown country=%s" %(i,raw_country))
                continue

            year = self._build_ref_time_object(data[i]['year'])

            raw_value = data[i]['value']
            if not(_is_valid_value(raw_value)):
		self._log.warning("Not valid value = " + str(raw_value))
                continue
                # TODO add some log
            value = self._build_value_object(raw_value)

	    note = None
            if 'note' in data[i]:
		note = data[i]['note']

            result.append(self._build_observation_for_cell(year, value, country, indicator, note))

        return result
    
    def _filter_historical_observations(self, year):
        if self._look_for_historical:
            return True
        else :
            if isinstance(year, YearInterval):
                return year.year > self._historical_year
            else:
                return year.end_time > self._historical_year 
    
    def _build_observation_for_cell(self, year, value, country, indicator, note=None):
        result = Observation(chain_for_id=self._org_id, int_for_id=self._obs_int)
        self._obs_int += 1  # Updating id value
        result.indicator = indicator
        result.value = value
        result.computation = self._get_computation_object()  # Always the same, no param needed
        result.issued = self._build_issued_object()  # No param needed
        result.note = note
        result.ref_time = year
        country.add_observation(result)  # And that stablish the relation in both directions
        
        return result
    
    def _build_ref_time_object(self, time):
        if self._dataset.frequency == Dataset.MONTHLY:
            months = str(time).split("-")
            if len(months) == 1:
                month_time = months[0].split("/") #01/1990
                return MonthInterval(year = month_time[1], month = month_time[0])
            else:
                return Interval(frequency = Interval.MONTHLY, start_time=months[0], end_time=months[1])
        else:
            years = str(time).split("-")
            if len(years) == 1:
                return YearInterval(year=int(time))
            else :
                return Interval(start_time=int(years[0]), end_time=int(years[1]))
            
    def _build_issued_object(self):
        return Instant(datetime.now())

    def _get_computation_object(self):
        return self._default_computation

    @staticmethod
    def _build_value_object(value):
        result = Value(value=None,
                       value_type=Value.MISSING,
                       obs_status=Value.MISSING)
        if _is_valid_value(value):
	   if isinstance(value, int):
              result.value = value
              result.value_type = Value.INTEGER
              result.obs_status = Value.AVAILABLE
	   elif isinstance(value, float):
              result.value = value
              result.value_type = Value.FLOAT
              result.obs_status = Value.AVAILABLE
	   elif isinstance(value, basestring):
              result.value = value
              result.value_type = Value.STRING
              result.obs_status = Value.AVAILABLE
        return result

    
    def _get_country(self, country):
        result = None
        try: 
            result = self._reconciler.get_country_by_iso3(country)
        except:
            pass

	if result is None:
           try:
               result = self._reconciler.get_country_by_en_name(country)
           except:
               pass

	if result is None:
	   self._log.warning("Unkwon country = " + country)
        return result

    def _build_default_user(self):
        return User(user_login="RAWIMPORTER")

    def _build_default_datasource(self):
        result = DataSource(chain_for_id=self._org_id,
                            int_for_id=1)
        result.name = "FIXME"
        
        return result

    def _build_default_dataset(self):
        result = Dataset(chain_for_id=self._org_id, int_for_id=self._dataset_internal_id)
        result.frequency = Dataset.YEARLY

        return result

    def _relate_common_objects(self):
        self._organization.add_user(self._default_user)
        self._organization.add_data_source(self._datasource)
        self._datasource.add_dataset(self._dataset)
        self._dataset.license_type = self._license
        # No return needed

# Checks if the value is not: None, "-" or blank
def _is_valid_value(value):
   if isinstance(value, basestring):
      if (value is not None) and (value.strip()!="-") and (value.strip() !=""):
         return True
      else:
         return False
   else:
      if (value is not None) and (value !=""):
         return True
      else:
         return False


"""
Created on 18/12/2013

@author: Nacho, BorjaGB
"""
from datetime import datetime

from lpentities.computation import Computation
from lpentities.data_source import DataSource
from lpentities.dataset import Dataset
from lpentities.indicator import Indicator
from lpentities.instant import Instant
from lpentities.license import License
from lpentities.measurement_unit import MeasurementUnit
from lpentities.observation import Observation
from lpentities.organization import Organization
from lpentities.slice import Slice
from lpentities.user import User
from lpentities.value import Value
from lpentities.year_interval import YearInterval
from reconciler.country_reconciler import CountryReconciler
from model2xml.model2xml import ModelToXMLTransformer
from requests.exceptions import ConnectionError

from es.weso.worldbank.rest.rest_client import RestClient


class Parser(object):
    countries = {}
    observations = []


    def __init__(self, config, log):
        self.logger = log
        self.config = config
        self._reconciler = CountryReconciler()

        self._look_for_historical = self.config.getboolean("TRANSLATOR", "historical_mode")
        if not self._look_for_historical:
            self._historical_year = self.config.getint("TRANSLATOR", "historical_year")

        self._org_id = self.config.get("ORGANIZATION", "acronym")
        self._obs_int = self.config.getint("TRANSLATOR", "obs_int")
        self._sli_int = self.config.getint("TRANSLATOR", "sli_int")
        self._dat_int = self.config.getint("TRANSLATOR", "dat_int")
        self._igr_int = self.config.getint("TRANSLATOR", "igr_int")

        self.countries_url = self.config.get('URLs', 'country_list')
        self.observations_url = self.config.get('URLs', 'indicator_pattern')
        self.data_sources = dict(self.config.items('data_sources'))

        self._organization = self._build_default_organization()
        self._user = self._build_default_user()
        self._license = self._build_default_license()


    def run(self):
        self.extract_countries()
        self.extract_observations()
        self.model_to_xml()


    def model_to_xml(self):
        for datasource in self._user.organization.data_sources:
            for dataset in datasource.datasets:
                if len(dataset.observations) > 0:
                    transformer = ModelToXMLTransformer(dataset,
                                                        ModelToXMLTransformer.API,
                                                        self._user,
                                                        self.config.get("URLs","base_api"))
                    transformer.run()
                else:
                    self.logger.warning("Dataset %s has no observations"%dataset.dataset_id)

    def extract_countries(self):
        response = RestClient.get(self.countries_url, {"format": "json"})
        countries_response = response[1]
        for possible_country in countries_response:
            try:
                country = self._reconciler.get_country_by_iso2(possible_country['iso2Code'])
                self.countries[country.iso3] = country
            except:
                self.logger.warning("No country matches found for iso code=" + possible_country['iso2Code'])

    def _build_default_organization(self):
        return Organization(chain_for_id=self._org_id,
                            name=self.config.get("ORGANIZATION", "name"),
                            url=self.config.get("ORGANIZATION", "url"),
                            url_logo=self.config.get("ORGANIZATION", "url_logo"),
                            description_en=self._read_config_value("ORGANIZATION", "description_en"),
                            description_es=self._read_config_value("ORGANIZATION", "description_es"),
                            description_fr=self._read_config_value("ORGANIZATION", "description_fr"),
                            acronym=self.config.get("ORGANIZATION", "acronym"))

    def _read_config_value(self, section, field):
        return (self.config.get(section, field)).decode(encoding="utf-8")

    def _build_default_user(self):
        return User(user_login="worldbank_importer",
                         organization=self._organization)

    def _build_default_license(self):
        return License(name=self.config.get("LICENSE", "name"),
                       description=self.config.get("LICENSE", "description"),
                       republish=self.config.get("LICENSE", "republish"),
                       url=self.config.get("LICENSE", "url"))

    def _build_data_source(self, data_source_name):
        data_source = DataSource(chain_for_id=self._org_id,
                                 int_for_id=self.config.get("datasource", "datasource_id"),
                                 name=data_source_name,
                                 organization=self._organization)
        return data_source

    def _build_data_set(self, data_source):
        frequency = Dataset.YEARLY
        dataset = Dataset(chain_for_id=self._org_id,
                              int_for_id=self.config.get("datasource", "datasource_id"),
                              frequency=frequency,
                              license_type=self._license,
                              source=data_source)
        self._dat_int += 1  # Updating dataset int id value
        return dataset

    def _build_indicator(self, indicator_code, dataset, measurement_unit):
        indicator = Indicator(chain_for_id=self._org_id,
                              int_for_id=self.config.get(indicator_code, "indicator_id"),
                              name_en=self.config.get(indicator_code, "name_en").decode(encoding="utf-8"),
                              name_es=self.config.get(indicator_code, "name_es").decode(encoding="utf-8"),
                              name_fr=self.config.get(indicator_code, "name_fr").decode(encoding="utf-8"), 
                              description_en=self.config.get(indicator_code, "desc_en").decode(encoding="utf-8"),
                              description_es=self.config.get(indicator_code, "desc_es").decode(encoding="utf-8"),
                              description_fr=self.config.get(indicator_code, "desc_fr").decode(encoding="utf-8"),
                              dataset=dataset,
                              measurement_unit=measurement_unit,
                              preferable_tendency=self._get_preferable_tendency_of_indicator(self.config.get(indicator_code, "indicator_tendency")),
                              topic=self.config.get(indicator_code, "indicator_topic"))

        return indicator

    def _build_slice(self, country, dataset, indicator):
        slice_object = Slice(chain_for_id=self._org_id,
                      int_for_id=self._sli_int,
                      dimension=country,
                      dataset=dataset,
                      indicator=indicator)
        self._sli_int += 1  # Updating int id slice value

        return slice_object

    def _build_value(self, indicator, country, date, value_element):
        value_object = Value(value_element,
                             Value.FLOAT,
                             Value.AVAILABLE)
        if value_object.value is None:
            value_object = Value(None,
                                 None,
                                 Value.MISSING)
            self.logger.warning('Missing value for ' + indicator.name_en + ', ' + country.name + ', ' + date)

        return value_object

    def _filter_historical_observations(self, year):
        if self._look_for_historical:
            return True
        else :
            if isinstance(year, YearInterval):
                return year.year > self._historical_year
            else:
                return year.end_time > self._historical_year

    def _build_observation(self, indicator, dataset, country, value, date):
        value_object = self._build_value(indicator,
                                         country,
                                         date,
                                         value)

        time = YearInterval(year=int(date))
        observation = Observation(chain_for_id=self._org_id,
                                  int_for_id=self._obs_int,
                                  ref_time=time,
                                  issued=Instant(datetime.now()),
                                  computation=Computation(Computation.RAW),
                                  value=value_object,
                                  indicator=indicator,
                                  dataset=dataset)
        self._obs_int += 1  # Updating obs int value

        return observation

    def extract_observations(self):
        for data_source_name in self.data_sources:
            indicators_section = self.config.get('data_sources', data_source_name)
            requested_indicators = dict(self.config.items(indicators_section))

            data_source = self._build_data_source(data_source_name)
            self._organization.add_data_source(data_source)
            dataset = self._build_data_set(data_source)
            data_source.add_dataset(dataset)

            # Iterate over the indicators
            for indicator_element in requested_indicators:
                indicator_code = self.config.get(indicators_section, indicator_element)
                measurement_unit = MeasurementUnit(name = self.config.get(indicator_code, "indicator_unit_name"),
                                                   convert_to = self.config.get(indicator_code, "indicator_unit_type"))
                indicator = self._build_indicator(indicator_code, dataset, measurement_unit)

                print '\t' + indicator.name_en  + "--------------" + indicator.preferable_tendency + "-----------"

                # Create an slice by country
                slice_by_country={}
                for iso3, country in self.countries.iteritems():
                    slice_object = self._build_slice(country, dataset, indicator)
                    slice_by_country[iso3] = slice_object

                # Compound the URL to request
                uri = self.observations_url.replace('{INDICATOR.CODE}', indicator_code)
                self.logger.info(uri)

                try:
                   response = RestClient.get(uri, {"format": "json"})
                   response_info = response[0]
		   if response_info['pages'] != 1:
			print "The URL request needs pagination"
			self.logger.error("The URL request needs pagination")
			sys.exit(1)
                   observations = response[1]
                   if observations is not None:
                      self.logger.info("Number of observations harvested="+str(len(observations)))
                      for observation_element in observations:
                         iso3code = observation_element['countryiso3code']
                         if (iso3code is None) or iso3code=="":
                            iso3code = observation_element['country']['id']
                            if (iso3code is None) or iso3code=="":
                              self.logger.warning("Skip the observation. Neither countryiso3code or nor country->id in observation: " + str(observation_element))
                              continue # pass to the next observation

                         if iso3code in self.countries:
                            country = self.countries[iso3code]
                         else:
                            self.logger.warning("Skip the observation. Not country returned by country_reconcilier using the iso3code: " + iso3code + " observation=" + str(observation_element))
                            continue # pass to the next observation

                         value = observation_element['value']
                         if value is not None: # Only create an observation if there is a value for it
                            observation = self._build_observation(indicator, dataset, country, observation_element['value'], observation_element['date'])
                            if self._filter_historical_observations(observation.ref_time):
                               country.add_observation(observation)
                               dataset.add_observation(observation)
                               slice_by_country[iso3code].add_observation(observation)
                except (KeyError, ConnectionError, ValueError):
                   self.logger.error('Error retrieving response for \'' + uri + '\'')

                # Add the slices to the dataset
                for slice in slice_by_country.itervalues():
                   if len(slice.observations) > 0:
			dataset.add_slice(slice)

                self.logger.info("FINISHED: " + indicator.name_en)

    @staticmethod
    def _get_preferable_tendency_of_indicator(tendency):
        if tendency.lower() == "decrease":
            return Indicator.DECREASE
        else:
            return Indicator.INCREASE

# coding=utf-8
__author__ = 'Dani'


from lpentities.observation import Observation
from lpentities.value import Value
from lpentities.indicator import Indicator
from lpentities.computation import Computation
from lpentities.instant import Instant
from lpentities.country import Country
from lpentities.measurement_unit import MeasurementUnit
from lpentities.dataset import Dataset
from lpentities.user import User
from lpentities.data_source import DataSource
from lpentities.license import License
from lpentities.organization import Organization


from .dates_builder import get_model_object_time_from_parsed_string
from ..dataset_user_pair import DatasetUserPair

from datetime import datetime
class IpfriModelObjectBuilder(object):

    def __init__(self, parsed_indicators, parsed_dates, parsed_countries, dataset_name):

        self.parsed_indicators = parsed_indicators
        self.parsed_dates = parsed_dates
        self.parsed_countries = parsed_countries
        self.dataset_name = dataset_name

        self.indicators_dict = {}
        self.dates_dict = {}
        self.countries_dict = {}

        self.dataset = None
        self.user = None

        print len(parsed_indicators)


    def run(self):
        self.prepare_base_hierarchy_objects()
        self.complete_indicators_dict()
        self.complete_dates_dict()
        self.complete_countries_dict()
        self.fetch_elements_by_index_and_translate()
        return DatasetUserPair(self.dataset, self.user)


    def prepare_base_hierarchy_objects(self):
        #Building dataset
        self.dataset = Dataset(dataset_id=self.dataset_name)  # Change TODO
        self.dataset.name = self.dataset_name
        self.dataset.frequency = "yearly"

        #Building license
        new_license = License()
        new_license.name = "IPFRI Copyright"
        new_license.description = "Attribution, no modification and non commercial without permission."
        new_license.republish = True
        new_license.url = "http://www.ifpri.org/copyright"

        self.dataset.license_type = new_license

        #building datasource
        new_datasource = DataSource(source_id="IPFRI")
        new_datasource.name = "IFPRI - International Food Policy Research Institute"

        new_datasource.add_dataset(self.dataset)

        # Building organization
        new_organization = Organization()
        new_organization.name = "IFPRI - International Food Policy Research Institute"
        new_organization.url = "http://www.ifpri.org/"

        new_organization.add_data_source(new_datasource)

        #Building user
        self.user = User("IPFRIImporter")
        self.user.ip = "156.35.80.80"  # Change TODO
        self.user.timestamp = datetime.now()

        new_organization.add_user(self.user)


    def complete_countries_dict(self):
        for pcountry in self.parsed_countries:
            new_country = self.TEMPORAL_RECONCILIAR_PAIS(pcountry)
            self.countries_dict[new_country.name] = new_country

    def TEMPORAL_RECONCILIAR_PAIS(self, pcountry):  # TODO: Communicate with CountryReconciler
        new_country = Country()
        new_country.iso2 = pcountry.name.replace(" ", "")
        new_country.iso3 = pcountry.name.replace(" ", "")
        new_country.name = pcountry.name

        return new_country

    def complete_dates_dict(self):
        for pdate in self.parsed_dates:
            time_object = get_model_object_time_from_parsed_string(pdate.string_date)
            self.dates_dict[pdate.string_date] = time_object


    def complete_indicators_dict(self):
        default_unit = MeasurementUnit("%")
        i = 0
        for pindicator in self.parsed_indicators:
            i += 1
            new_indicator = Indicator()
            new_indicator.indicator_id = "indicator_id" + str(i)  # Change! TODO
            new_indicator.name = pindicator.name
            new_indicator.description = pindicator.name
            new_indicator.measurement_unit = default_unit
            self.indicators_dict[pindicator.name] = new_indicator
            #Completing dataset object
            self.dataset.add_indicator(new_indicator)


    def fetch_elements_by_index_and_translate(self):
        for pdate in self.parsed_dates:
            pindicator = self.find_pindicator_by_pdate(pdate)
            for pcountry in self.parsed_countries:
                self.generate_observation_with_model_objects(pindicator, pdate, pcountry)

    def generate_observation_with_model_objects(self, pindicator, pdate, pcountry):
        #Building obs
        excell_value = self.look_for_value_in_a_pdate(pdate, pcountry)
        new_obs = Observation()
        new_obs.id = "obsid"  # Change! TODO
        self.add_value_object_to_observation(excell_value, new_obs)
        self.add_indicator_object_to_observation(pindicator, new_obs)
        self.add_computation_object_to_observation(excell_value, new_obs)
        self.add_issued_object_to_observation(new_obs)
        self.add_ref_time_object_to_observation(pdate, new_obs)
        self.add_country_object_to_observation(pcountry, new_obs)

        #Adding complete obs to dataset
        self.dataset.add_observation(new_obs)



    def add_country_object_to_observation(self, pcountry, new_obs):
        country_object = self.countries_dict[pcountry.name]
        country_object.add_observation(new_obs)
        #No return needed. Modyfing new_obs object

    def add_ref_time_object_to_observation(self, pdate, new_obs):
        new_obs.ref_time = self.dates_dict[pdate.string_date]
        #No return. Modifying received new_obs

    def add_issued_object_to_observation(self, new_obs):
        new_issued = Instant(datetime.now())
        new_obs.issued = new_issued
        #No return. Modifying received new_obs

    def add_computation_object_to_observation(self, excell_value, new_obs):
        if excell_value is None or not excell_value.estimated:
            if not self.__dict__.has_key("default_raw"):
                self.default_raw = Computation(uri=Computation.RAW)
            new_obs.computation = self.default_raw
        else:
            if not self.__dict__.has_key("default_estimated"):
                self.default_estimated = Computation(uri=Computation.ESTIMATED)
            new_obs.computation = self.default_estimated

        # No returning sentence needed


    def add_indicator_object_to_observation(self, pindicator, new_obs):
        new_obs.indicator = self.indicators_dict[pindicator.name]

    def add_value_object_to_observation(self,excell_value, new_obs):
        obs_value = Value()

        if excell_value is None:
            obs_value.value = None
            obs_value.obs_status = Value.MISSING
            obs_value.value_type = "float"
        else:
            obs_value.value = excell_value.value
            obs_value.obs_status = Value.AVAILABLE
            obs_value.value_type = "float"

        new_obs.value = obs_value
        # No return sentence needed. Modifying received new_obs object


    def look_for_value_in_a_pdate(self, pdate, pcountry):
        """
        If the value exist, it returns it. Elsewhere, it returns None

        """
        for a_value in pcountry.values:
            if pdate.beg_col <= a_value.column <= pdate.end_col:
                return a_value
        return None  # We reach this sentence only if the loop ends without executing the if´s body



    def find_pindicator_by_pdate(self, pdate):
        for pindicator in self.parsed_indicators:
            if pdate.beg_col >= pindicator.beg_col and pdate.end_col <= pindicator.end_col:
                return pindicator
        raise RuntimeError("Unable to find indicator to the date {0}".format(pdate.string_date))

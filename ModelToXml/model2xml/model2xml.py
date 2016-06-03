# coding=utf-8
"""
Created on 03/02/2014

@author: Dani
"""
from __future__ import unicode_literals
from lpentities.computation import Computation
from lpentities.country import Country
import zipfile


try:
    from xml.etree.cElementTree import Element, ElementTree
except:
    from xml.etree.ElementTree import Element, ElementTree
from lpentities.interval import Interval
from lpentities.instant import Instant
from lpentities.month_interval import MonthInterval
from lpentities.year_interval import YearInterval
from lpentities.time import Time
from lpentities.region import Region

from ConfigParser import ConfigParser

import codecs
import os
import requests


class ModelToXMLTransformer(object):
    """
    classdocs
    """

    XML = "XML"
    XLS = "XLS"
    CSV = "CSV"
    API = "API"
    JSON = "JSON"
    SCRAP = "SCRAP"

    def __init__(self, dataset, import_process, user, path_to_original_file, indicator_relations=None):
        """
        Constructor:
         - dataset: lpentities.dataset object containing most of the info
         - user: user that strat the importation process. According to the model, it is not possible to
        obtain it form the dataset
         - import_proces: string chain that summarizes the way in which data were taken from the source: excell, api,...
         - indicator_relations: list with lpentities.IndicatorRelationship objects

        """
        self._datasource = dataset.source
        self._dataset = dataset
        self._user = user
        self._import_process = import_process
        self._root = None
        self._indicator_dic = {}  # It will store an indicator object with it id as key.
        self._group_dic = {}
        self._indicator_relations = indicator_relations
        self._path_to_original_file = path_to_original_file
        self._zip_file_name = self._zip_file_name()
        # One per indicator referred by the observations

        self._config = self._build_internal_config()
        self._adapt_user()  # In the final version the user sent in the xml will be always the same.
                            # The importers don't have to specify

        self._root = self._build_root()

    #
    # Const containing names of tag or attributtes
    # to use in the XML file
    #
    ROOT = "dataset"
    ROOT_ID = "id"
    INDICATORS = "indicators"

    SLICES = "slices"
    SLICE = "slice"
    SLICE_METADATA = "sli_metadata"
    SLICE_ATT_ID = "id"
    SLICE_REFERRED = "referred"

    OBSERVATIONS = "observations"

    OBSERVATION = "observation"
    OBSERVATION_ATT_ID = "id"
    OBSERVATION_ISSUED = "issued"
    OBSERVATION_OBS_STATUS = "obs-status"
    OBSERVATION_COMPUTATION = "computation"
    OBSERVATION_COMPUTATION_TYPE_ATT = "type"
    OBSERVATION_REGION = "region"
    OBSERVATION_COUNTRY = "country"
    OBSERVATION_VALUE = "value"
    OBSERVATION_INDICATOR = "indicator"
    OBSERVATION_TIME = "time"
    OBSERVATION_ATT_GROUP = "group"

    OBSERVATION_ATT_COUNTRY_PREFIX = ""  # Empty value, but it remains here because it could still be changed
    OBSERVATION_ATT_INDICATOR_PREFIX = ""  # Empty value, but it remains here because it could still be changed
    OBSERVATION_ATT_TIME_PREFIX = ""  # Empty value, but it remains here because it could still be changed

    IMPORT_PROCESS = "import_process"
    IMPORT_PROCESS_ORGANIZATION_NAME = "organization_name"
    IMPORT_PROCESS_ORGANIZATION_ACRONYM = "organization_acronym"
    IMPORT_PROCESS_ORGANIZATION_URL = "organization_url"
    IMPORT_PROCESS_ORGANIZATION_DESC_EN = "organization_description_en"
    IMPORT_PROCESS_ORGANIZATION_DESC_ES = "organization_description_es"
    IMPORT_PROCESS_ORGANIZATION_DESC_FR = "organization_description_fr"
    IMPORT_PROCESS_ORGANIZATION_ID = "organization_id"
    # IMPORT_PROCESS_ORGANIZATION_URL_LOGO = "organization_logo"
    IMPORT_PROCESS_DATASOURCE = "datasource"
    IMPORT_PROCESS_DATASOURCE_ID_ATT = "id"
    IMPORT_PROCESS_TYPE = "type"
    IMPORT_PROCESS_USER = "user"
    IMPORT_PROCESS_SDMX_FREQUENCY = "sdmx_frequency"
    IMPORT_PROCESS_DATASOURCE_PREFIX = ""  # Empty value, but it remains here because it could still be changed
    IMPORT_PROCESS_TYPE_PREFIX = ""  # Empty value, but it remains here because it could still be changed
    IMPORT_PROCESS_USER_PREFIX = ""  # Empty value, but it remains here because it could still be changed
    IMPORT_PROCESS_FILE_NAME = "file_name"

    INDICATOR = "indicator"
    INDICATOR_ATT_ID = "id"
    INDICATOR_NAME_EN = "ind_name_en"
    INDICATOR_NAME_ES = "ind_name_es"
    INDICATOR_NAME_FR = "ind_name_fr"
    INDICATOR_DESCRIPTION_EN = "ind_description_en"
    INDICATOR_DESCRIPTION_ES = "ind_description_es"
    INDICATOR_DESCRIPTION_FR = "ind_description_fr"
    INDICATOR_MEASURE_UNIT = "measure_unit"
    INDICATOR_MEASURE_UNIT_CONVERT_TO_ATT = "convertible_to"
    INDICATOR_MEASURE_UNIT_FACTOR_ATT = "factor"
    INDICATOR_TOPIC = "topic-ref"
    INDICATOR_SPLITS_IN = "splitsIn"
    INDICATOR_PREFERABLE_TENDENCY = "preferable_tendency"

    INDICATOR_REF = "indicator-ref"

    INDICATOR_ATT_ID_PREFIX = ""  # Empty value, but it remains here because it could still be changed
    INDICATOR_ATT_MEASURE_UNIT_PREFIX = ""  # Empty value, but it remains here because it could still be changed

    LICENSE = "license"
    LICENSE_NAME = "lic_name"
    LICENSE_DESCRIPTION = "lic_description"
    LICENSE_REPUBLISH = "republish"
    LICENSE_URL = "lic_url"

    TIME = "time"
    TIME_INTERVAL = "interval"
    TIME_INTERVAL_BEG = "beginning"
    TIME_INTERVAL_END = "end"
    TIME_ATT_UNIT = "unit"

    INDICATOR_GROUPS = "indicator_groups"
    GROUP = "indicator_group"
    GROUP_ATT_ID = "id"
    GROUP_ATT_INDICATOR = "indicator"

    OBSERVATION_REF = "observation-ref"
    OBSERVATION_REF_ID = "id"


    def run(self):
        #Building xml
        #The order calling these methods should not be changed
        try:
            self.build_import_process_node()  # Done
            self.build_license_node()  # Done
            self.build_observations_node()  # Done
            self.build_indicators_node()  # Done
            self.build_indicator_groups_node()  # Done
            self.build_slices_node()  # Done
            self.include_indicator_relations()  # Done
        except BaseException as e:
            raise RuntimeError("Error while building xml file. " + e.message)
        paths = None

        #Persisting xml
        try:
            paths = self._persist_tree()
        except BaseException as e:
            raise RuntimeError("Error while persisting the builded xml. " + e.message)

        #Sending xml to the receiver
        try:
            #self._send_to_receiver(paths)
            pass
        except BaseException as e:
            raise RuntimeError("Error while sending xml to the receiver module. " + e.message)


    def _build_internal_config(self):
        result = ConfigParser()
        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'user.ini')
        result.read(config_path)
        return result


    def _adapt_user(self):
        """
        This method changes the login of the user, to use always the same, not mattering the
        object user received. It has been decided to make the importers work in that way.

        """
        self._user.user_id = self._config.get("USER", "login")
        pass

    def _build_root(self):
        result = Element(self.ROOT)
        result.attrib[self.ROOT_ID] = self._dataset.dataset_id
        return result

    def _send_to_receiver(self, paths):
        url = self._config.get("URL", "url")
        exceptions = []
        for file_path in paths:
            try:
                with codecs.open(file_path, encoding="utf-8") as xml:
                    file_content = xml.read()
                    file_identifier = self._obtain_content_of_original_path()
                    api_key = self._config.get("USER", "api_key")
                    '''req = requests.post(url=url,
                                        data={'xml': unicode(file_content).encode('utf-8'),
                                              'api_key': api_key},
                                        files={'file': file_identifier})
                    print req.status_code
                    print req.text'''

            except BaseException as e:
                e.message = 'File "{0}": {1}'.format(file_path, e.message)
                exceptions.append(e)
        self._process_sending_exceptions(exceptions)

    def _zip_file_name(self):
        """
        Return the path to where the zip file with the original contente must be.
        """
        if self._import_process in [self.API, self.SCRAP]:
            return str(self._path_to_original_file)
        if isinstance(self._path_to_original_file, str) or isinstance(self._path_to_original_file, unicode):
            return self._path_to_original_file + ".zip"
        elif isinstance(self._path_to_original_file, list):
            return self._path_to_original_file[0] + ".zip"
        else:
            raise RuntimeError("Unrecognized type object in param path_to_original_file: " + type(self._path_to_original_file))

    def _short_file_name(self, original_name):
        """
        Returns the name of the original file (remove the directory names in case we need it).
        """
        if isinstance(original_name, list):  # Recursive, but only one time.
            return self._short_file_name(self._zip_file_name)
        elif self._import_process in [self.API, self.SCRAP]:  # API, SCRAP
            return original_name

        else:  # Rest of import types

            if "/" in original_name:  # Linux
                arr = original_name.split("/")
                return arr[len(arr) - 1]
            elif "\\" in original_name:  # Windows
                arr = original_name.split("\\")
                return arr[len(arr) - 1]
            else:
                return original_name


    def _obtain_content_of_original_path(self):
        """
        It returns the content that should be in the variable "file" when sending a request to the receiver.
        If import procces in [SCRAP, API], then the content is a url.
        Elsewhere, the content is a zipped file.
        """

        if self._import_process in [self.API, self.SCRAP]:
            return self._api_or_scrap_original_content()
        else:
            return self._persisted_file_original_content()

    def _api_or_scrap_original_content(self):
        return self._path_to_original_file

    def _persisted_file_original_content(self):
        file_zip = zipfile.ZipFile(self._zip_file_name, "w")
        if isinstance(self._path_to_original_file, list):
            for path in self._path_to_original_file:
                self._write_file_to_zip_object(file_zip, path)
        elif isinstance(self._path_to_original_file, str) or isinstance(self._path_to_original_file, unicode):
            self._write_file_to_zip_object(file_zip, self._path_to_original_file)
        else:
            raise RuntimeError("Unrecognized type object in param path_to_original_file: " + type(self._path_to_original_file))
        file_zip.close()
        # with open(self._zip_file_name(), "rb") as file_content:
        #     return file_content.read()
        return open(self._zip_file_name, "rb")

    def _write_file_to_zip_object(self, zip_object, path):
        zip_object.write(path, self._short_file_name(path))

    @staticmethod
    def _process_sending_exceptions(exceptions):
        if len(exceptions) == 0:
            return
        message = ""
        for e in exceptions:
            message += e.message + "\n"
        raise RuntimeError("Error processing files:\n")


    def include_indicator_relations(self):
        if self._indicator_relations is None or len(self._indicator_relations) == 0:
            return  # Nothing to fo (most of cases)
        else:
            for a_relation in self._indicator_relations:
                self.include_relation_in_the_tree(a_relation)

    def include_relation_in_the_tree(self, a_relation):
        #Looking for source node in the tree
        source_node = self._get_indicator_node_by_id(a_relation.source.indicator_id)
        relations_node = source_node.find(self.INDICATOR_SPLITS_IN)

        #Creating base relation node if needed, and incorporating it to the tree
        if relations_node is None:
            relations_node = Element(self.INDICATOR_SPLITS_IN)
            source_node.append(relations_node)

        #Creating and adding new relation
        new_node = Element(self.INDICATOR_REF)
        new_node.text = a_relation.target.indicator_id
        relations_node.append(new_node)


    def _get_indicator_node_by_id(self, indicator_id):
        indicator_nodes = self._root.find(self.INDICATORS).getchildren()
        for ind in indicator_nodes:
            if ind.attrib[self.INDICATOR_ATT_ID] == indicator_id:
                return ind
        raise RuntimeError("Impossible to find indicator with id {0}. Unable to relate indicators with it"
                           .format(indicator_id))

    def build_indicator_groups_node(self):
        groups = Element(self.INDICATOR_GROUPS)
        for group_node in self._group_dic:
            # The nodes are already built. We are storing nodes in the dict
            groups.append(group_node)
        self._root.append(groups)

    def build_slices_node(self):
        #Building node
        slices_node = Element(self.SLICES)
        #Building child nodes
        for data_slice in self._dataset.slices:
            slices_node.append(self.build_slice_node(data_slice))
        #Appending node to root
        self._root.append(slices_node)


    def build_slice_node(self, data_slice):
        #Building node
        slice_node = Element(self.SLICE)
        #Attaching info
        #id
        slice_node.attrib[self.SLICE_ATT_ID] = data_slice.slice_id
        #metadata
        slice_node.append(self.build_metadata_slice_node(data_slice))
        #referred obs
        slice_node.append(self.build_referred_slice_node(data_slice))
        #returnin node
        return slice_node


    def build_metadata_slice_node(self, data_slice):
        #Building metadata
        metadata_node = Element(self.SLICE_METADATA)
        #Adding info
        #indicator-ref
        indicator_ref_node = Element(self.INDICATOR_REF)
        indicator_ref_node.attrib[self.INDICATOR_ATT_ID] = data_slice.indicator.indicator_id
        metadata_node.append(indicator_ref_node)

        #time/region
        if isinstance(data_slice.dimension, Time):
            metadata_node.append(self.build_time_node(data_slice.dimension))
        elif isinstance(data_slice.dimension, Region):
            if type(data_slice.dimension) == Region:
                region_node = Element(self.OBSERVATION_REGION)
                region_node.text = self.OBSERVATION_ATT_COUNTRY_PREFIX \
                                   + data_slice.dimension.un_code
                metadata_node.append(region_node)
            elif type(data_slice.dimension) == Country:
                country_node = Element(self.OBSERVATION_COUNTRY)
                country_node.text = str(data_slice.dimension.iso3)  # It will have it
                metadata_node.append(country_node)
            else:
                raise RuntimeError("Unrecognized area type {0} while building slice. Impossible to generate xml".
                                   format(type(data_slice.dimension)))

        else:
            raise RuntimeError("Unknown dimension while building slice.")

        #Returnin node
        return metadata_node

    def build_referred_slice_node(self, data_slice):
        #Building node
        referred_node = Element(self.SLICE_REFERRED)

        #Adding info
        for data_obs in data_slice.observations:
            obs_node = Element(self.OBSERVATION_REF)
            obs_node.attrib[self.OBSERVATION_ATT_ID] = data_obs.get_observation_id()
            referred_node.append(obs_node)
        #returnig node
        return referred_node


    def build_observations_node(self):
        observations_node = Element(self.OBSERVATIONS)
        for data_obs in self._dataset.observations:
            observations_node.append(self.build_observation_node(data_obs))
        self._root.append(observations_node)


    def build_indicators_node(self):
        result = Element(self.INDICATORS)
        self._add_possible_dataset_specified_indicators_to_dict()
        for data_indicator in self._indicator_dic:
            result.append(self.build_indicator_node(self._indicator_dic[data_indicator]))

        self._root.append(result)

    def _add_possible_dataset_specified_indicators_to_dict(self):
        """
        Some importers have been built linking indicator objects with datasets, and some does not link them.
        It does not cause this module to crash: indicators are incorporated on the fly while parsing observations.
        But, if the links exist, this module ensures at this point that they are stored in the internal ind_dict,
        preventing situations such as:
         - We want to introduce an indicator, but no observation points to it.
         - We need an indicator for an 'plitsIn' node, but no observation points to it.

        """
        if self._dataset.indicators is None:
            return
        for an_ind in self._dataset.indicators:
            self.include_indicator_if_needed(an_ind)
        pass

    def build_indicator_node(self, data_indicator):
        #Building node
        result = Element(self.INDICATOR)

        #Attaching info
        #id
        result.attrib[self.INDICATOR_ATT_ID] = \
            self.INDICATOR_ATT_ID_PREFIX \
            + data_indicator.indicator_id
        #names
        names = self._extract_indicator_name_nodes(data_indicator)
        for a_name in names:
            result.append(a_name)

        #descriptions
        descriptions = self._extract_indicator_description_nodes(data_indicator)
        for a_desc in descriptions:
            result.append(a_desc)

        #topic
        node_topic = Element(self.INDICATOR_TOPIC)
        node_topic.text = data_indicator.topic
        result.append(node_topic)

        #preferable_tendency
        node_tendency = Element(self.INDICATOR_PREFERABLE_TENDENCY)
        node_tendency.text = data_indicator.preferable_tendency
        result.append(node_tendency)

        #MeasureUnit
        node_measure = Element(self.INDICATOR_MEASURE_UNIT)
        node_measure.text = self.INDICATOR_ATT_MEASURE_UNIT_PREFIX \
                            + data_indicator.measurement_unit.name
        node_measure.attrib[self.INDICATOR_MEASURE_UNIT_CONVERT_TO_ATT] = data_indicator.measurement_unit.convert_to
        node_measure.attrib[self.INDICATOR_MEASURE_UNIT_FACTOR_ATT] = str(data_indicator.measurement_unit.factor)
        result.append(node_measure)

        #Returning complete node
        return result

    def _extract_indicator_description_nodes(self, data_indicator):
        result = []

        #EN
        node_desc_en = Element(self.INDICATOR_DESCRIPTION_EN)
        node_desc_en.text = data_indicator.description_en
        result.append(node_desc_en)
        #ES
        node_desc_es = Element(self.INDICATOR_DESCRIPTION_ES)
        node_desc_es.text = data_indicator.description_es
        result.append(node_desc_es)
        #FR
        node_desc_fr = Element(self.INDICATOR_DESCRIPTION_FR)
        node_desc_fr.text = data_indicator.description_fr
        result.append(node_desc_fr)

        return result

    def _extract_indicator_name_nodes(self, data_indicator):
        result = []
        #EN
        node_name_en = Element(self.INDICATOR_NAME_EN)
        node_name_en.text = data_indicator.name_en
        result.append(node_name_en)
        #ES
        node_name_es = Element(self.INDICATOR_NAME_ES)
        node_name_es.text = data_indicator.name_es
        result.append(node_name_es)
        #FR
        node_name_fr = Element(self.INDICATOR_NAME_FR)
        node_name_fr.text = data_indicator.name_fr
        result.append(node_name_fr)

        return result

    def build_license_node(self):
        #Building node
        license_node = Element(self.LICENSE)

        #Attaching info
        #name
        name_node = Element(self.LICENSE_NAME)
        name_node.text = self._dataset.license_type.name
        license_node.append(name_node)

        #description
        desc_node = Element(self.LICENSE_DESCRIPTION)
        desc_node.text = self._dataset.license_type.description
        license_node.append(desc_node)

        #republish
        republish_node = Element(self.LICENSE_REPUBLISH)
        republish_node.text = str(self._dataset.license_type.republish).lower()
        license_node.append(republish_node)

        #url
        url_node = Element(self.LICENSE_URL)
        url_node.text = self._dataset.license_type.url
        license_node.append(url_node)


        #Attaching node to root
        self._root.append(license_node)


    def _persist_tree(self):
	print "self._dataset.dataset_id=%s" %self._dataset.dataset_id
        return XmlSplitter(self._root, self._dataset.dataset_id).run()


    def build_observation_node(self, data_obs):
        #Building node
        observation_node = Element(self.OBSERVATION)

        #Attaching info
        #id (attrib.)
        observation_node.attrib[self.OBSERVATION_ATT_ID] = \
            str(data_obs.get_observation_id())
        #issued
        issued_node = Element(self.OBSERVATION_ISSUED)
        issued_node.text = data_obs.issued.get_time_string()
        observation_node.append(issued_node)
        #obs-staus, value
        self.attach_value_to_observation(observation_node, data_obs)

        #computation
        computation_node = Element(self.OBSERVATION_COMPUTATION)
        computation_node.attrib[self.OBSERVATION_COMPUTATION_TYPE_ATT] = data_obs.computation.uri
        computation_node.text = Computation.get_desc_of_uri(data_obs.computation.uri)
        observation_node.append(computation_node)

        if type(data_obs.region) == Region:
            region_node = Element(self.OBSERVATION_REGION)
            region_node.text = self.OBSERVATION_ATT_COUNTRY_PREFIX + str(data_obs.region.un_code)

            observation_node.append(region_node)
        elif type(data_obs.region) == Country:
            country_node = Element(self.OBSERVATION_COUNTRY)
            country_node.text = str(data_obs.region.iso3)  # It will have it, do not worry.
            observation_node.append(country_node)
        else:
            raise RuntimeError("Unrecognized area type {0} while building observation. Unable to build xml".
                               format(type(data_obs.region)))

        #time
        observation_node.append(self.build_time_node(data_obs.ref_time))

        #indicator
        indicator_ref_node = Element(self.INDICATOR_REF)
        indicator_ref_node.attrib[self.OBSERVATION_INDICATOR] = \
            self.OBSERVATION_ATT_INDICATOR_PREFIX \
            + str(data_obs.indicator.indicator_id)
        self.include_indicator_if_needed(data_obs.indicator)  # Managing ind. info
        observation_node.append(indicator_ref_node)

        #Attaching optional group info
        self.attach_groups_info_if_needed(observation_node, data_obs)

        return observation_node


    def build_time_node(self, ref_time):
        #Building top node
        time_node = Element(self.TIME)

        #Managging different time instances
        if type(ref_time) is Instant:
            time_node.attrib[self.TIME_ATT_UNIT] = "instant"
            time_node.text = ref_time.get_time_string()
        elif type(ref_time) is YearInterval:
            time_node.attrib[self.TIME_ATT_UNIT] = "years"
            time_node.text = ref_time.get_time_string()
        elif type(ref_time) is MonthInterval:
            time_node.attrib[self.TIME_ATT_UNIT] = "months"
            time_node.text = ref_time.get_time_string()
        elif type(ref_time) is Interval:
            if ref_time.frequency == Interval.YEARLY:
                time_node.attrib[self.TIME_ATT_UNIT] = "years"
            else:
                time_node.attrib[self.TIME_ATT_UNIT] = "months"
            interval_node = Element(self.TIME_INTERVAL)
            beg_node = Element(self.TIME_INTERVAL_BEG)
            beg_node.text = str(ref_time.start_time)
            end_node = Element(self.TIME_INTERVAL_END)
            end_node.text = str(ref_time.end_time)
            interval_node.append(beg_node)
            interval_node.append(end_node)
            time_node.append(interval_node)

        else:
            raise RuntimeError("Unrecognized time type. Impossible to build node")
        #Returning final node
        return time_node


    def attach_groups_info_if_needed(self, node_obs, data_obs):
        if data_obs.indicator_group is None:
            return  # No actions needed in this case
        node_obs.attrib[self.OBSERVATION_ATT_GROUP] = data_obs.indicator_group.group_id
        self.treat_new_group_info(data_obs.indicator_group)

    def treat_new_group_info(self, data_obs):
        data_group = data_obs.indicator_group
        #Treating indicator info
        self.include_indicator_if_needed(data_group)  # Group info is a specialization of indicator

        #Treating group_node info
        group_node = None
        #Looking for node/adding node to internal dict if needed
        if data_group.group_id in self._group_dic:
            group_node = self._group_dic[data_group.group_id]
        else:
            group_node = Element(self.GROUP)
            group_node.attrib[self.GROUP_ATT_ID] = str(data_group.group_id)
            group_node.attrib[self.GROUP_ATT_INDICATOR] = self.INDICATOR_ATT_ID_PREFIX + data_group.indicator_id
            self._group_dic[data_group.group_id] = group_node

            # We don't need to add observations to this node according to the current spec. but it could change.
            # So code for that remains in this comment
            #
            # #Adding obs to node
            # obs_node_ref = Element(self.OBSERVATION_REF)
            # obs_node_ref.attrib[self.OBSERVATION_REF_ID] = data_obs.get_observation_id()
            # group_node.append(obs_node_ref)

    def include_indicator_if_needed(self, data_indicator):
        if data_indicator.indicator_id in self._indicator_dic:
            return
        self._indicator_dic[data_indicator.indicator_id] = data_indicator

    def attach_value_to_observation(self, obs_node, data_obs):
        #Adding obligatory node obs-status
        status_node = Element(self.OBSERVATION_OBS_STATUS)
        status = data_obs.value.obs_status
        status_node.text = status
        obs_node.append(status_node)

        #Adding value if needed
        if not status == data_obs.value.MISSING:
            value_node = Element(self.OBSERVATION_VALUE)
            value_node.text = str(data_obs.value.value)
            obs_node.append(value_node)

            #No returning sentence. We are modifying the received obs_node object

    def build_import_process_node(self):
        #Building node
        metadata = Element(self.IMPORT_PROCESS)

        #Attaching nodes
        #Organization_name
        organization_name_node = Element(self.IMPORT_PROCESS_ORGANIZATION_NAME)
        organization_name_node.text = self._datasource.organization.name
        metadata.append(organization_name_node)
        #organization_id
        organization_acronym_node = Element(self.IMPORT_PROCESS_ORGANIZATION_ACRONYM)
        organization_acronym_node.text = self._datasource.organization.acronym
        metadata.append(organization_acronym_node)
        #Organization_url
        organization_url_node = Element(self.IMPORT_PROCESS_ORGANIZATION_URL)
        organization_url_node.text = self._datasource.organization.url
        metadata.append(organization_url_node)
        #organization_id
        organization_id_node = Element(self.IMPORT_PROCESS_ORGANIZATION_ID)
        organization_id_node.text = self._datasource.organization.organization_id
        metadata.append(organization_id_node)

        #Organization_desc_en
        organization_desc_en_node = Element(self.IMPORT_PROCESS_ORGANIZATION_DESC_EN)
        organization_desc_en_node.text = self._datasource.organization.description_en
        metadata.append(organization_desc_en_node)

        #Organization_desc_es
        organization_desc_es_node = Element(self.IMPORT_PROCESS_ORGANIZATION_DESC_ES)
        organization_desc_es_node.text = self._datasource.organization.description_es
        metadata.append(organization_desc_es_node)

        #Organization_desc_fr
        organization_desc_fr_node = Element(self.IMPORT_PROCESS_ORGANIZATION_DESC_FR)
        organization_desc_fr_node.text = self._datasource.organization.description_fr
        metadata.append(organization_desc_fr_node)

        # #Organization_url
        # organization_logo_node = Element(self.IMPORT_PROCESS_ORGANIZATION_URL_LOGO)
        # organization_logo_node.text = self._datasource.organization.url_logo
        # metadata.append(organization_logo_node)

        #datasource
        datasource_node = Element(self.IMPORT_PROCESS_DATASOURCE)
        datasource_node.attrib[self.IMPORT_PROCESS_DATASOURCE_ID_ATT] = self._datasource.source_id
        datasource_node.text = self.IMPORT_PROCESS_DATASOURCE_PREFIX + self._datasource.name
        metadata.append(datasource_node)

        #type
        if self._import_process not in [self.API, self.SCRAP, self.XML, self.CSV, self.JSON, self.XLS]:
            raise RuntimeError("Unrecognized import process: " + self._import_process)
        type_node = Element(self.IMPORT_PROCESS_TYPE)
        type_node.text = self.IMPORT_PROCESS_TYPE_PREFIX + self._import_process
        metadata.append(type_node)

        #file_name
        file_name_node = Element(self.IMPORT_PROCESS_FILE_NAME)
        file_name_node.text = self._short_file_name(self._zip_file_name)
        metadata.append(file_name_node)

        #user
        user_node = Element(self.IMPORT_PROCESS_USER)
        user_node.text = self.IMPORT_PROCESS_USER_PREFIX + self._user.user_id
        metadata.append(user_node)
        #sdmx_frequency
        sdmx_freq_node = Element(self.IMPORT_PROCESS_SDMX_FREQUENCY)
        sdmx_freq_node.text = self._dataset.frequency
        metadata.append(sdmx_freq_node)


        #Addind node to root
        self._root.append(metadata)


    @staticmethod
    def _read_external_field(original):
        try:
            return unicode(original, errors="ignore")
        except:
            return original


############################################################################
#                               XmlSplitter                                #
############################################################################




class XmlSplitter(object):
    """
    It receives an xml tree object and return a list of files with the tree serialized.
    It will split its content into files if it is too big, following this formula:

     - Each file will contain a top of 10.000 observations
     - If we have slices, they will be in tis own file.
     - Information of indicators, organization, license, etc, will be repeated in all the files,
        according to the xsd definition

    """

    _MAX_OBSERVATIONS_ALLOWED = 100000000000

    def __init__(self, tree, dataset_id):
        self._tree = tree
        self._int_for_file = 0
        self._dataset_id = dataset_id
        self._path_counter = 0


    def run(self):
        """
        It return a list of files that contains all the info of the xml in a format that can be sended
        to the receiver

        """
        if self._too_much_observations_for_a_file():
            return self._return_tree_splitted_in_files()
        else:
            return self._return_tree_in_a_single_file()

    def _return_tree_splitted_in_files(self):
        """
        Steps:
         - Look for observations node
         - Remove it from the tree, but store it
         - remove the slices node and substitute it for an empty one
         - getchildren of observations_node and, for i in len(getchildren)
            -pop an element (an observation) from the list
            - put this element in a new observation node
            - when reaching max_allowed_observations, put this observation node
            in the global tree.
            - Serialize it
            - Save the path of serialization and add it to the result
         - Do something similar with the slices_node (with an empty observations_node)
            In this case, no need to control number of slices. Just a file containing only slices


        """
        result = []
        #Getting original obs and slices
        original_obs_node = self._get_observations_node_of_a_tree(self._tree)
        every_obs = original_obs_node.getchildren()
        original_sli_node = self._get_slices_node_of_a_tree(self._tree)

        #Removing obs and slices from the original tree
        self._remove_slices_and_obs_from_the_original_tree()

        #putting groups of obs in the tree and serializing
        original_length = len(every_obs)
        temporal_observations_node = Element(ModelToXMLTransformer.OBSERVATIONS)
        for i in range(1, original_length + 1):
            if i % self._MAX_OBSERVATIONS_ALLOWED == 0:  # cycle of _MAX_OBSERVATIONS_ALLOWED: serialize and new node
                result.append(self._persist_tree_with_obs_node(temporal_observations_node))
                temporal_observations_node = Element(ModelToXMLTransformer.OBSERVATIONS)
            temporal_observations_node.append(every_obs.pop())
        if len(temporal_observations_node.getchildren()):  # Out of the for loop, but we may have obs to include yet
            result.append(self._persist_tree_with_obs_node(temporal_observations_node))

        #managing slices:
        if len(original_sli_node.getchildren()) == 0:
            return result  # No more to do. The original tree hadn't got slices.
        else:
            result.append(self._persist_tree_with_sli_node(original_sli_node))

        #No more to do but returning result. We could restore the original tree object, but there is no reason to do it.

        return result

    def _remove_slices_and_obs_from_the_original_tree(self):
        empty_obs_node = Element(ModelToXMLTransformer.OBSERVATIONS)
        self._replace_node(parent=self._tree,
                           old_node=self._get_observations_node_of_a_tree(self._tree),
                           new_node=empty_obs_node)
        empty_sli_node = Element(ModelToXMLTransformer.SLICES)
        self._replace_node(parent=self._tree,
                           old_node=self._get_slices_node_of_a_tree(self._tree),
                           new_node=empty_sli_node)


    def _persist_tree_with_obs_node(self, temporal_observations_node):
        """
        It return the path to the file where the xml has been persisted
        """
        original_observations_node = self._get_observations_node_of_a_tree(self._tree)
        self._replace_node(parent=self._tree,
                           old_node=original_observations_node,
                           new_node=temporal_observations_node)
        result = self._presist_current_tree()
        #Restoring state of the tree
        self._replace_node(parent=self._tree,
                           old_node=temporal_observations_node,
                           new_node=original_observations_node)
        return result

    def _persist_tree_with_sli_node(self, temporal_sli_node):
        """
        It returns the path to the file where the xml has been persisted.

        """
        original_sli_node = self._get_slices_node_of_a_tree(self._tree)
        self._replace_node(parent=self._tree,
                           old_node=original_sli_node,
                           new_node=temporal_sli_node)
        result = self._presist_current_tree()
        #Restoring state of the tree
        self._replace_node(parent=self._tree,
                           old_node=temporal_sli_node,
                           new_node=original_sli_node)
        return result

    def _presist_current_tree(self):
        """
        It returns the path of the xml file where the tree has been persisted

        """
        path = self._get_a_new_file_path()
        ElementTree(self._tree).write(path, encoding="utf-8")
        return path


    @staticmethod
    def _replace_node(parent, old_node, new_node):
        parent.remove(old_node)
        parent.append(new_node)

    def _too_much_observations_for_a_file(self):
        """
        It returns a bool indicating if the tree should be splitted because it has too much observations.

        """
        observations_node = self._get_observations_node_of_a_tree(self._tree)
        if len(observations_node.getchildren()) > self._MAX_OBSERVATIONS_ALLOWED:
            return True
        return False

    @staticmethod
    def _get_observations_node_of_a_tree(tree):
        """
        It returns the observations node of the received tree. It should build an special string for
        executing the search

        """
        param_for_the_search = ".//" + ModelToXMLTransformer.OBSERVATIONS
        return tree.find(param_for_the_search)

    @staticmethod
    def _get_slices_node_of_a_tree(tree):
        """
        It returns the slices node of the received tree. It should build an special string for executing
        teh search.

        """
        param_for_the_search = ".//" + ModelToXMLTransformer.SLICES
        return tree.find(param_for_the_search)


    def _return_tree_in_a_single_file(self):
        """
        Even returning a single file, we must place it in a list. model2xml expects a list

        """
        result = []
        file_path = self._get_a_new_file_path()
        self.write_tree_in_path(self._tree, file_path)
        result.append(file_path)
        return result


    def _get_a_new_file_path(self):
        self._int_for_file += 1
        return self._dataset_id + "_" + str(self._int_for_file) + "_" + str(self._path_counter) + ".xml"


    @staticmethod
    def write_tree_in_path(tree, file_path):
        ElementTree(tree).write(file_path, encoding="utf-8")

__author__ = 'Dani'

from ..entities.deal import Deal
import re

class DealsBuilder(object):

    def __init__(self):
        pass

    @staticmethod
    def turn_node_into_deal_object(info_node):
        """
        It receives a node (Element of ElementTree) and returns a deal object containing the needed data

        """
        a_deal = Deal()
        a_deal.target_country = _extract_target_country(info_node)
        a_deal.date = _extract_date(info_node)
        a_deal.production_hectares = _extract_production_hectares(info_node)
        a_deal.intended_hectares = _extract_intended_hectares(info_node)
        a_deal.contract_hectares = _extract_contract_hectares(info_node)
        a_deal.sectors = _extract_sectors(info_node)
        a_deal.negotiation_status = _extract_negotiation_status(info_node)
        return a_deal


#############################################################################################
#                                       FUNCTIONS                                           #
#############################################################################################

###  Contants


PROPERTY = "name"
TARGET_COUNTRY = "target_country"
SECTORS = "intention"
NEGOTIATION_STATUS = "negotiation_status"
NO_VALUE = "None"
INTENDED_SIZE = "intended_size"
CONTRACT_SIZE = "contract_size"
PRODUCTION_SIZE = "production_size"


#Functions

def _extract_hectares(info_node, hectares_type):
    hectares_container = _get_node_data(info_node, hectares_type)
    if hectares_container == NO_VALUE:
        return None
    elif hectares_container.isdigit():
        return int(hectares_container)
    else:
        return None


def _extract_intended_hectares(info_node):
    return _extract_hectares(info_node, INTENDED_SIZE)


def _extract_contract_hectares(info_node):
    return _extract_hectares(info_node, CONTRACT_SIZE)


def _extract_production_hectares(info_node):
    return _extract_hectares(info_node, PRODUCTION_SIZE)


def _extract_negotiation_status(info_node):
    #Looking for the target text
    status_container = _get_node_data(info_node, NEGOTIATION_STATUS)
    if status_container == NO_VALUE:
        return None
    elif status_container.__contains__(Deal.FAILED):
        return Deal.FAILED
    elif status_container.__contains__(Deal.CONCLUDED):
        return Deal.CONCLUDED
    elif status_container.__contains__(Deal.INTENDED):
        return Deal.INTENDED
    else:
        raise RuntimeError("Unrecognized negotiation status in node: " + status_container)


def _extract_target_country(info_node):
    for subnode in info_node.getchildren():
        if subnode.attrib[PROPERTY] == TARGET_COUNTRY:
            return subnode.text.strip()
    _raise_error("country", "not found")


def _extract_date(info_node):
    # 2016/03/29: Pattern of negotiation_status node "[YYYY] STATUS (XXXX XXXXXX)" or "STATUS (XXXX XXXXXX)"

    #Looking for the target text
    date_container = _get_node_data(info_node, NEGOTIATION_STATUS)
    # return None if there is no negotiation_status value
    if date_container == NO_VALUE:
        return None

    # return None if there is no year in negotiation_status node. STATUS (XXXX XXXXXXXX)
    if '[' not in date_container:
        return None

    candidate_years = re.findall(r'\[([^]]*)\]', date_container) # get the years (as string)
    candidate_years = map(int, candidate_years) # convert to integer
    negotiation_status_year = max(candidate_years) # obtain the highest value

    return negotiation_status_year


def _lower_lenght(elem1, elem2):
    if len(elem1) <= len(elem2):
        return len(elem1)
    return len(elem2)


def _find_index_all_occurrences_of_a_sequence(string, sequence):
    result = []
    last_found_pos = 0
    while last_found_pos != -1:
        last_found_pos = string.find(sequence, last_found_pos+1)
        if last_found_pos != -1:
            result.append(last_found_pos)
    return result


def _get_node_data(info_node, tag):
    for subnode in info_node.getchildren():
        if subnode.attrib[PROPERTY] == tag:
            return _remove_blanks(subnode.text)
    return NO_VALUE

def _remove_blanks(text):
    if text is None:
	return NO_VALUE

    result = text.replace("\t", "")
    result = result.replace("\n", "")
    result = result.replace("\r", "")
    return result


def _extract_sectors(info_node):
    #Looking for text
    text = _get_node_data(info_node, SECTORS)
    if text is None:
        _raise_error("sectors", "not found")
        return  # It will throw an error, the next won't execute.... but let's ensure that
    elif text == NO_VALUE:
        return ['Unknown']  # Unknowk sector
    result = []
    candidate_sectors = text.split(",")
    for candidate in candidate_sectors:
        if not (candidate is None or candidate == ""):
            result.append(candidate.replace(" ", "")) # Should we replace blank space ?
    if len(result) == 0:
        _raise_error("sectors", "not found")

    return result


def _raise_error(concrete_filed, cause):
    raise RuntimeError("Error while parsing {0} in a node. Cause: {1}. Node will be ignored".format(concrete_filed,
                                                                                                    cause))

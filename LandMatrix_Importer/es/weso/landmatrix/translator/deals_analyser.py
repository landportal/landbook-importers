from reconciler.country_reconciler import CountryReconciler
from reconciler.exceptions.unknown_country_error import UnknownCountryError


from .keys_dicts import KeyDicts
from ..entities.deal_analyser_entry import DealAnalyserEntry
from ..entities.deal import Deal

__author__ = 'Dani'


class DealsAnalyser(object):
    """
    It is built with a list of deal objects. When calling run, it return a dict that contains
    objetcs of type DealAnalyserEntry, containing a country, a date, an indicator and the composed
    value for the first two. Date will indicate the higher of the found dates

    """


    def __init__(self, deals_list, indicators_dict):
        self._list_deals = deals_list
        self._reconciler = CountryReconciler()
        self._deals_dict = {}
        self._indicators_dict = indicators_dict
        self.latest_date = 0  # It will store the latest date found for all the deals (no matter about the country)


    def run(self):
        for a_deal in self._list_deals:
            target_country = self._process_target_country(a_deal.target_country)
            if not target_country is None:
                self._process_the_fact_that_the_deal_has_valid_country(target_country)
                self._process_deals_by_negotiation_status(a_deal, target_country)
                self._process_deals_by_implementation_status(a_deal, target_country)
                self._process_deals_by_topic(a_deal, target_country)
                self._process_deals_by_hectares(a_deal, target_country)
                self._update_latest_date(a_deal)
            else:
                raise RuntimeError("We have found a deal with a non recognized country."
                                   " Agregate values cuold be incorrect form this point, execution should stop. "
                                   "Country: " + a_deal.target_country)
	self._set_last_date_for_all_indicators()

        return self._deals_dict

    def _process_target_country(self, target_country):
        try:
            return self._reconciler.get_country_by_en_name(target_country.encode(encoding="utf-8"))
        except UnknownCountryError:
            return None


    def _process_the_fact_that_the_deal_has_valid_country(self, target_country):
        self._increase_counter_indicator(KeyDicts.TOTAL_DEALS, target_country)


    def _process_deals_by_negotiation_status(self, deal, target_country):
        if deal.negotiation_status == Deal.CONCLUDED:
            self._increase_counter_indicator(KeyDicts.CONCLUDED_DEALS, target_country)
        elif deal.negotiation_status == Deal.FAILED:
            self._increase_counter_indicator(KeyDicts.FAILED_DEALS, target_country)
        elif deal.negotiation_status == Deal.INTENDED:
            self._increase_counter_indicator(KeyDicts.INTENDED_DEALS, target_country)

    def _process_deals_by_implementation_status(self, deal, target_country):
        if (_is_in_production(deal)):
            self._increase_counter_indicator(KeyDicts.IN_PRODUCTION_DEALS, target_country)

    def _update_latest_date(self, deal):
        if deal.date is not None and deal.date > self.latest_date:
            self.latest_date = deal.date

    """ This method set the last_date of all the deal_entries using the latest date found in all the deals.
    """
    def _set_last_date_for_all_indicators(self):
	for deal_entry in self._deals_dict.itervalues():
	    deal_entry.last_date = self.latest_date

    def _process_deals_by_topic(self, deal, target_country):
	hectares_to_add = self._get_hectares_to_add(deal)

	# AGRICULTURE
        if Deal.BIOFUELS in deal.sectors:
            self._increase_counter_indicator(KeyDicts.BIOFUELS_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_BIOFUELS_DEALS, hectares_to_add, target_country)
            self._increase_counter_indicator(KeyDicts.AGRICULTURE_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_AGRICULTURE_DEALS, hectares_to_add, target_country)

        if Deal.FOOD_CROPS in deal.sectors:
            self._increase_counter_indicator(KeyDicts.FOOD_CROPS_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_FOOD_CROPS_DEALS, hectares_to_add, target_country)
            self._increase_counter_indicator(KeyDicts.AGRICULTURE_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_AGRICULTURE_DEALS, hectares_to_add, target_country)

        if Deal.LIVESTOCK in deal.sectors:
            self._increase_counter_indicator(KeyDicts.LIVESTOCK_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_LIVESTOCK_DEALS, hectares_to_add, target_country)
            self._increase_counter_indicator(KeyDicts.AGRICULTURE_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_AGRICULTURE_DEALS, hectares_to_add, target_country)

        if Deal.NON_FOOD_AGRICULTURAL_COMMODITIES in deal.sectors:
            self._increase_counter_indicator(KeyDicts.NON_FOOD_AGRICULTURAL_COMMODITIES_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_NON_FOOD_AGRICULTURAL_COMMODITIES_DEALS, hectares_to_add, target_country)
            self._increase_counter_indicator(KeyDicts.AGRICULTURE_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_AGRICULTURE_DEALS, hectares_to_add, target_country)

        if Deal.AGRIUNSPECIFIED in deal.sectors:
            self._increase_counter_indicator(KeyDicts.AGRIUNSPECIFIED_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_AGRIUNSPECIFIED_DEALS, hectares_to_add, target_country)
            self._increase_counter_indicator(KeyDicts.AGRICULTURE_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_AGRICULTURE_DEALS, hectares_to_add, target_country)


        if Deal.CONSERVATION in deal.sectors:
            self._increase_counter_indicator(KeyDicts.CONSERVATION_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_CONSERVATION_DEALS, hectares_to_add, target_country)


	# FORESTRY
        if Deal.FOR_WOOD_AND_FIBRE in deal.sectors:
            self._increase_counter_indicator(KeyDicts.FOR_WOOD_AND_FIBRE_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_FOR_WOOD_AND_FIBRE_DEALS, hectares_to_add, target_country)
            self._increase_counter_indicator(KeyDicts.FORESTRY_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_FORESTRY_DEALS, hectares_to_add, target_country)

        if Deal.FOR_CARBON_SEQUESTRATION_REDD in deal.sectors:
            self._increase_counter_indicator(KeyDicts.FOR_CARBON_SEQUESTRATION_REDD_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_FOR_CARBON_SEQUESTRATION_REDD_DEALS, hectares_to_add, target_country)
            self._increase_counter_indicator(KeyDicts.FORESTRY_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_FORESTRY_DEALS, hectares_to_add, target_country)

        if Deal.FORESTUNSPECIFIED in deal.sectors:
            self._increase_counter_indicator(KeyDicts.FORESTUNSPECIFIED_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_FORESTUNSPECIFIED_DEALS, hectares_to_add, target_country)
            self._increase_counter_indicator(KeyDicts.FORESTRY_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_FORESTRY_DEALS, hectares_to_add, target_country)


        if Deal.INDUSTRY in deal.sectors:
            self._increase_counter_indicator(KeyDicts.INDUSTRY_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_INDUSTRY_DEALS, hectares_to_add, target_country)


        if Deal.RENEWABLE_ENERGY in deal.sectors:
            self._increase_counter_indicator(KeyDicts.RENEWABLE_ENERGY_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_RENEWABLE_ENERGY_DEALS, hectares_to_add, target_country)


        if Deal.TOURISM in deal.sectors:
            self._increase_counter_indicator(KeyDicts.TOURISM_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_TOURISM_DEALS, hectares_to_add, target_country)


        if Deal.OTHER in deal.sectors:
            self._increase_counter_indicator(KeyDicts.OTHER_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_OTHER_DEALS, hectares_to_add, target_country)


        if Deal.UNKNOWN in deal.sectors:
            self._increase_counter_indicator(KeyDicts.UNKNOWN_DEALS, target_country)
            self._increase_hectares_indicator(KeyDicts.HECTARES_UNKNOWN_DEALS, hectares_to_add, target_country)


    def _process_deals_by_hectares(self, deal, target_country):
        """ The algorithm to obtain the value to add to the total hectares is:
             1) Try to obtain the contract hectares
             2) If not, try to obtain the intended hectares
             3) If not, try to obtain the production hectares
             4) If not, add 0 (zero)
            To run the algorithm, the initial value is set to 0 and the process write over the best value in reverse order.
        """

        if (deal.production_hectares is not None) and (_is_in_production(deal)):
            self._increase_hectares_indicator(KeyDicts.HECTARES_PRODUCTION_DEALS,
                                              deal.production_hectares,
                                              target_country)

        if deal.intended_hectares is not None:
            self._increase_hectares_indicator(KeyDicts.HECTARES_INTENDED_DEALS,
                                              deal.intended_hectares,
                                              target_country)

        if deal.contract_hectares is not None:
            self._increase_hectares_indicator(KeyDicts.HECTARES_CONTRACT_DEALS,
                                              deal.contract_hectares,
                                              target_country)

	# Calculate and process the total hectares to add
        total_hectares_to_add = self._get_hectares_to_add(deal)

        if deal.negotiation_status == Deal.FAILED:
            self._increase_hectares_indicator(KeyDicts.HECTARES_FAILED_DEALS,
                                              total_hectares_to_add,
                                              target_country)



        self._increase_hectares_indicator(KeyDicts.HECTARES_TOTAL_DEALS,
                                          total_hectares_to_add,
                                          target_country)


    def _get_hectares_to_add(self, deal):
        """ The algorithm to obtain the hectares to add is:
             1) Try to obtain the contract hectares
             2) If not, try to obtain the intended hectares
             3) If not, try to obtain the production hectares
             4) If not, add 0 (zero)
            To run the algorithm, the initial value is set to 0 and the process write over the best value in reverse order.
	    Values equal or under 0 are discarded.
        """

        total_hectares_to_add = 0

        if deal.production_hectares is not None and deal.production_hectares > 0:
            total_hectares_to_add = deal.production_hectares

        if deal.intended_hectares is not None and deal.intended_hectares > 0:
            total_hectares_to_add = deal.intended_hectares

        if deal.contract_hectares is not None and deal.contract_hectares > 0:
            total_hectares_to_add = deal.contract_hectares

	return total_hectares_to_add


    def _increase_hectares_indicator(self, deal_key, hectares, country):
        """
        It increases in "max_hectares" the value of the entry under the key "deal_key + country"
        If the entry does not exist in the internal dict, it creates it.
        """
	# If hectares value is 0 or below, exit the function
	if hectares <= 0:
	   return
		
        compound_key = _get_compound_key(deal_key, country)

        #Creating new entry if needed
        if not compound_key in self._deals_dict:
            new_entry = DealAnalyserEntry(indicator=self._indicators_dict[deal_key],
                                          country=country,
                                          last_date=None,
                                          value=0)
            self._deals_dict[compound_key] = new_entry

        #Updating entry
        entry = self._deals_dict[compound_key]
        entry.value += hectares
        #Done, no return needed




    def _increase_counter_indicator(self, deal_key, country):
        """
        Increase in one unit the value of the appropiate entry in observations_dict
        If the entry does not exist, it also creates it

        """
        compound_key = _get_compound_key(deal_key, country)

        #Creating new entry in obs_dict if needed
        if not compound_key in self._deals_dict:
            new_entry = DealAnalyserEntry(indicator=self._indicators_dict[deal_key],
                                          country=country,
                                          last_date=None,
                                          value=0)
            self._deals_dict[compound_key] = new_entry
        #Updating entry
        entry = self._deals_dict[compound_key]
        entry.value += 1
        #Done. No return needed



##################################################################
#                            FUNCTIONS                           #
##################################################################


def _get_compound_key(deal_key, country):
    return str(deal_key) + country.iso3

# This method could me moved to Deal entity
def _is_in_production(deal):
   if (deal.implementation_status == Deal.IN_OPERATION):
      return True
   else:
      return False

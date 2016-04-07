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
        self.latest_date = 0  # It will store the latest date found between the date of every observations.


    def run(self):
        for a_deal in self._list_deals:
            target_country = self._process_target_country(a_deal.target_country)
            if not target_country is None:
                self._process_the_fact_that_the_deal_has_valid_country(target_country)
                self._process_deals_by_negotiation_status(a_deal, target_country)
                self._process_deals_by_topic(a_deal, target_country)
                self._process_deals_by_hectares(a_deal, target_country)
                self._procces_date(a_deal, target_country)
            else:
                raise RuntimeError("We have found a deal with a non recognized country."
                                   " Agregate values cuold be incorrect form this point, execution should stop. "
                                   "Country: " + a_deal.target_country)

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


    def _procces_date(self, deal, target_country):
        compound_key = _get_compound_key(KeyDicts.TOTAL_DEALS, target_country)  # We have to get an entry of some
                                                                        #indicator, it does not matter which...
                                                                        #but we know that TOTAL_DEALS exists with                                                                     #no doucbt when reaching this point
        current_date = self._deals_dict[compound_key].date
        if deal.date is not None and deal.date > current_date:
            self._update_date_of_all_entrys_of_a_country(target_country, deal.date)
        if deal.date is not None and deal.date > self.latest_date:
            self.latest_date = deal.date

    def _update_date_of_all_entrys_of_a_country(self, country, date):
        self._update_date_of_an_entry(KeyDicts.TOTAL_DEALS, country, date)
        self._update_date_of_an_entry(KeyDicts.INTENDED_DEALS, country, date)
        self._update_date_of_an_entry(KeyDicts.CONCLUDED_DEALS, country, date)
        self._update_date_of_an_entry(KeyDicts.FAILED_DEALS, country, date)

        self._update_date_of_an_entry(KeyDicts.AGRICULTURE_DEALS, country, date)
        self._update_date_of_an_entry(KeyDicts.BIOFUELS_DEALS, country, date)
        self._update_date_of_an_entry(KeyDicts.FOOD_CROPS_DEALS, country, date)
        self._update_date_of_an_entry(KeyDicts.LIVESTOCK_DEALS, country, date)
        self._update_date_of_an_entry(KeyDicts.NON_FOOD_AGRICULTURAL_COMMODITIES_DEALS, country, date)
        self._update_date_of_an_entry(KeyDicts.AGRIUNSPECIFIED_DEALS, country, date)

        self._update_date_of_an_entry(KeyDicts.CONSERVATION_DEALS, country, date)

        self._update_date_of_an_entry(KeyDicts.FORESTRY_DEALS, country, date)
        self._update_date_of_an_entry(KeyDicts.FOR_WOOD_AND_FIBRE_DEALS, country, date)
        self._update_date_of_an_entry(KeyDicts.FOR_CARBON_SEQUESTRATION_REDD_DEALS, country, date)
        self._update_date_of_an_entry(KeyDicts.FORESTUNSPECIFIED_DEALS, country, date)

        self._update_date_of_an_entry(KeyDicts.INDUSTRY_DEALS, country, date)
        self._update_date_of_an_entry(KeyDicts.RENEWABLE_ENERGY_DEALS, country, date)
        self._update_date_of_an_entry(KeyDicts.TOURISM_DEALS, country, date)
        self._update_date_of_an_entry(KeyDicts.OTHER_DEALS, country, date)
        self._update_date_of_an_entry(KeyDicts.UNKNOWN_DEALS, country, date)
        self._update_date_of_an_entry(KeyDicts.HECTARES_TOTAL_DEALS, country, date)
        self._update_date_of_an_entry(KeyDicts.HECTARES_INTENDED_DEALS, country, date)
        self._update_date_of_an_entry(KeyDicts.HECTARES_CONTRACT_DEALS, country, date)
        self._update_date_of_an_entry(KeyDicts.HECTARES_PRODUCTION_DEALS, country, date)

    def _update_date_of_an_entry(self, deal_key, country, date):
        """
        It updates the date of the entry if it exists. If not, it simply returns without doing anything

        """
        compound_key = _get_compound_key(deal_key, country)
        if not compound_key in self._deals_dict:  # If there is no entry, nothing to do
            return
        else:
            self._deals_dict[compound_key].date = date


    def _process_deals_by_topic(self, deal, target_country):

        if Deal.BIOFUELS in deal.sectors:
            self._increase_counter_indicator(KeyDicts.BIOFUELS_DEALS, target_country)
            self._increase_counter_indicator(KeyDicts.AGRICULTURE_DEALS, target_country)
        if Deal.FOOD_CROPS in deal.sectors:
            self._increase_counter_indicator(KeyDicts.FOOD_CROPS_DEALS, target_country)
            self._increase_counter_indicator(KeyDicts.AGRICULTURE_DEALS, target_country)
        if Deal.LIVESTOCK in deal.sectors:
            self._increase_counter_indicator(KeyDicts.LIVESTOCK_DEALS, target_country)
            self._increase_counter_indicator(KeyDicts.AGRICULTURE_DEALS, target_country)
        if Deal.NON_FOOD_AGRICULTURAL_COMMODITIES in deal.sectors:
            self._increase_counter_indicator(KeyDicts.NON_FOOD_AGRICULTURAL_COMMODITIES_DEALS, target_country)
            self._increase_counter_indicator(KeyDicts.AGRICULTURE_DEALS, target_country)
        if Deal.AGRIUNSPECIFIED in deal.sectors:
            self._increase_counter_indicator(KeyDicts.AGRIUNSPECIFIED_DEALS, target_country)
            self._increase_counter_indicator(KeyDicts.AGRICULTURE_DEALS, target_country)

        if Deal.CONSERVATION in deal.sectors:
            self._increase_counter_indicator(KeyDicts.CONSERVATION_DEALS, target_country)

        if Deal.FOR_WOOD_AND_FIBRE in deal.sectors:
            self._increase_counter_indicator(KeyDicts.FOR_WOOD_AND_FIBRE_DEALS, target_country)
            self._increase_counter_indicator(KeyDicts.FORESTRY_DEALS, target_country)
        if Deal.FOR_CARBON_SEQUESTRATION_REDD in deal.sectors:
            self._increase_counter_indicator(KeyDicts.FOR_CARBON_SEQUESTRATION_REDD_DEALS, target_country)
            self._increase_counter_indicator(KeyDicts.FORESTRY_DEALS, target_country)
        if Deal.FORESTUNSPECIFIED in deal.sectors:
            self._increase_counter_indicator(KeyDicts.FORESTUNSPECIFIED_DEALS, target_country)
            self._increase_counter_indicator(KeyDicts.FORESTRY_DEALS, target_country)


        if Deal.INDUSTRY in deal.sectors:
            self._increase_counter_indicator(KeyDicts.INDUSTRY_DEALS, target_country)
        if Deal.RENEWABLE_ENERGY in deal.sectors:
            self._increase_counter_indicator(KeyDicts.RENEWABLE_ENERGY_DEALS, target_country)
        if Deal.TOURISM in deal.sectors:
            self._increase_counter_indicator(KeyDicts.TOURISM_DEALS, target_country)
        if Deal.OTHER in deal.sectors:
            self._increase_counter_indicator(KeyDicts.OTHER_DEALS, target_country)
        if Deal.UNKNOWN in deal.sectors:
            self._increase_counter_indicator(KeyDicts.UNKNOWN_DEALS, target_country)


    def _process_deals_by_hectares(self, deal, target_country):
        """ The algorithm to obtain the value to add to the total hectares is:
             1) Try to obtain the contract hectares
             2) If not, try to obtain the intended hectares
             3) If not, try to obtain the production hectares
             4) If not, add 0 (zero)
            To run the algorithm, the initial value is set to 0 and the process write over the best value in reverse order.
        """

        if deal.production_hectares is not None:
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

	if total_hectares_to_add > 0 :
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
        """

        total_hectares_to_add = 0

        if deal.production_hectares is not None:
            total_hectares_to_add = deal.production_hectares

        if deal.intended_hectares is not None:
            total_hectares_to_add = deal.intended_hectares

        if deal.contract_hectares is not None:
            total_hectares_to_add = deal.contract_hectares

	return total_hectares_to_add


    def _increase_hectares_indicator(self, deal_key, hectares, country):
        """
        It increases in "max_hectares" the value of the entry under the key "deal_key + country"
        If the entry does not exist in the internal dict, it creates it.
        """
        compound_key = _get_compound_key(deal_key, country)

        #Creating new entry if needed
        if not compound_key in self._deals_dict:
            new_entry = DealAnalyserEntry(indicator=self._indicators_dict[deal_key],
                                          country=country,
                                          date=None,
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
                                          date=None,
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

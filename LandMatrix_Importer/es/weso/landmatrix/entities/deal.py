__author__ = 'Dani'
import re

class Deal(object):

    # Negotiation status
    INTENDED = "Intended"
    CONCLUDED = "Concluded"
    FAILED = "Failed"

    # Implementation status
    IN_OPERATION = "In operation (production)"
    STARTUP_PHASE = "Startup phase (no production)"
    PROJECT_NOT_STARTED = "Project not started"
    PROJECT_ABANDONED = "Project abandoned"

    # This must match the intention value, removing the blank spaces"
    # Sectors
    AGRICULTURE = "Agriculture"
    BIOFUELS = "Biofuels"
    FOOD_CROPS = "Foodcrops"
    LIVESTOCK = "Livestock"
    NON_FOOD_AGRICULTURAL_COMMODITIES = "Nonfoodagriculturalcommodities"
    AGRIUNSPECIFIED = "Agricultureunspecified"
    FOODER = "Fodder"

    CONSERVATION = "Conservation"

    FORESTRY = "Forestry"
    TIMBER_FOR_WOOD_AND_FIBRE = "Timberplantation(forwoodandfibre)"
    LOGGING_FOR_WOOD_AND_FIBRE = "Forestlogging/management(forwoodandfibre)"
    FOR_CARBON_SEQUESTRATION_REDD = "Forcarbonsequestration/REDD"
    FORESTUNSPECIFIED = "Forestryunspecified"

    INDUSTRY = "Industry"
    RENEWABLE_ENERGY = "RenewableEnergy"
    TOURISM = "Tourism"
    OTHER = "Other(pleasespecify)"
    UNKNOWN = "Unknown"

    MINING = "Mining"
    LANDSPECULATION = "Landspeculation"
    OIL_GAS = "Oil/Gasextraction"

    def __init__(self, target_country=None, production_hectares=None, contract_hectares=None,
                 intended_hectares=None, date=None, sectors=None, negotiation_status=None, implementation_status=None):
        self.target_country = target_country
        self.production_hectares = production_hectares
        self.contract_hectares = contract_hectares
        self.intended_hectares = intended_hectares
        self.date = date
        self.sectors = sectors
        self.negotiation_status = negotiation_status
	self.implementation_status = implementation_status

    def __str__(self):
	sb = list()
	for key in self.__dict__:
	    value = self.__dict__[key]
	    if isinstance(value, unicode):
		value = self.__dict__[key].encode('utf-8') # transfor to str to allow 
	    if (key=="date"):# and value not in ["In operation (production)", "Project not started", "Startup phase (no production)", "Project abandoned"]:
	       pass#print(value)
	    sb.append("{key}='{value}'".format(key=key, value=value))
 
	return ', '.join(sb)
 
    def __repr__(self):
	return self.__str__() 

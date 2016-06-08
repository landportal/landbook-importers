__author__ = 'Dani'


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
    NON_FOOD_AGRICULTURAL_COMMODITIES = "Non-foodagriculturalcommodities"
    AGRIUNSPECIFIED = "Agriunspecified"

    CONSERVATION = "Conservation"

    FORESTRY = "Forestry"
    FOR_WOOD_AND_FIBRE = "Forwoodandfibre"
    FOR_CARBON_SEQUESTRATION_REDD = "Forcarbonsequestration/REDD"
    FORESTUNSPECIFIED = "Forestunspecified"

    INDUSTRY = "Industry"
    RENEWABLE_ENERGY = "RenewableEnergy"
    TOURISM = "Tourism"
    OTHER = "Other(pleasespecify)"
    UNKNOWN = "Unknown"



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
	sb = []
	for key in self.__dict__:
	    value = (self.__dict__[key])
	    if isinstance(value, unicode):
		value = (self.__dict__[key]).encode('utf-8') # transfor to str to allow 
	    sb.append("{key}='{value}'".format(key=key, value=value))
 
	return ', '.join(str(sb))
 
    def __repr__(self):
	return self.__str__() 

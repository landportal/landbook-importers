__author__ = 'Dani'


class Deal(object):

    #Negotiation status
    INTENDED = "Intended"
    CONCLUDED = "Concluded"
    FAILED = "Failed"

    #Sectors
    AGRICULTURE = "Agriculture"
    BIOFUELS = "Biofuels"
    CONSERVATION = "Conservation"
    FORESTRY = "Forestry"
    INDUSTRY = "Industry"
    RENEWABLE_ENERGY = "RenewableEnergy"
    TOURISM = "Tourism"
    OTHER = "Other"
    UNKNOWN = "Unknown"



    def __init__(self, target_country=None, production_hectares=None, contract_hectares=None,
                 intended_hectares=None, date=None, sectors=None, negotiation_status=None):
        self.target_country = target_country
        self.production_hectares = production_hectares
        self.contract_hectares = contract_hectares
        self.intended_hectares = intended_hectares
        self.date = date
        self.sectors = sectors
        self.negotiation_status = negotiation_status

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

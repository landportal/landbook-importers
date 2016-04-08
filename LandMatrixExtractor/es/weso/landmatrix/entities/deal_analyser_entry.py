__author__ = 'Dani'


class DealAnalyserEntry(object):
    """
    The DealAnalyser will return a dict that saves under a key composed by Country and indicator
    certains group of entities.
    This class contains all this elements: an indicator, a first_date (see deatils), a last_date (int), a country (country entity) and a value.
    Details about first_date:
    From http://www.landmatrix.org/en/about/#what-is-a-land-deal
    Deals must: 
       - Have been initiated since the year 2000;
    """

    def __init__(self, indicator, last_date, country, value):
        self.indicator = indicator
        self.last_date = last_date
        self.country = country
        self.value = value
	self.first_date = 2000

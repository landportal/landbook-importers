'''
Created on 18/12/2013

@author: Nacho
'''
from lpentities.computation import Computation
from lpentities.dataset import Dataset
from lpentities.indicator import Indicator
from lpentities.value import Value


class Observation(object):
    '''
    classdocs
    '''

    def __init__(self, chain_for_id, int_for_id, ref_time=None, issued=None,
                 computation=None, value=None, indicator=None, dataset=None, note=None):
        '''
        Constructor
        '''

        self.ref_time = ref_time
        self.issued = issued
        self._computation = computation
        self._value = value
        self._indicator = indicator
        self._dataset = dataset
        self._note = note 
        self.group = None
        self.indicator_group = None
        self._int_for_id = int_for_id

    def get_observation_id(self):
	indicator_id = str(self._indicator.indicator_id)
	country_id = self.region._iso3
	time_id = self.ref_time.get_time_string()
	return indicator_id + "_" + country_id + "_" + time_id

    def __get_computation(self):
        return self._computation
    
    def __set_computation(self, computation):
        if isinstance(computation, Computation) :
            self._computation = computation
        else:
            raise ValueError("Expected Computation object in Observation")
        
    computation = property(fget=__get_computation,
                      fset=__set_computation,
                      doc="The computation for the observation")

    def __get_value(self):
        return self._value
    
    def __set_value(self, value):
        if isinstance(value, Value) :
            self._value = value
        else:
            raise ValueError("Expected Value object in Observation")
        
    value = property(fget=__get_value,
                      fset=__set_value,
                      doc="The value for the observation")

    def __get_indicator(self):
        return self._indicator
    
    def __set_indicator(self, indicator):
        if isinstance(indicator, Indicator) :
            self._indicator = indicator
        else:
            raise ValueError("Expected Indicator object in Observation")
        
    indicator = property(fget=__get_indicator,
                      fset=__set_indicator,
                      doc="The indicator for the observation")

    def __get_dataset(self):
        return self._dataset
    
    def __set_dataset(self, dataset):
        if isinstance(dataset, Dataset) :
            self._dataset = dataset
        else:
            raise ValueError("Expected Dataset object in Observation")
        
    dataset = property(fget=__get_dataset,
                      fset=__set_dataset,
                      doc="The dataset for the observation")

    def __get_note(self):
        return self._note
    
    def __set_note(self, note):
        self._note = note
        
    note = property(fget=__get_note,
                    fset=__set_note,
                    doc="The note for the observation")

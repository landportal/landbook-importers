'''
Created on 02/02/2014

@author: Miguel Otero
'''
from lpentities.dataset import Dataset


class DataSource(object):
    '''
    classdocs
    '''


    def __init__(self, chain_for_id=None, int_for_id=None, name=None, organization=None):
        '''
        Constructor
        '''

        self.name = name
        self.organization = organization
        self.datasets = []
        self.source_id = self._generate_id(chain_for_id, int_for_id)


    @staticmethod
    def _generate_id(chain_for_id, int_for_id):
        return "SOU" + chain_for_id.upper() + str(int_for_id).upper()


    def add_dataset(self, dataset):
        if isinstance(dataset, Dataset):
            self.datasets.append(dataset)
            dataset.source = self
        else:
            raise ValueError("Trying to append a non dataset object to datasource")
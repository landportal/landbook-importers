'''
Created on 21/01/2014

@author: Miguel Otero
'''

import logging
from es.weso.faogenderextractor.web_access.selenium_access import SeleniumAccess

class FaoGenderExtractor(object):
    '''
    classdocs
    '''
    
    logger = logging.getLogger('faogender_extractor')
    rest_client= SeleniumAccess()

    def __init__(self):
        '''
        Constructor
        '''
        self.countries = []
        
    def extract_countries(self):
        self.rest_client.obtain_countries()
    
    
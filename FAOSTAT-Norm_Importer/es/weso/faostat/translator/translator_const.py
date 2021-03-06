'''
Created on 03/02/2014

@author: Dani
'''

class TranslatorConst(object):
    '''
    This class is only used to provide some constants handy for many class of the package

    '''
    COUNTRY_CODE = 0
    COUNTRY = 1
    ITEM_CODE = 2
    ITEM = 3
    ELEMENT_CODE = 4
    ELEMENT = 5
    YEAR_CODE = 6
    YEAR = 7
    UNIT = 8
    VALUE = 9
    FLAG = 10
    COMPUTATION_PROCESS = 11  # Non-parsed field
    EXPECTED_NUMBER_OF_COLS = 11  # All the fields but the non-parsed COMPUTATION_PROCESS
    

    CODE_LAND_AREA = "6601-5110"
    CODE_AGRICULTURAL_LAND = "6610-5110"
    CODE_FOREST_LAND = "6646-5110"
    CODE_ARABLE_LAND = "6621-5110"
    CODE_PERMANENT_CROPS = "6650-5110"
    CODE_PERMANENT_MEADOW_AND_PASTURES = "6655-5110"
    CODE_AGRICULTURAL_AREA_ORGANIC = "6671-5110"

    CODE_WATER = "6720-5510"

    #  The next three are random numbers that are not it the previous indicator codes.
    CODE_RELATIVE_AGRICULTURAL_LAND = "X-6610-5110"
    CODE_RELATIVE_ARABLE_LAND = "X-6621-5110"
    CODE_RELATIVE_FOREST_LAND = "X-6646-5110"
    

        

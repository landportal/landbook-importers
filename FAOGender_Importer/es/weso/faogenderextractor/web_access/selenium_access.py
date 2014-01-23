'''
Created on 21/01/2014

@author: Miguel Otero
'''

import logging
from selenium import webdriver
from time import sleep

class SeleniumAccess(object):
    '''
    classdocs
    ''' 
    logger = logging.getLogger('selenium_access')

    def __init__(self):
        '''
        Constructor
        '''
        
    def obtain_countries(self):
        driver = webdriver.Firefox()    
        driver.get('http://www.fao.org/gender/landrights/topic-selection/en/')
        radioButton = driver.find_element_by_id('7')
        radioButton.click()
        countryCheckboxes = driver.find_elements_by_css_selector("input[type='checkbox']")
        for checkbox in countryCheckboxes:
            checkbox.click()
        submitButton = driver.find_element_by_id('report')
        submitButton.click()
        sleep(0.5)
        englishButton = driver.find_element_by_css_selector("#report_79 .dls a")
        englishButton.click()
        sleep(0.5)
        countryReports = driver.find_elements_by_css_selector("div[class='report_x']")
        for countryReport in countryReports:
            country = countryReport.find_element_by_css_selector("div[class='country']")
            languageTextLength = len(country.find_element_by_css_selector("span").text)
            wholeTextLength = len(country.text)
            print country.text[0:(wholeTextLength - languageTextLength)]
            indicatorValues = countryReport.find_elements_by_css_selector("div[class='data']")
            for value in indicatorValues:
                textValue = value.text.encode('utf-8')
                print '\t' + textValue.replace(' ', '').replace('\r', '').replace('\n', '').replace(',', '')
        driver.close()
    
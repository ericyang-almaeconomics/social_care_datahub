from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from urllib.request import urlopen
import pandas as pd

SLEEP = 2


class SocialCareDatahubTest(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        self.browser = webdriver.Chrome(executable_path = r'C:\Users\DimitrisIntzeler\Downloads\chromedriver.exe', chrome_options=options)

    def tearDown(self):
        self.browser.quit()

    def userLogin(self):
        time.sleep(SLEEP)
        self.browser.get("http://localhost:8000/search/")
        self.browser.find_element(By.ID, "id_username").send_keys("dimitris")
        self.password = self.browser.find_element(By.ID, "id_password")
        self.password.send_keys("123456789")
        self.password.submit()

    def userSearch(self, local_authority_values, region_values, england_click, year_index, disaggregation_xpath, measure_group_description_value):
        if local_authority_values:
            local_authority = self.browser.find_element(By.ID, "id_local_authority")
            select_local_authority = Select(local_authority)
            for local_authority_value in local_authority_values:
                select_local_authority.select_by_value(local_authority_value)
                time.sleep(SLEEP)


        if region_values:
            region = self.browser.find_element(By.ID, "id_region")
            select_region = Select(region)
            for region_value in region_values:
                select_region.select_by_value(region_value)
                time.sleep(SLEEP)

        if england_click:
            england = self.browser.find_element(By.XPATH, '//*[@id="div_id_england"]/label')
            england.click()
            time.sleep(SLEEP)

        year = self.browser.find_element(By.ID, "id_year")
        select_year = Select(year)
        select_year.select_by_index(year_index)
        time.sleep(SLEEP)

        if disaggregation_xpath:
            disaggregation = self.browser.find_element(By.XPATH,disaggregation_xpath)
            disaggregation.click()
            time.sleep(SLEEP)
        
        if measure_group_description_value:
            measure_group_description = self.browser.find_element(By.ID, "id_measure_group_description")
            select_measure_group_description = Select(measure_group_description)
            select_measure_group_description.select_by_value(measure_group_description_value)
            time.sleep(SLEEP)

        search = self.browser.find_element(By.ID,"search_button")
        self.browser.execute_script("arguments[0].click();", search)
        time.sleep(SLEEP)

    
    def test_userLogin(self):
        self.userLogin()
        if self.browser.current_url != "http://localhost:8000/search/":
            self.fail("Not expected")
        time.sleep(SLEEP)

    def test_search_local_authority(self):
        time.sleep(SLEEP)
        self.userLogin()
        self.userSearch(local_authority_values = ['Barnet','Bath and North East Somerset'], region_values=None, england_click=False, year_index=2, disaggregation_xpath='//*[@id="div_id_disaggregation"]/div/div[1]/label', measure_group_description_value = 'Long-term support needs of older adults (aged 65 and over) met by admission to residential and nursing care homes, per 100,000 population')
        if self.browser.current_url != "http://localhost:8000/results/":
            self.fail("Not expected")
        time.sleep(SLEEP)        


    def test_search_region(self):
        time.sleep(SLEEP)
        self.userLogin()
        self.userSearch(local_authority_values = None, region_values=['London'], england_click=False, year_index=2, disaggregation_xpath='//*[@id="div_id_disaggregation"]/div/div[1]/label', measure_group_description_value = 'Long-term support needs of older adults (aged 65 and over) met by admission to residential and nursing care homes, per 100,000 population')
        if self.browser.current_url != "http://localhost:8000/results/":
            self.fail("Not expected")
        time.sleep(SLEEP)   


    def test_search_england(self):
        time.sleep(SLEEP)
        self.userLogin()
        self.userSearch(local_authority_values = None, region_values=None, england_click=True, year_index=2, disaggregation_xpath='//*[@id="div_id_disaggregation"]/div/div[1]/label', measure_group_description_value = 'Long-term support needs of older adults (aged 65 and over) met by admission to residential and nursing care homes, per 100,000 population')
        if self.browser.current_url != "http://localhost:8000/results/":
            self.fail("Not expected")
        time.sleep(SLEEP)   

    def test_search_local_authority(self):
        time.sleep(SLEEP)
        self.userLogin()
        self.userSearch(local_authority_values = ['Barnet','Bath and North East Somerset'], region_values=None, england_click=False, year_index=2, disaggregation_xpath='//*[@id="div_id_disaggregation"]/div/div[1]/label', measure_group_description_value = 'Long-term support needs of older adults (aged 65 and over) met by admission to residential and nursing care homes, per 100,000 population')
        if self.browser.current_url != "http://localhost:8000/results/":
            self.fail("Not expected")
        time.sleep(SLEEP)   

    def test_search_wrong_input(self):
        time.sleep(SLEEP)
        self.userLogin()

        #choose local authority and region
        self.userSearch(local_authority_values = ['Barnet','Bath and North East Somerset'], region_values=['London'], england_click = False, year_index=2, disaggregation_xpath='//*[@id="div_id_disaggregation"]/div/div[1]/label', measure_group_description_value = 'Long-term support needs of older adults (aged 65 and over) met by admission to residential and nursing care homes, per 100,000 population')
        alert = self.browser.find_element(By.XPATH, '//*[@id="main-body-container"]/ul/div')
        if alert.text != "You must fill in either only one of the fields Local Authority and Region or tick the England checkbox":
            self.fail("Not expected behaviour")
        time.sleep(SLEEP)
        if self.browser.current_url != "http://localhost:8000/search/":
            self.fail("Not expected redirect")
        time.sleep(SLEEP)

        #choose  local authority and england
        self.userSearch(local_authority_values = ['Barnet','Bath and North East Somerset'], region_values=None, england_click = True, year_index=2, disaggregation_xpath='//*[@id="div_id_disaggregation"]/div/div[1]/label', measure_group_description_value = 'Long-term support needs of older adults (aged 65 and over) met by admission to residential and nursing care homes, per 100,000 population')
        alert = self.browser.find_element(By.XPATH, '//*[@id="main-body-container"]/ul/div')
        if alert.text != "You must fill in either only one of the fields Local Authority and Region or tick the England checkbox":
            self.fail("Not expected behaviour")
        time.sleep(SLEEP)
        if self.browser.current_url != "http://localhost:8000/search/":
            self.fail("Not expected redirect")
        time.sleep(SLEEP)

        #choose region and england        
        self.userSearch(local_authority_values = None, region_values=['London'], england_click = True, year_index=2, disaggregation_xpath='//*[@id="div_id_disaggregation"]/div/div[1]/label', measure_group_description_value = 'Long-term support needs of older adults (aged 65 and over) met by admission to residential and nursing care homes, per 100,000 population')
        alert = self.browser.find_element(By.XPATH, '//*[@id="main-body-container"]/ul/div')
        if alert.text != "You must fill in either only one of the fields Local Authority and Region or tick the England checkbox":
            self.fail("Not expected behaviour")
        time.sleep(SLEEP)
        if self.browser.current_url != "http://localhost:8000/search/":
            self.fail("Not expected redirect")
        time.sleep(SLEEP)

        #choose all three fields
        self.userSearch(local_authority_values = ['Barnet','Bath and North East Somerset'], region_values=['London'], england_click = True, year_index=2, disaggregation_xpath='//*[@id="div_id_disaggregation"]/div/div[1]/label', measure_group_description_value = 'Long-term support needs of older adults (aged 65 and over) met by admission to residential and nursing care homes, per 100,000 population')
        alert = self.browser.find_element(By.XPATH, '//*[@id="main-body-container"]/ul/div')
        if alert.text != "You must fill in either only one of the fields Local Authority and Region or tick the England checkbox":
            self.fail("Not expected behaviour")
        time.sleep(SLEEP)
        if self.browser.current_url != "http://localhost:8000/search/":
            self.fail("Not expected redirect")
        time.sleep(SLEEP)

    def test_search_no_results(self):
        time.sleep(SLEEP)
        self.userLogin()
        self.userSearch(local_authority_values = ['Barking and Dagenham'], region_values=None, england_click=False, year_index=0, disaggregation_xpath='//*[@id="div_id_disaggregation"]/div/div[3]/label', measure_group_description_value = 'Long-term support needs of younger adults (aged 18-64) met by admission to residential and nursing care homes, per 100,000 population')

        alert = self.browser.find_element(By.XPATH, '//*[@id="main-body-container"]/ul/div')

        if alert.text != "No results":
            self.fail("Not expected behaviour")
        time.sleep(SLEEP)

        if self.browser.current_url != "http://localhost:8000/search/":
            self.fail("Not expected redirect")
        time.sleep(SLEEP)
    

    def test_results(self):
        time.sleep(SLEEP)
        self.userLogin()       
        self.userSearch(local_authority_values = ['Barnet','Bath and North East Somerset'], region_values=None, england_click=False, year_index=2, disaggregation_xpath='//*[@id="div_id_disaggregation"]/div/div[1]/label', measure_group_description_value = 'Long-term support needs of older adults (aged 65 and over) met by admission to residential and nursing care homes, per 100,000 population')
        time.sleep(SLEEP)

        #check if table exists
        try:
            table = self.browser.find_element(By.ID, 'results_table')
        except:
            self.fail("No table")

        #check if 'Export to Excel' button exists
        try:
            export_to_excel_button = self.browser.find_element(By.ID, 'export_to_excel')
        except:
            self.fail("Export to excel button not found")

        time.sleep(SLEEP)

        

if __name__ == '__main__':  
    unittest.main()
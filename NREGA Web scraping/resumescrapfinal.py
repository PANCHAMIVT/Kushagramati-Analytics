
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.webdriver import NoSuchElementException
import os
from selenium.common.exceptions import WebDriverException

# create web driver


def driverFun(link):
    driver = webdriver.Chrome(executable_path='D:/chrome selenium/chromedriver.exe')
    driver.get(link)
    return driver

# this functions using to create a folders
# using os commands
def stateFun(slink):
    os.mkdir('D:\\Scrap\\'+slink)


def disFun(slink, dlink):
    os.mkdir('D:\\Scrap\\'+slink+'\\'+dlink)


def blockFun(slink, dlink, blink):
    os.mkdir('D:\\Scrap\\'+slink+'\\'+dlink+'\\'+blink)


# this functions using to get a links
# @inputs
# it will return list formate
def getState(link):
    driver = driverFun(link)
    states = [slink for slink in driver.find_elements(
        By.XPATH, '//*[@id="form1"]/div[3]/center/table/tbody/tr/td/a')]
    return states


def getDistrict(link):
    driver = driverFun(link.get_attribute('href'))
    districtLink = [dlink for dlink in driver.find_elements(
        By.XPATH, '//*[@id="gvdist"]/tbody/tr/td/a')]
    return districtLink


def getBlock(dlink):
    driver = driverFun(dlink.get_attribute('href'))
    blockLinks = [blink for blink in driver.find_elements(
        By.XPATH, '//*[@id="gvdpc"]/tbody/tr/td/a')]
    return blockLinks

# this function using to download a files one by one
# It will stored pecific locations
def fun(slink, dlink, blink):
    op = webdriver.ChromeOptions()
    p = {'download.default_directory': 'D:\\Scrap\\' +
         slink.text+'\\'+dlink.text+'\\'+blink.text}
    print(blink.text)
    op.add_experimental_option('prefs', p)
    driver = webdriver.Chrome(executable_path='D:/chrome selenium/chromedriver.exe', options=op)
    link = blink.get_attribute('href')
    driver.get(link)
    try:
        expenditure = driver.find_element(By.LINK_TEXT, 'Amount Sanctioned/Expenditure On Works')
        driver.get(expenditure.get_attribute('href'))
        dropdown = driver.find_element(
            By.XPATH, '/html/body/form/div[3]/center/table/tbody/tr[1]/td[4]/b/font/select')
        panchayat = Select(dropdown)
        list = panchayat.options
        for i in range(2, len(list)):
            driver.get(link)
            expenditure = driver.find_element(
                By.LINK_TEXT, 'Amount Sanctioned/Expenditure On Works')
            driver.get(expenditure.get_attribute('href'))
            dropdown = driver.find_element(
                By.XPATH, '/html/body/form/div[3]/center/table/tbody/tr[1]/td[4]/b/font/select')
            panchayats = Select(dropdown)
            panchayats.select_by_index(i)
            try:
                driver.find_element(
                    By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_Btnreport"]').click()
                driver.find_element(
                    By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_LinkButton1"]').click()
            except WebDriverException:
                print("no : "+str(i)+" ==> no data found")
    except NoSuchElementException:
        print("the service is unavailable")

def dis(slink):
    districtLink = getDistrict(slink)
    for dlink in districtLink:
            try:
                disFun(slink.text, dlink.text)
                blo(slink,dlink)
            except FileExistsError:
                blo(slink,dlink)


def blo(slink,dlink):
    blockLink = getBlock(dlink)
    for blink in blockLink:
        try:
            blockFun(slink.text, dlink.text, blink.text)
            fun(slink, dlink, blink)
        except FileExistsError:
            continue



# this codes is a main function codes
link = "https://nrega.nic.in/Netnrega/sthome.aspx"
# list variable
stateLinks = getState(link)
for slink in stateLinks:
    try:
        stateFun(slink.text)
        dis(slink)
    except FileExistsError:
        dis(slink)

import time
import datetime
import sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from mytable_lucien import mycsv
import os
import yaml

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    MYDIR=os.path.dirname(os.path.abspath(sys.executable))
    PAUSE_BEFORE_EXIT = True
else:
    MYDIR=os.path.dirname(os.path.abspath(__file__))
    PAUSE_BEFORE_EXIT = False

TOTAL_COURSES = 8

__mycorres = mycsv.read(MYDIR + '/data/course_list/c.csv')
CORRES = {}
for __corres in __mycorres:
    CORRES[__corres[0]] = __corres[1] # CORRES['an'] = '安'

def myprint(mystr):
    print(mystr)
    with open(MYDIR + '/log.txt','a+',encoding='utf8') as f:
        f.write(mystr + '\n')

def Clickx(_drivr,ele): #Click on the ele(ment) through xpath by ActionChains
    spot=_drivr.find_element(by=By.XPATH,value=ele)
    ActionChains(_drivr).click(spot).perform()

def Enterx(_drivr,word,ele): #Put the word in the ele(ment) through xpath
    spot=_drivr.find_element(by=By.XPATH,value=ele)
    spot.send_keys(Keys.CONTROL,'a') #Select all, making sure it's empty
    spot.send_keys(word)

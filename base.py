import time
import datetime
import sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
import chardet
import os
import yaml

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    MYDIR=os.path.dirname(os.path.abspath(sys.executable))
    PAUSE_BEFORE_EXIT = True
else:
    MYDIR=os.path.dirname(os.path.abspath(__file__))
    PAUSE_BEFORE_EXIT = False

def mycsv(filename):
    with open(filename,'rb') as f:
        text = f.read()
        res = chardet.detect(text)

    with open(filename, 'r', encoding=res['encoding']) as csvfile:
        myreader = csv.reader(csvfile)
        return [x for x in list(myreader) if x != []]

TOTAL_COURSES = 8

__mycorres = mycsv(MYDIR + '/data/course_list/c.csv')
CORRES = {}
for __corres in __mycorres:
    CORRES[__corres[0]] = __corres[1] # CORRES['an'] = '安'

with open(MYDIR + '/settings.yaml','r',encoding='utf-8') as g:
    settings = yaml.full_load(g.read())
LOG = settings['runtime']['log']
CMDOUT = settings['runtime']['cmdout']
WAIT_INTERVAL = settings['driver']['wait_interval']

def myprint(mystr):
    if CMDOUT:
        sys_platform = sys.platform
        if 'win' in sys_platform:
            cmdstrs = mystr.split('\n')
            for cmdstr in cmdstrs:
                os.system('echo=%s'%(cmdstr))
        else:
            os.system('echo "%s"'%(mystr))
    else:
        print(mystr)
    if LOG:
        with open(MYDIR + '/log.txt','a+',encoding='utf-8') as f:
            f.write(mystr + '\n')

def Clickx(_drivr,ele): #Click on the ele(ment) through xpath by ActionChains
    spot=_drivr.find_element(by=By.XPATH,value=ele)
    ActionChains(_drivr).click(spot).perform()

def Enterx(_drivr,word,ele): #Put the word in the ele(ment) through xpath
    spot=_drivr.find_element(by=By.XPATH,value=ele)
    spot.send_keys(Keys.CONTROL,'a') #Select all, making sure it's empty
    spot.send_keys(word)

def selenium_wait(_drivr,ele): # 检测ele存在
    wait_time = 8
    wait_step = WAIT_INTERVAL
    res = False
    for i in range(int(wait_time/wait_step)):
        try:
            spot = _drivr.find_element(by=By.XPATH,value=ele)
        except:
            time.sleep(wait_step)
        else:
            res = True
            break
    return res

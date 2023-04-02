# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 10:59:17 2022
@author: TommyLo
"""

#################################################
## Google Keywords Search Result Scraper
##
## How to use:
## - input the list of keywords interested into the Gsheet (or xlsx file) 
## - run the script and it will return the result of first X pages (X to be defined on the script)
#################################################

import undetected_chromedriver as uc  #<-- special driver used for remote server
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date
import time
import pandas as pd

#Define working directory
wd = r'E:\SEO'

#Read Keyword file
df_keywords = pd.read_excel(wd+r'\keywords.xlsx')

# No. of top N result extracting
n_result = 100

# initializing
se_results = []
n_keyword = 0


#Loop over keyword list
for keyword in list(df_keywords['Keywords']):

    #Start webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
#    options.add_argument("--headless") #hidden browser
#    options.add_experimental_option('excludeSwitches', ['enable-logging']) #To fix device event log error
#    options.use_chromium = True  #To fix device event log error
#    options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")
#    options.binary_location = r"C:\Program Files\Google\Chrome\Application\Chrome.exe"
#    driver = webdriver.Chrome(executable_path=r'C:\TommyLo\google-rank-tracker\chromedriver.exe',chrome_options=options)    
    driver = uc.Chrome(options=options)

    n_rank = 0 #reset rank
    n_keyword += 1
    url = 'https://www.google.co.id/search?num={}&q={}'.format(n_result,keyword)
    print('#{} --- {} --- {} ...'.format(n_keyword,keyword,url))
    driver.get(url)    
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    #SEM class start with 'v5yQqb'  <--pls check if update needed
    #Organic class start with 'yuRUbf'   
    results_selector = soup.select('div[class*="v5yQqb"] , div[class*="yuRUbf"]')
    
    # print(results_selector)
    # #Loop over the results
    for result_selector in results_selector:
        # Case when SEM / Organic Result
        if result_selector['class'][0].startswith('v5yQqb'):
            result_type = 'SEM'

        else:
            result_type = 'Organic'
        link = result_selector.select('a')[0]['href']
        n_rank += 1
        temp_dict = {
            'query_date' : date.today().strftime("%Y%m%d"),
            'keyword' : keyword,
            'rank' : n_rank,
            'result_type' : result_type,
            'link' : link
            }        
        se_results.append(temp_dict)
        

    time.sleep(10)

    driver.close()
    driver.quit()



import pandas as pd
df_se_results = []
for data in se_results:
    if "solideflex" in data['link']:
        
        df_se_results.append(data);

# print(df_se_results)
###Export to excel
# df_se_results.to_excel(wd+r'\results\se_result_{}.xlsx'.format(date.today().strftime("%Y%m%d")),encoding='utf-8',index=False)

###Export to csv
df_se = pd.DataFrame(df_se_results)
df_se.to_csv(wd+r'\results\se_result_{}.csv'.format(date.today().strftime("%Y%m%d")),encoding='utf-8',index=False)
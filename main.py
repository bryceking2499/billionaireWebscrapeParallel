# The goal of this app is to provide a sample of what Python Dash is capable of

# Uncomment the following lines if you would like to install additional libraries
# import pip
# pip.main(['install',
#           'dash', 'dash-html-components', 'dash-core-components', 'pandas', 'plotly', 'selenium',
#           'webdriver_manager', 'joblib'])

from datetime import date
from joblib import Parallel, delayed
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

bloomberg_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
bloomberg_driver.get("https://www.bloomberg.com/billionaires/")

list_of_rank_elements = bloomberg_driver.find_elements(by=By.XPATH, value='//div[@class="table-cell t-rank"]')

bloomberg_date_pulled = []
bloomberg_bil_rank = []
bloomberg_name = []
bloomberg_total_worth = []
bloomberg_daily_change = []
bloomberg_yearly_change = []
bloomberg_country_region = []
bloomberg_industry = []
wiki_links = []

for rank in range(len(list_of_rank_elements)):
    today = date.today()
    bloomberg_date_pulled.append(today)
    # Get rank and add to list
    rank_text = list_of_rank_elements[rank].text
    bloomberg_bil_rank.append(rank_text)

    # Get name and add to list
    xpath = '//div[@class="table-cell t-rank" and normalize-space(text())="' + str(rank + 1) + '"]/../div[2]/a'
    name_element = bloomberg_driver.find_element(by=By.XPATH, value=xpath)
    name_text = name_element.text
    bloomberg_name.append(name_text)

    # Get total worth and add to list
    xpath = '//div[@class="table-cell t-rank" and normalize-space(text())="' + str(rank + 1) + '"]/../div[3]'
    total_worth_element = bloomberg_driver.find_element(by=By.XPATH, value=xpath)
    total_worth_text = total_worth_element.text
    bloomberg_total_worth.append(total_worth_text)

    # Get daily change in worth and add to list
    xpath = '//div[@class="table-cell t-rank" and normalize-space(text())="' + str(rank + 1) + '"]/../div[4]'
    daily_change_element = bloomberg_driver.find_element(by=By.XPATH, value=xpath)
    daily_change_text = daily_change_element.text
    bloomberg_daily_change.append(daily_change_text)

    # Get yearly change and add to list
    xpath = '//div[@class="table-cell t-rank" and normalize-space(text())="' + str(rank + 1) + '"]/../div[5]'
    yearly_change_element = bloomberg_driver.find_element(by=By.XPATH, value=xpath)
    yearly_change_text = yearly_change_element.text
    bloomberg_yearly_change.append(yearly_change_text)

    # Get country/region and add to list
    xpath = '//div[@class="table-cell t-rank" and normalize-space(text())="' + str(rank + 1) + '"]/../div[6]'
    country_region_element = bloomberg_driver.find_element(by=By.XPATH, value=xpath)
    country_region_text = country_region_element.text
    bloomberg_country_region.append(country_region_text)

    # Get industry and add to list
    xpath = '//div[@class="table-cell t-rank" and normalize-space(text())="' + str(rank + 1) + '"]/../div[7]'
    industry_element = bloomberg_driver.find_element(by=By.XPATH, value=xpath)
    industry_text = industry_element.text
    bloomberg_industry.append(industry_text)

    substring = '& family'
    name_text = name_text.removesuffix(substring).replace(' ', '_')
    wikipedia_link = 'https://en.wikipedia.org/wiki/' + name_text
    wiki_links.append(wikipedia_link)


def wiki_driver(wiki_link):
    wikipedia_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wikipedia_driver.get(wiki_link)
    birthplace_text = "NA"
    birthplace_list = wikipedia_driver.find_elements(by=By.XPATH, value='//*[@class="birthplace"]')
    if birthplace_list:
        birthplace = birthplace_list[len(birthplace_list) - 1]
        birthplace_text = birthplace.text
    return birthplace_text


birthplace_texts = Parallel(n_jobs=-1)(delayed(wiki_driver)(wiki_link) for wiki_link in wiki_links)
print(birthplace_texts)

bloomberg_df = pd.DataFrame()
bloomberg_df['date'] = bloomberg_date_pulled
bloomberg_df['date'] = pd.to_datetime(bloomberg_df['date'])
bloomberg_df['rank'] = bloomberg_bil_rank
bloomberg_df['name'] = bloomberg_name
bloomberg_df['total_worth'] = bloomberg_total_worth
bloomberg_df['daily_change'] = bloomberg_daily_change
bloomberg_df['yearly_change'] = bloomberg_yearly_change
bloomberg_df['country/region'] = bloomberg_country_region
bloomberg_df['industry'] = bloomberg_industry
bloomberg_df['birthplace'] = birthplace_texts

# bloomberg_df.to_csv('/Users/bryceking/Desktop/billionaire_project/billionaire_data.csv', index=False)

bloomberg_df = bloomberg_df.astype(str)

old_data = pd.read_csv('/Users/bryceking/Desktop/billionaire_project/billionaire_data.csv')
old_data['date'] = pd.to_datetime(old_data['date'])
old_data = old_data.astype(str)

updated_df = pd.concat([old_data, bloomberg_df], ignore_index=True).drop_duplicates(subset=['date', 'rank'],
                                                                                    keep='first')
print(updated_df)

updated_df.to_csv('/Users/bryceking/Desktop/billionaire_project/billionaire_data.csv', index=False)

time.sleep(60)

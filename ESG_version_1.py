# Note! Before run projects so important create new csv file in function Create_csv
import requests
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd
import re
import openpyxl
import lxml
import re
from lxml import html
from datetime import datetime
import selenium
from airtable import Airtable
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import msvcrt, sys
# import datetime


chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--headless')
chromeOptions.add_argument('--no-sandbox')
chromeOptions.add_argument('--disable-dev-shm-usage')
chromeOptions.add_argument("--start-maximized")

TRIGGER = ['/about-us/careers?gh_jid=',
           #'/articles/', # Note bad trigger
           '/atomlearning/',
           '/babylon/jobs/',
           '/bighealth/',
           '/blog/job/',
           '/careers/',
           '/careers/jobs/',
           '/careers/position/',
           '/careers-listing?gh_jid=',
           '/details/',
           '/h/',
           '/huma/',
           '/j/',
           '/job/',
           '/job/details/',
           '/job_adverts/',
           '/JobDetail/',
           '/jobs/',
           '/joinzoe/',
           '/lead-dev-role',
           '/lyft/jobs/',
           '/news-post/',
           '/o/',
           '/opportunities/',
           '/p/',
           '/Posting/View/',
           '/recruitment/vacancies/',
           '/s/',
           '/samlabs/jobs/',
           '/site/ru/careers/jobs/',
           '/static/',
           '/stories/',
           '/uk/en/',
           '/ux/ats/',
           '/vacancies/',
           '/wp-content/uploads/',
           'sourse',
           'com/file/',
           '.paycomonline.net/v4/',
           '/uploads/',
           '/jobs/details/',
           '/apply/',
           '/Handlers/',
           '/#masthead',
           '69/files/',
           '/wp-content/uploads/',
           '/octoenergy/',
           'com/file/d/',
           'uk/jobs/#vacancies',
           '/3757/files/',
           'thebikeclub.peoplehr.net/Pages/JobBoard/',
           '?gh_jid=',
           '/s/files/',
           '/fRecruit__ApplyJob?v',
           '/jd-',
           '/Pages/JobBoard/',
           '/job?q=',
           '/job/live-in-carer',
           '/job_listings/',
           'googleapis.com/website-docs/',
           '//f.hubspotusercontent20',
           '.notion.site/',
           '/?gh_jid=',
           'jobs.lever.'
           ]

def get_data():
    # get data from AirTable
    urls = []
    base_key = 'apporlxSPon7AJAxv' # Insert the Base ID of your working base
    table_name = 'Companies' #Insert the name of the table in your working base
    api_key = 'keyHdp0DxoHCbnHHX' #Insert your API Key
    airtable = Airtable(base_key,table_name,  api_key)
    df = airtable.get_all(fields='Website')
    for i in df:
        for k, v in i['fields'].items():
            urls.append(v)
    return urls

def check_valid_links(links):
    has_jobs=[]

    for url in links:

        try:
            res = requests.get(url)
            html_page = res.content

            if ("job" in str(html_page).lower()) or ('career' in str(html_page).lower()):
                print('it good links - ', url)
                has_jobs.append(url)

            time.sleep(2.5)
        except:
            print(f"{url} broken")
            time.sleep(5)
    return has_jobs

def compare_data(all_urls): #has_jobs_urls
    df_1 = pd.DataFrame(all_urls, columns=['link'])
    links = df_1['link'].to_list()
    for link in links:
    # df_1.to_csv("has_jobs.csv", index=False)
    # binary = df_1['link'].apply(lambda x: x in has_jobs_urls)
    # binary.replace({False: 0, True: 1}, inplace=True)
    # df_2 = pd.DataFrame(binary)
        with open(f'has_jobs.csv', 'a', newline='', encoding='utf-8') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=','
                                    , quoting=csv.QUOTE_MINIMAL)
            datawriter.writerow([link])

def post_to_airtable():
    AIRTABLE_API_KEY = 'keyHdp0DxoHCbnHHX'
    post_url = 'https://api.airtable.com/v0/apporlxSPon7AJAxv/Has%20or%20not%20jobs' #https://api.airtable.com/v0/apporlxSPon7AJAxv/Has%20or%20not%20jobs
    # post_url = 'https://api.airtable.com/v0/apporlxSPon7AJAxv/Companies/recxcDBt17TWIO95N'
    post_headers = {
        'Authorization': f'Bearer {AIRTABLE_API_KEY}',
        'Content-Type': 'application/json'
    }

    df = pd.read_csv("has_jobs.csv")
    df = df.drop_duplicates(subset=["link"], keep = False)
    df_1 = df.copy()

    df_1 = df_1.drop_duplicates(subset=["link"], keep = False)




    with open(f'Trial_has_jobs.csv', 'w', newline='', encoding='utf-8') as csvfile:
        datawriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        datawriter.writerow(
            ['link'])

    data = df_1.to_csv('Trial_has_jobs.csv', index=False)

    filename = open('Trial_has_jobs.csv', encoding="utf8")

    file = csv.DictReader(filename)

    for col in file:
        links = col['link']

        data = {"fields":
            {
                "Links have jobs": links
            }}

        print(data)
        post_airtable_request = requests.post(post_url, headers=post_headers, json=data)
        print(post_airtable_request.status_code)

# The second function

def get_links():
    # Note! Links must add from AirTable
    # urls_has_jobs = []
    base_key = 'apporlxSPon7AJAxv'  # 'tblrc6HK1rZto83zN' # Insert the Base ID of your working base
    table_name = 'Has or not jobs'  # Insert the name of the table in your working base
    api_key = 'keyHdp0DxoHCbnHHX'  # Insert your API Key
    airtable = Airtable(base_key, table_name, api_key)
    df = airtable.get_all(fields='Vacancy URL page')
    # jobs_munually_remove_drop_for_minimize_dataset = pd.read_csv('Jobs_finding_manually.csv')
    # jobs_munually_remove_drop_for_minimize_dataset = jobs_munually_remove_drop_for_minimize_dataset.drop_duplicates(subset=['link'], keep = 'first')
    # jobs_munually_remove_drop_for_minimize_dataset.to_csv('Jobs_finding_manually.csv', index = False)
    for i in df:
        for k, v in i['fields'].items():
            with open('Jobs_finding_manually.csv', 'a', newline='', encoding='utf-8') as csvfile:
                datawriter = csv.writer(csvfile, delimiter=','
                                        , quoting=csv.QUOTE_MINIMAL)
                datawriter.writerow([v])

    jobs_munually = pd.read_csv('Jobs_finding_manually.csv')
    jobs_munually = jobs_munually.drop_duplicates(subset=['link'], keep = False)
    urls_has_jobs = jobs_munually['link'].tolist()
    print('urls_has_jobs',  urls_has_jobs)

    return urls_has_jobs

    # all_links_of_ESG = pd.read_csv('Links_of_valid_ESG.csv')
    # all_links_of_ESG = all_links_of_ESG['0'].values
    # return all_links_of_ESG

def get_link_Selenium(head_list):
    count = 0
    qw = []
    for link in head_list:
        count += 1
        print('Work with - ', link, 'counting - ', count)
        try:
            browser = webdriver.Chrome(
                executable_path=r'chromedriver.exe',
                chrome_options=chromeOptions)
            browser.get(link)
            browser.implicitly_wait(15)
            time.sleep(1)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight,)")
            time.sleep(1.5)
            urls = browser.find_elements_by_xpath("//a")
            print('Yes_url')
            for lin in urls:
                lin = lin.get_attribute('href')
                qw.append(lin)
        except Exception as ex:
            print(ex)
            print('--------')
            print('Bad link - ', link)
    return qw

def remove_none(links):
    res = list(filter(None, links))
    return res

def clean_links(link_list, TRIGGER):
    all_clean = []
    triggered_list = [link for trig in TRIGGER for link in link_list if trig in link]

    triggered_list = set(triggered_list)
    triggered_list = list(triggered_list)

    for l in triggered_list:
        if 'help-' in l or '/reviews' in l or '/stockists' in l or '-location' in l or 'collaborate' in l or 'news' in l or 'our-customers' in l or 'conditions' in l or 'conformity' in l or '/credits' in l or 'inclusion' in l or '.docx' in l or 'rewards' in l or 'download' in l or 'gifts' in l or 'impact' in l or 'our-' in l or '.png' in l or 'top-5' in l or 'join' in l or 'sleep' in l or 'delivery' in l or 'sign-up' in l or 'covid_19' in l or 'twitter' in l or 'facebook' in l or 'instagram' in l or 'google' in l or 'tiktok' in l:
            continue
        else:
            all_clean.append(l)

    return all_clean

def remove_links(links):
    s = []
    for l in links:
        if '/press' in l or 'get-in' in l or 'primary' in l or 'story' in l or 'returns' in l or 'events' in l or 'faq' in l or 'tokens' in l or 'privacy' in l or 'policy' in l or 'cookie' in l or 'policy' in l or '/awards' in l or '/dwow' in l or 'about' in l or 'mailto:?subject' in l or 'terms-of-use' in l or 'our-values' in l or '/search' in l or '/free-samples' in l or '/#content' in l or 'partners' in l or 'popup' in l or 'contact' in l or 'our-' in l:
            continue
        else:
            s.append(l)
    return s

def get_links_to_remove():
    df = pd.read_csv('Links_to_remove.csv')
    LINKS_TO_REMOVE = df['0'].values[:-2]
    return LINKS_TO_REMOVE

def remove_bad_links(links, LINKS_TO_REMOVE):
    good_s = [i for j in LINKS_TO_REMOVE for i in links if j in i]

    result = list(set(good_s) ^ set(links))
    return result

def parse_vacancy_SELENIUM(links_for_all):
    # main functions - response for get info about vacancy
    salary_s = re.compile(r'([£$])\d{2,}[.,]\d{1,}.-..\d{1,}[.,]\d{1,}')
    salary_s_ = re.compile(r'([£€$])\d{2,}[.,]\d{1,}')
    salary_s_1 = re.compile(r'\d{2,}..GBR')


    time_full = re.compile(r'full.time')
    time_part = re.compile(r'part.time')
    print('Length of links - ', len(links_for_all))
    count = 0
    print(links_for_all)
    for i in links_for_all:
        count +=1
        salary_ = ''
        time_jobs = ''
        vacancy_text = ''
        print('Work with - ', i, 'parse again - ', len(links_for_all) - count)
        try:
            browser = webdriver.Chrome(
                executable_path=r'chromedriver.exe',
                chrome_options=chromeOptions)
            browser.implicitly_wait(4)
            browser.get(i)
            time.sleep(1.5)

            try:
                button_cockie = browser.find_element(By.XPATH, "//*[text()[contains(., 'Access')]]")
                browser.execute_script("arguments[0].click();", button_cockie)
            except:
                pass
            try:
                button_cockie_ = browser.find_element(By.XPATH, "//*[text()[contains(., 'Dismiss')]]")
                browser.execute_script("arguments[0].click();", button_cockie_)
            except:
                pass

            browser.execute_script("window.scrollTo(0, 1000)")

            html = browser.page_source
            html = html.lower()

            data_now = datetime.now()
            data = data_now.strftime("%Y-%m-%d")
            try:
                vacancy_n = browser.title
            except Exception as ex:
                vacancy_n = 'None'

            try:
                vacancy_n_1 = browser.find_elements(By.XPATH, "//h1")[-1].text
                if len(vacancy_n_1) < 2:
                    vacancy_n_1 = browser.find_element(By.XPATH, "//h2").text

            except Exception as ex:
                vacancy_n_1 = 'None'

            # try:
            #     vacancy_d = [i.text.replace('\n', ' ') for i in browser.find_elements_by_xpath("//div")]  # //div/p
            #     vacancy = '.'.join(vacancy_d)
            # except Exception as ex:
            #     vacancy = ''
            try:
                vacancy_d = [i.text for i in browser.find_elements(By.XPATH, "//div/p")]
                vacancy = '.'.join(vacancy_d)
            except Exception as ex:
                vacancy = ''

            try:
                vacancy_d_1 = [i.text for i in browser.find_elements(By.XPATH,"//div//ul/li")]
                vacancy_ = '.'.join(vacancy_d_1)

            except Exception as ex:
                vacancy_ = ''

            vacancy_text = vacancy_text + vacancy + vacancy_

            try:
                salary1 = re.search(salary_s, html)
                if salary1:
                    salary_ = salary_ + ", " + salary1[0]
            except:
                pass

            try:
                salary2 = re.search(salary_s_, html)
                if salary2:
                    salary_ = salary_ + ", " + salary2[0]
            except:
                pass

            try:
                salary3 = re.search(salary_s_1, html)
                if salary3:
                    salary_ = salary_ + ", " + salary3[0]
            except:
                pass


            try:
                time_jobs_1 = re.search(time_full, html)
                time_jobs_2 = re.search(time_part, html)
                if time_jobs_1:
                    time_jobs = time_jobs + 'Full-time'

                elif time_jobs_2:
                    time_jobs = time_jobs + 'Part-time'
            except:
                pass

            with open(f'Valid_vacancy_v_1.csv', 'a', newline='', encoding='utf-8') as csvfile:
                datawriter = csv.writer(csvfile, delimiter=','
                                        , quoting=csv.QUOTE_MINIMAL)
                datawriter.writerow(
                    [data] + [i] + [vacancy_n] + [vacancy_n_1] + [vacancy] + [salary_] + [time_jobs])

        except Exception as e:
            print(e)
            print('-------------')
            print(i)
        time.sleep(0.5)

def get_vacancy_url_for_compare():
    urls = []
    base_key = 'apporlxSPon7AJAxv' # Insert the Base ID of your working base
    table_name = 'Trial_API' #Insert the name of the table in your working base
    api_key = 'keyHdp0DxoHCbnHHX' #Insert your API Key
    airtable = Airtable(base_key,table_name,  api_key)
    df = airtable.get_all(fields='company_url')
    for i in df:
        for k, v in i['fields'].items():
            urls.append(v)
    return urls




def post_to_airtable_final():
    AIRTABLE_API_KEY = 'keyHdp0DxoHCbnHHX'
    post_url = 'https://api.airtable.com/v0/apporlxSPon7AJAxv/Trial_API'
    post_headers = {
        'Authorization': f'Bearer {AIRTABLE_API_KEY}',
        'Content-Type': 'application/json'
    }
    df = pd.read_csv("Valid_vacancy_v_1.csv")
    df_1 = df.copy()
    vacancy_compare = get_vacancy_url_for_compare()

    df = df.drop_duplicates(subset=['company_url'], keep = False)

    for i in range(len(df['company_url'])):
        if df['company_url'][i] in vacancy_compare:
            df.drop([i], axis=0, inplace=True)

    # df - connect with AirTable
    # Data to AirTable
    dates = list(df['data'].unique())
    if len(dates) == 1:

        with open(f'Trial.csv', 'w', newline='', encoding='utf-8') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
            datawriter.writerow(
                ['data'] + ['company_url'] + ['vacancy_name_title'] + ['vacancy_name_jobs'] + [
                    'vacancy_description'] + ['Salary'] + ['Time_jobs'])

        # from df to csv for post in Airtable
        data = df.to_csv('Trial.csv', index=False)

        filename = open('Trial.csv', encoding="utf8")

        file = csv.DictReader(filename)

        for col in file:
            data = col['data']
            company_url = col['company_url']
            vacancy_name_title = col['vacancy_name_title']
            vacancy_name_jobs = col['vacancy_name_jobs']
            vacancy_description = col['vacancy_description']
            Salary = col['Salary']
            Time_jobs = col['Time_jobs']

            data = {"fields":
                {
                    "data": data,
                    "company_url": company_url,
                    "vacancy_name_title": vacancy_name_title,
                    "vacancy_name_jobs": vacancy_name_jobs,
                    "vacancy_description": vacancy_description,
                    "Salary": Salary,
                    "Time_jobs": Time_jobs
                }
            }

            print(data)

            post_airtable_request = requests.post(post_url, headers=post_headers, json=data)
            print(post_airtable_request.status_code)
    if len(dates) >= 2:
        df_1 = df[df['data'] == dates[-2]]
        df_2 = df[df['data'] == dates[-1]]
        df = df_2.merge(df_1, how='left', on='company_url', suffixes=('', '_drop'), indicator=True)
        df = df[df['_merge'] == 'left_only']
        df.drop([col for col in df.columns if 'drop' in col], axis=1, inplace=True)
        del (df['_merge'])

        # df_1 - renew csv
        # Data to renew csv
        # Remove all recordes past dates and remain only now date for minimize values of dataset
        dates = df_1['data'].unique()
        df_1 = df_1[df_1['data'] == dates[-1]]
        df_1.to_csv("Valid_vacancy_v_1.csv",index=False)

        # create csv for post in Airtable
        with open(f'Trial.csv', 'w', newline='', encoding='utf-8') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
            datawriter.writerow(
                ['data'] + ['company_url'] + ['vacancy_name_title'] + ['vacancy_name_jobs'] + ['vacancy_description']+['Salary']+['Time_jobs'])

        # from df to csv for post in Airtable
        data = df.to_csv('Trial.csv', index = False)

        filename = open('Trial.csv', encoding="utf8")

        file = csv.DictReader(filename)

        for col in file:
            data = col['data']
            company_url = col['company_url']
            vacancy_name_title = col['vacancy_name_title']
            vacancy_name_jobs = col['vacancy_name_jobs']
            vacancy_description = col['vacancy_description']
            Salary = col['Salary']
            Time_jobs = col['Time_jobs']


            data = {"fields":
                    {
                "data": data,
                "company_url": company_url,
                "vacancy_name_title": vacancy_name_title,
                "vacancy_name_jobs": vacancy_name_jobs,
                "vacancy_description":vacancy_description,
                "Salary":Salary,
                "Time_jobs":Time_jobs
                }
            }

            print(data)

            post_airtable_request = requests.post(post_url, headers = post_headers, json = data)
            print(post_airtable_request.status_code)


def main():
    while True:
        # time.sleep(1)
        # if datetime.datetime.now().time().strftime("%H:%M:%S") == '08:00:00':
        print('I begin work')
        # the first function
        df = get_data()
        df = df[50:65]
        has_jobs = check_valid_links(df)
        compare_data(has_jobs)
        post_to_airtable()
        print('Programm sleep for few minutes')
        time.sleep(10)
        # the second function
        while True:
                # if datetime.datetime.now().time().strftime("%H:%M:%S") == '17:00:00':
            all_links_of_ESG = get_links()
            if len(all_links_of_ESG) == 0:
                print('There are no jobs url finding manually')
                time.sleep(30)
            else:
                print('Yes finding manually jobs')
                urls_has_jobs = get_link_Selenium(all_links_of_ESG)
                # all_jobs_links_Selenium = get_link_Selenium(all_links_of_ESG)
                all_links_for_cleaning = remove_none(urls_has_jobs)
                jobs_links_ = clean_links(all_links_for_cleaning, TRIGGER)
                jobs_links_clear = remove_links(jobs_links_)
                LINKS_TO_REMOVE = get_links_to_remove()
                jobs_final = remove_bad_links(jobs_links_clear, LINKS_TO_REMOVE)
                print('All length of final links - ', len(jobs_final))
                parse_vacancy_SELENIUM(jobs_final)
                print('Begin post to Airtable')
                #the third function
                post_to_airtable_final()
                break

if __name__ == '__main__':
    main()

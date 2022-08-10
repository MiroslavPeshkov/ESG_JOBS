import pandas as pd
import requests
import time
from airtable import Airtable
import json
import csv

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




# def make_csv_jobs(has_jobs):
#     df_all = pd.DataFrame()
#     df_all["link"]=list(set(has_jobs))
#     df_all.to_csv("has_jobs.csv",index=False)

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

def main():
    df = get_data()
    df = df[:17]
    has_jobs = check_valid_links(df)
    compare_data(has_jobs)
    post_to_airtable()

if __name__ == '__main__':
    main()
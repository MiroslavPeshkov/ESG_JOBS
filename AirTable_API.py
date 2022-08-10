import csv
import requests
import pandas as pd
import json
from airtable import Airtable
# AIRTABLE_API_KEY = 'keyHdp0DxoHCbnHHX'
# post_url = 'https://api.airtable.com/v0/apporlxSPon7AJAxv/Trial_API'
# post_headers = {
#     'Authorization': f'Bearer {AIRTABLE_API_KEY}',
#     'Content-Type': 'application/json'
# }

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
print(post_to_airtable())



# def get_data():
#     # get data from AirTable
#     urls = []
#     base_key = 'apporlxSPon7AJAxv' # Insert the Base ID of your working base
#     table_name = 'Companies' #Insert the name of the table in your working base
#     api_key = 'keyHdp0DxoHCbnHHX' #Insert your API Key
#     airtable = Airtable(base_key,table_name,  api_key)
#     df = airtable.get_all(fields='Website')
#     for i in df:
#         for k, v in i['fields'].items():
#             urls.append(v)
#     return urls
# links = get_data()
# print(len(links))
# def post_to_airtable_final():
#     df = pd.read_csv("Valid_vacancy_v_1.csv")
#     df_1 = df.copy()
#     # df - connect with AirTable
#     # Data to AirTable
#     dates = df['data'].unique()
#     if len(dates) == 1:
#         with open(f'Trial.csv', 'w', newline='', encoding='utf-8') as csvfile:
#             datawriter = csv.writer(csvfile, delimiter=',',
#                                     quotechar='"', quoting=csv.QUOTE_MINIMAL)
#             datawriter.writerow(
#                 ['data'] + ['company_url'] + ['vacancy_name_title'] + ['vacancy_name_jobs'] + [
#                     'vacancy_description'] + ['Salary'] + ['Time_jobs'])
#
#         # from df to csv for post in Airtable
#         data = df.to_csv('Trial.csv', index=False)
#
#         filename = open('Trial.csv', encoding="utf8")
#
#         file = csv.DictReader(filename)
#
#         for col in file:
#             data = col['data']
#             company_url = col['company_url']
#             vacancy_name_title = col['vacancy_name_title']
#             vacancy_name_jobs = col['vacancy_name_jobs']
#             vacancy_description = col['vacancy_description']
#             Salary = col['Salary']
#             Time_jobs = col['Time_jobs']
#
#             data = {"fields":
#                 {
#                     "data": data,
#                     "company_url": company_url,
#                     "vacancy_name_title": vacancy_name_title,
#                     "vacancy_name_jobs": vacancy_name_jobs,
#                     "vacancy_description": vacancy_description,
#                     "Salary": Salary,
#                     "Time_jobs": Time_jobs
#                 }
#             }
#
#             print(data)
#
#             post_airtable_request = requests.post(post_url, headers=post_headers, json=data)
#             print(post_airtable_request.status_code)
#     else:
#
#         df_1 = df[df['data'] == dates[-2]]
#         df_2 = df[df['data'] == dates[-1]]
#         df = df_2.merge(df_1, how='left', on='company_url', suffixes=('', '_drop'), indicator=True)
#         df = df[df['_merge'] == 'left_only']
#         df.drop([col for col in df.columns if 'drop' in col], axis=1, inplace=True)
#         del (df['_merge'])
#
#         # df_1 - renew csv
#         # Data to renew csv
#         dates = df_1['data'].unique()
#         df_1 = df_1[df_1['data'] == dates[-1]]
#         df_1.to_csv("Valid_vacancy_v_1.csv",index=False)
#
#         # create csv for post in Airtable
#         with open(f'Trial.csv', 'w', newline='', encoding='utf-8') as csvfile:
#             datawriter = csv.writer(csvfile, delimiter=',',
#                                     quotechar='"', quoting=csv.QUOTE_MINIMAL)
#             datawriter.writerow(
#                 ['data'] + ['company_url'] + ['vacancy_name_title'] + ['vacancy_name_jobs'] + ['vacancy_description']+['Salary']+['Time_jobs'])
#
#         # from df to csv for post in Airtable
#         data = df.to_csv('Trial.csv', index = False)
#
#         filename = open('Trial.csv', encoding="utf8")
#
#         file = csv.DictReader(filename)
#
#         for col in file:
#             data = col['data']
#             company_url = col['company_url']
#             vacancy_name_title = col['vacancy_name_title']
#             vacancy_name_jobs = col['vacancy_name_jobs']
#             vacancy_description = col['vacancy_description']
#             Salary = col['Salary']
#             Time_jobs = col['Time_jobs']
#
#
#             data = {"fields":
#                     {
#                 "data": data,
#                 "company_url": company_url,
#                 "vacancy_name_title": vacancy_name_title,
#                 "vacancy_name_jobs": vacancy_name_jobs,
#                 "vacancy_description":vacancy_description,
#                 "Salary":Salary,
#                 "Time_jobs":Time_jobs
#                 }
#             }
#
#             print(data)
#
#             post_airtable_request = requests.post(post_url, headers = post_headers, json = data)
#             print(post_airtable_request.status_code)
# print(post_to_airtable_final())
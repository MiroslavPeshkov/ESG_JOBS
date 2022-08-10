import pandas as pd

pd.set_option('display.max_column', None)
pd.set_option('display.max_rows', None)
from airtable import Airtable

# def get_vacancy_url_for_compare():
df1 = pd.read_csv("Valid_vacancy_v_1.csv")
# df_1 = df.copy()
urls = []
base_key = 'apporlxSPon7AJAxv'  # Insert the Base ID of your working base
table_name = 'Trial_API'  # Insert the name of the table in your working base
api_key = 'keyHdp0DxoHCbnHHX'  # Insert your API Key
airtable = Airtable(base_key, table_name, api_key)
df = airtable.get_all(fields='company_url')
for i in df:
    for k, v in i['fields'].items():
        urls.append(v)

df1 = df1.drop_duplicates(subset=['company_url'], keep=False)

for i in range(len(df1['company_url'])):
    if df1['company_url'][i] in urls:
        df1.drop([i], axis=0, inplace=True)
print(df1)


# for vacancy in urls:
#     # try:
#
#         sd = df1['company_url'].str.contains(vacancy.strip(), regex=False)
#         # print(sd)
#         # if True in list(sd):
#         index = list(sd).index(True)
#         # print(index)
#         # print('sd')
#         df1.drop([index], axis=0, inplace=True)
#     # except:
#     #     pass
# print(df1)


# df = pd.read_csv("Valid_vacancy_v_1.csv")
# dates = list(df['data'].unique())
# print(type(dates))

# df = pd.read_csv("Valid_vacancy_v_1.csv")
# df_1 = df.copy()
# print(len(df))
# df = df.drop_duplicates(subset=['company_url'], keep = False)
# print(df)


# df = pd.read_csv("Valid_vacancy_v_1.csv")
# df_1 = df.copy()
# df = df_1.merge(df_1, how='left', on='company_url', suffixes=('', '_drop'), indicator=True)
# df = df[df['_merge'] == 'left_only']
# df.drop([col for col in df.columns if 'drop' in col], axis=1, inplace=True)
# del (df['_merge'])

# df = pd.DataFrame(columns = ['UR'])
# df['UR'] = ['10', '10']
# df['cou'] = [111, 222]
#
# df_ = pd.DataFrame(columns = ['UR'])
# df_['UR'] = ['11', '11']
# df_['cou'] = [333, 444]
#
# df1 = df_.merge(df, how='left', on='UR', suffixes=('', '_drop'), indicator=True)
# df1 = df1[df1['_merge'] == 'left_only']
# df1.drop([col for col in df1.columns if 'drop' in col], axis=1, inplace=True)
# del (df1['_merge'])
# print(df1)

def main():
    while True:
        # time.sleep(1)
        # if datetime.datetime.now().time().strftime("%H:%M:%S") == '08:00:00':
        print('I begin work')
        # the first function
        df = get_data()
        has_jobs = check_valid_links(df)
        compare_data(has_jobs)
        post_to_airtable()
        print('Programm sleep for few minutes')
        time.sleep(100)
        # the second function
        if datetime.now().time().strftime("%H:%M:%S") == '20:00:00':
            while True:
                all_links_of_ESG = get_links()
                if len(all_links_of_ESG) == 0:
                    print('There are no jobs url finding manually')
                    time.sleep(100)
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
                    # the third function
                    post_to_airtable_final()
                    break

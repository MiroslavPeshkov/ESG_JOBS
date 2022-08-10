import csv

with open(f'Valid_vacancy_v_1.csv', 'w', newline='', encoding='utf-8') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow(
        ['data'] + ['company_url'] + ['vacancy_name_title'] + ['vacancy_name_jobs'] + ['vacancy_description']+['Salary']+['Time_jobs'])

with open(f'has_jobs.csv', 'w', newline='', encoding='utf-8') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow(['link'])

with open(f'Jobs_finding_manually.csv', 'w', newline='', encoding='utf-8') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow(
        ['link'])



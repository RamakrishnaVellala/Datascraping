from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as Bs
import json

service_obj = Service('/home/ramakrishna/Downloads/chromedriver_linux64/chromedriver')
driver = webdriver.Chrome(service=service_obj)
driver.get('https://www.indeed.com/browsejobs/')
driver.maximize_window()
# set implicit wait time
driver.implicitly_wait(4)
driver.find_element(By.XPATH, "//a[normalize-space()='Computer/internet']").click()
job_titles = driver.find_elements(By.XPATH, "//a[@title]")
job_categories = []
for job in job_titles:
    job_categories.append(('+'.join(job.text.split())).strip('+jobs'))
job_urls = []
for i in job_categories:
    url = 'https://www.indeed.com/jobs?q={}'.format(i)
    job_urls.append(url)

# driver.get(job_urls[1])
# driver.implicitly_wait(4)
# total_jobs = driver.find_elements(By.ID, 'searchCountPages')
# jobs_count_str = ''
# for i in total_jobs:
#     jobs_count_str = i.text
#
# # count of jobs in particular category
# jobs_count = jobs_count_str.split()[3]
# jobs_count=int(float(jobs_count))
# print(jobs_count)
for i in range(0, 100, 10):
    url = job_urls[1] + '&start=' + str(i)
    driver.get(url)
    jobs_data = driver.find_elements(By.CLASS_NAME, 'result')
    for job in jobs_data:
        result_html = job.get_attribute('innerHTML')
        soup = Bs(result_html, "html.parser")

        try:
            job_title = soup.find('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0').text.replace('\n', '')
        except:
            job_title = None

        try:
            location = soup.find('div', class_='companyLocation').text.replace('\n', '')
        except:
            location = None

        try:
            company = soup.find('span', class_='companyName').text.replace('\n', '')
        except:
            company = None
        try:
            category = soup.find('div', class_='attribute_snippet').text.replace('\n', '')
        except:
            category = None
        try:
            Id = soup.find('a', class_='jcs-JobTitle').get('id')
        except:
            Id = None
        job_dict = dict()
        job_dict['Title'] = job_title
        job_dict['Location'] = location
        job_dict['Company'] = company
        job_dict['Category'] = category
        job_dict['Job_Id'] = Id

        f = open('output.json', 'w')
        f.write(json.dumps(job_dict))
        f.close()

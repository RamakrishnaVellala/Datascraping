# importing required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as Bs
import json

# chrome webdriver initialization
service_obj = Service('/home/ramakrishna/Downloads/chromedriver_linux64/chromedriver')
driver = webdriver.Chrome(service=service_obj)
# getting required website
driver.get('https://www.indeed.com/browsejobs/')
# maximizing window
driver.maximize_window()
# set implicit wait time
driver.implicitly_wait(4)
# click and get of required category
driver.find_element(By.XPATH, "//a[normalize-space()='Computer/internet']").click()
# Getting all job title categories
job_titles = driver.find_elements(By.XPATH, "//a[@title]")
job_categories = []
for job in job_titles:
    job_categories.append(('+'.join(job.text.split())).strip('+jobs'))
# Getting all urls based on job categories to scrap
job_urls = []
for i in job_categories:
    url = 'https://www.indeed.com/jobs?q={}'.format(i)
    job_urls.append(url)

# Based on all job urls,getting 30 jobs for each category
jobs_list = []
for j in range(len(job_urls)):
    for i in range(0, 30, 10):
        url = job_urls[j] + '&start=' + str(i)
        driver.get(url)
        jobs_data = driver.find_elements(By.CLASS_NAME, 'result')

        for job in jobs_data:
            result_html = job.get_attribute('innerHTML')
            soup = Bs(result_html, "html.parser")
            job_title = soup.find('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0').text.replace('\n', '')
            location = soup.find('div', class_='companyLocation').text.replace(' ', '')
            try:
                company = soup.find('span', class_='companyName').text.replace(' ', '')
            except:
                company = None

            category = job_categories[j]
            Id = soup.find('a', class_='jcs-JobTitle').get('id')

            job_dict = {'Title': job_title, 'Location': location, 'Company': company, 'Category': category,
                        'Job_Id': Id}
            jobs_list.append(job_dict)

# creating  json file  and writing scraped data to json file
f = open('jobs.json', 'w')
f.write(json.dumps(jobs_list))
f.close()
# Quitting the browser
driver.quit()

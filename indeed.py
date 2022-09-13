from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

service_obj = Service('/home/ramakrishna/Downloads/chromedriver_linux64/chromedriver')
driver = webdriver.Chrome(service=service_obj)
driver.get('https://www.indeed.com/browsejobs/')
driver.maximize_window()

driver.find_element(By.XPATH, "//a[normalize-space()='Computer/internet']").click()
job_titles = driver.find_elements(By.XPATH, "//a[@title]")
job_categories = []
for job in job_titles:
    job_categories.append(('+'.join(job.text.split())).strip('+jobs'))
job_urls = []
for i in job_categories:
    url = 'https://www.indeed.com/jobs?q={}'.format(i)
    job_urls.append(url)


df = pd.DataFrame(columns=["Title","Location","Company","Category","Id"])
url=job_urls[1]+'&start=10'
print(url)
driver.get(url)
jobs_data=driver.find_elements(By.CLASS_NAME,'result')
for job in jobs_data:
    result_html=job.get_attribute('innerHTML')
    soup = bs(result_html, "html.parser")
    try:
        job_title=soup.find('a',class_='jcs-JobTitle').text.replace('\n','')
    except:
        job_title=None

    try:
        location=soup.find('div',class_='companyLocation').text.replace('\n','')
    except:
        location=None

    try:
        company=soup.find('span',class_='companyName').text.replace('\n','')
    except:
        company=None
    try:
        category=soup.find('div',class_='attribute_snippet').text.replace('\n','')
    except:
        category=None
    # try:
    #     id=soup.find('a',class_='jcs-JobTitle')['id']


    print(job_title,location,company,category)





# title = soup.find("span",title_="jcs-JobTitle css-jspxzf eu4oa1w0").text.replace("\n","").strip()
# print(title)
# # driver.implicitly_wait(5)
#
# job_titles = driver.find_elements(By.XPATH, "//span[@title]")
# company = driver.find_elements(By.XPATH, "//a[@class='turnstileLink companyOverviewLink']")
# location = driver.find_elements(By.XPATH, "//div[@class='companyLocation']")

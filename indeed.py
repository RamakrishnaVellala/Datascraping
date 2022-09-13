from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

service_obj = Service('/home/ramakrishna/Downloads/chromedriver_linux64/chromedriver')
driver = webdriver.Chrome(service=service_obj)
driver.get('https://www.indeed.com/browsejobs/')
driver.maximize_window()

driver.find_element(By.XPATH, "//a[normalize-space()='Computer/internet']").click()
time.sleep(10)
job_titles = driver.find_elements(By.XPATH, "//a[@title]")
job_categories=[]
for job in job_titles:
    job_categories.append('-'.join(job.text.split()))
job_urls=[]
for i in job_categories:
    url='https://www.indeed.com/q-{}.html'.format(i)
    job_urls.append(url)


 # driver.implicitly_wait(5)
#
# job_titles = driver.find_elements(By.XPATH, "//span[@title]")
# company = driver.find_elements(By.XPATH, "//a[@class='turnstileLink companyOverviewLink']")
# location = driver.find_elements(By.XPATH, "//div[@class='companyLocation']")










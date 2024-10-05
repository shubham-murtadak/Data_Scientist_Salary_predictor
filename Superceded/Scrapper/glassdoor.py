from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

PATH = 'D:\personal\Personal Projects\salary_predictor\chromedriver\chromedriver.exe'


l=list()
o={}

target_url = "https://www.glassdoor.co.in/Job/pune-india-data-scientist-jobs-SRCH_IL.0,10_IC2856202_KO11,25.htm"

driver=webdriver.Chrome(PATH)

driver.get(target_url)

driver.maximize_window()
time.sleep(2)

resp = driver.page_source
driver.close()

soup=BeautifulSoup(resp,'html.parser')

allJobsContainer = soup.find("ul",{"class":"JobsList_jobsList__lqjTr"})

allJobs = allJobsContainer.find_all("li")

for job in allJobs:
    try:
        o["name-of-company"]=job.find("div",{"class":"EmployerProfile_profileContainer__VjVBX"}).text
    except:
        o["name-of-company"]=None

    try:
        o["name-of-job"]=job.find("a",{"class":"JobCard_jobTitle___7I6y"}).text
    except:
        o["name-of-job"]=None


    try:
        o["location"]=job.find("div",{"class":"JobCard_location__rCz3x"}).text
    except:
        o["location"]=None


    try:
        o["salary"]=job.find("div",{"class":"JobCard_salaryEstimate__arV5J"}).text
    except:
        o["salary"]=None

    l.append(o)

    o={}

print(l)

df = pd.DataFrame(l)
df.to_excel(r'Data\\jobs2.xlsx', index=False)






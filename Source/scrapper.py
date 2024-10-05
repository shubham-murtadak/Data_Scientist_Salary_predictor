import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

load_dotenv()

PROJECT_HOME_PATH=os.getenv('PROJECT_HOME_PATH')
WEBDRIVER_PATH=os.getenv('WEBDRIVER_PATH')


print(PROJECT_HOME_PATH)
print(WEBDRIVER_PATH)
#Reading Config File

with open(os.path.join(PROJECT_HOME_PATH,'Config','Config.json')) as file:
    r_config=json.load(file)
    print("json loaded")
    file.close


def initialize_driver(path):
    """
    * method: initialize_driver
    * description: Initializes the Selenium WebDriver for Chrome.
    * return: webdriver.Chrome instance to interact with the browser.
    *
    * who             when            version  change (include bug# if apply)
    * ----------      -----------     -------  ------------------------------
    * Shubham M       05-OCT-2024     1.0      initial creation
    *
    * Parameters
    *   path (str): The path to the ChromeDriver executable.
    """
    print(path)
     # Create a Service object
    service = Service(path)

    driver = webdriver.Chrome(service=service)
    time.sleep(5)

    return driver

def load_jobs_page(driver, url):
    """
    * method: load_jobs_page
    * description: Loads the job listings page in the browser using the provided URL.
    * return: None
    *
    * who             when            version  change (include bug# if apply)
    * ----------      -----------     -------  ------------------------------
    * Shubham M       05-OCT-2024     1.0      initial creation
    *
    * Parameters
    *   driver (webdriver.Chrome): The Selenium WebDriver instance.
    *   url (str): The URL of the job listings page.
    """
    driver.get(url)

def click_show_more_jobs(driver):
    """
    * method: click_show_more_jobs
    * description: Clicks the "Show more jobs" button repeatedly until no more jobs are available.
    * return: None
    *
    * who             when            version  change (include bug# if apply)
    * ----------      -----------     -------  ------------------------------
    * Shubham M       05-OCT-2024     1.0      initial creation
    *
    * Parameters
    *   driver (webdriver.Chrome): The Selenium WebDriver instance.
    """

    while True:
        try:
            show_more_button = driver.find_element(by=By.XPATH, value='//button[@data-test="load-more"]')
            show_more_button.click()
            time.sleep(2)  # Wait for new jobs to load
        except NoSuchElementException:
            print("No more jobs to load.")
            break

def extract_job_details(driver):
    """
    * method: extract_job_details
    * description: Extracts job details from the current job listing page and returns them as a dictionary.
    * return: dict
    *
    * who             when            version  change (include bug# if apply)
    * ----------      -----------     -------  ------------------------------
    * Shubham M       05-OCT-2024     1.0      initial creation
    *
    * Parameters
    *   driver (webdriver.Chrome): The Selenium WebDriver instance.
    """

    job_details = {}


    try:
        job_details['Job Title'] = driver.find_element(by=By.XPATH, 
            value='//h1[@class="heading_Heading__BqX5J heading_Level1__soLZs"]').text
    except:
        job_details['Job Title'] = 'N/A'

    try:
        job_details['Employer'] = driver.find_element(by=By.XPATH, 
            value='//h4[contains(@class, "heading_Subhead__Ip1aW")]').text
    except:
        job_details['Employer'] = 'N/A'


    # Extract job details with error handling
    try:
        job_details['Rating'] = driver.find_element(by=By.XPATH, 
            value='/html/body/div[3]/div[1]/div[4]/div[2]/div[2]/div/div[1]/header/div[1]/a/div[2]/div[2]').text
    except:
        job_details['Rating'] = 'N/A'

    try:
        job_details['Description'] = driver.find_element(by=By.XPATH, 
            value='/html/body/div[3]/div[1]/div[4]/div[2]/div[2]/div/div[1]/section/div[2]/div[1]').text
    except:
        job_details['Description'] = 'N/A'

        
    try:
        job_details['Salary Estimate'] = driver.find_element(by=By.XPATH, 
            value='/html/body/div[3]/div[1]/div[4]/div[2]/div[2]/div/div[1]/section/section[1]/div/div[1]/div[1]/div[2]').text
    except:
        job_details['Salary Estimate'] = 'N/A'

    try:
        job_details['Location'] = driver.find_element(by=By.XPATH, 
            value='//div[@class="JobDetails_location__mSg5h" and @data-test="location"]').text
    except:
        job_details['Location'] = 'N/A'

    try:
        job_details['Company Overview'] = driver.find_element(by=By.XPATH, 
            value='/html/body/div[3]/div[1]/div[4]/div[2]/div[2]/div/div[1]/section/section[2]').text
    except:
        job_details['Company Overview'] = 'N/A'

    return job_details


def loadAllJobs(driver):
    """
    * method: loadAllJobs
    * description: Loads all job listings by clicking the "Show more jobs" button until no more jobs are available.
    * return: None
    *
    * who             when            version  change (include bug# if apply)
    * ----------      -----------     -------  ------------------------------
    * Shubham M       05-OCT-2024     1.0      initial creation
    *
    * Parameters
    *   driver (webdriver.Chrome): The Selenium WebDriver instance.
    """

    while(True):
        try:
            more = driver.find_element(by = By.CSS_SELECTOR, value = '.JobsList_buttonWrapper__ticwb > button:nth-child(1)')
            more.click()
            time.sleep(2)
            try:
                close = driver.find_element(by = By.CSS_SELECTOR, value = '.CloseButton')
                close.click()
                print('popup closed')
            except:
                print('No poopy popup...loading more jobs...')
        except:
            print('All jobs loaded')
            break


def main(rarget_url):
    
    driver_name=r_config['driver_name']
    PATH =os.path.join(PROJECT_HOME_PATH, 'chromedriver', driver_name)


    driver = initialize_driver(PATH)

    # time.sleep(10)

    # # Call the function to LOAD ALL jobs and  close the sign-in popup
    load_jobs_page(driver, target_url)

    try:
        loadAllJobs(driver)
    except Exception as e:
        # close_sign_in_popup(driver)
        # click_show_more_jobs(driver)
        print(e)


    job_listings = driver.find_elements(by=By.CLASS_NAME, value='JobCard_jobCardContainer___hKKI')
    job_data = []

    for job in job_listings:
        job.click()
        time.sleep(3)  # Wait for the job details to load
        try:
            job_details = extract_job_details(driver)
            job_data.append(job_details)
        except Exception as e:
            print(e)

        # Print the results for the current job post
        for key, value in job_details.items():
            print(f"{key}: {value}")
        print()

    # Create a DataFrame from the job data
    job_df = pd.DataFrame(job_data)

    # Export the DataFrame to an Excel file
    export_data_file_name=r_config['data_scrap_file_name']
    export_data_file_name_with_path=os.path.join(PROJECT_HOME_PATH,'Data',export_data_file_name)
    job_df.to_excel(export_data_file_name_with_path, index=False)

    # Close the WebDriver
    driver.quit()

if __name__ == "__main__":
    target_url = "https://www.glassdoor.co.in/Job/pune-india-data-scientist-jobs-SRCH_IL.0,10_IC2856202_KO11,25.htm"
    main(target_url)

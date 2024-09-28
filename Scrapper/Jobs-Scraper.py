#Automation Package
from playwright.sync_api import sync_playwright
import time
#Scraping Package
from selectolax.parser import HTMLParser
from bs4 import BeautifulSoup as bs
#Preprosscsing Package
import pandas as pd
import numpy as np
import re
from datetime import datetime as dt
import json
import os
##################################################
#Create Automating Page
with sync_playwright() as playwright:
    #Launch the browser and go to the page
    browser = playwright.chromium.launch(headless=False , slow_mo=200)
    page = browser.new_page()
    page.set_viewport_size({'width':1920,'height':1080})
    page.goto('https://www.glassdoor.com/Job',wait_until='domcontentloaded')



    #Adjust Resarch Job and Filters
    page.get_by_placeholder('Find your perfect job').type('Data Analyst',delay=200) #Write Data Analyst in job research
    page.locator('div input[value="Data Analyst"]').press('Enter') #Press Enter
    page.wait_for_timeout(2000) # Wait for several milliseconds
    page.locator("div[class*='job-search']  input[placeholder='Location']").type('Remote',delay=200)#Write Remote in location research
    page.locator("div[class*='job-search']  input[placeholder='Location']").press('ArrowDown+Enter')#Press Arrow Down Enter to choose  the first result
    page.wait_for_timeout(1000) # Wait for several milliseconds
    page.locator("div > [data-test='DATEPOSTED']:visible").click() #Click in Dateposted to make it visible
    # If Last 3 Days not found
    try:
        page.locator("button[value='3']").click() # Choose the Last 3 Days
    except:
        page.locator("button[value='1']").click() # Choose the last 3 Days
    page.wait_for_timeout(1000) # # Wait for several milliseconds
    page.locator("div [data-test='sort-by-header']:visible").click()# Make sort header visible
    page.wait_for_timeout(1000) # # Wait for several milliseconds
    page.get_by_role('button',name='Recent').click() # Sort by recent res

    page.wait_for_selector("li[class*='react-job-listing']") # Wait for selector
    
    def iter_each_job(Jobs):
        '''
        This function take all 30 jobs in the page and loop
        for each one of them to extract more info about each job
        like job_description , salray , about the company and more
        finaly store the result in the genrator to loop on it in another time
        '''
        for i in range(len(Jobs)):
            page.locator("li[class*='react-job-listing']").all()[i].click()
            page.wait_for_timeout(2000)# Wait for several milliseconds
            if page.locator("div[class*='actionBar'] > button").count() == 1:# Check if there is register page
                page.locator("div[class*='actionBar'] > button").click() # Close the register page
                page.wait_for_selector("article[class*='scrollable active']") # Wait untile the selector load
                page.get_by_text('Show More').first.click() # Show job description
                page.wait_for_timeout(200)# Wait for several milliseconds
                yield page.inner_html('body') 
            else:    
                page.wait_for_selector("article[class*='scrollable active']") # Wait untile the selector load
                page.get_by_text('Show More').first.click() # Show job description
                page.wait_for_timeout(200)# Wait for several milliseconds
                yield page.inner_html('body')


        # html_bodies = iter_each_job(page.locator("li[class*='react-job-listing']").all())        

    def scrape_data(body):
        '''
        This function works to store the data in json list of dict
        first loop over all right continer jobs in the page to
        just get the job title , company title ,location and date posted
        from the main body of html
        '''
        
        html = HTMLParser(body) # parse the the body of html page to dealing with it using css selector
        df=[{
            'Job_Title':title.text(),#Extract the Job Title
            'Company_Title':re.sub(r'[^A-z]',' ',company.text()).strip(), # Substract all anything except string than get the string
            'Location':location.text(),#Extract the Location of the company
            'Date_Posted':dt.strftime(dt.now() - pd.Timedelta(value= int(re.findall(r'\d',date_posted.text())[0]), unit='D'),'%Y-%m-%d') if re.findall(r'[A-z]',date_posted.text())[0].lower() != 'h' else dt.strftime(dt.now(),'%Y-%m-%d'),
            } # if the date posted is 24h i'll return the today's day in date formating else the date posted like 5d i'll substract 5 days from today's date and return it in formating date 
            for title ,company ,location, date_posted in zip(html.css("div [class*='job-title']"),html.css("div [id*=job-employer]"),html.css("div[class*='location mt-xxsm']"),html.css("div [data-test='job-age']"))] 
        
        # Loop for each job to get the job describtion and more info about the company
        df_desc = []
        for job in iter_each_job(page.locator("li[class*='react-job-listing']").all()):
                html_desc = HTMLParser(job) # parse the first html of the job desc
                if len(html_desc.css("#CompanyContainer")) != 0 : # Check if there is a comany over view container
                    company_over_view = {company_overview_matric.text().lower():company_overview_value.text().lower() for company_overview_matric,company_overview_value  in zip(html_desc.css("#CompanyContainer div span[class*='1taruhi']"),html_desc.css("#CompanyContainer div span[class*='i9gxme']"))} 
                    df_desc.append(# First, I have to iterate on the key and the value for each container I did a dictionary because there are some jobs that have incomplete information and without order
                        {'Size' : company_over_view['size'] if 'size' in company_over_view.keys() else np.NaN,
                        'Founded' : int(company_over_view['founded']) if 'founded' in company_over_view.keys() else np.NaN,
                        'Type' : company_over_view['type'] if 'type' in company_over_view.keys() else np.NaN,
                        'Industry' : company_over_view['industry'] if 'industry' in company_over_view.keys() else np.NaN,
                        'Sector' : company_over_view['sector'] if 'sector' in company_over_view.keys() else np.NaN,
                        'Revenue' : company_over_view['revenue'] if 'revenue' in company_over_view.keys() else np.NaN,
                        'Average_Salary':page.locator("div [class*='7rpujz']").inner_text() if len(html_desc.css("div [class*='salaryTab']")) != 0 else np.NaN,
                        'Estimate_Salary':page.locator("div [class*='1d4p0fd']").first.inner_text() +" to "+ page.locator("div [class*='1d4p0fd']").last.inner_text() if len(html_desc.css("div [class*='salaryTab']")) != 0 else np.NaN,
                        'Job_Description': page.locator("div [class*='jobDescriptionContent']").inner_text() if len(html_desc.css("div [class*='jobDescriptionContent']"))  != 0 else np.NaN}
                        )
                else: # If the comany over view container fill all the data with null values
                      df_desc.append(
                        {'Size' : np.NaN,
                        'Founded' : np.NaN,
                        'Type' : np.NaN,
                        'Industry' : np.NaN,
                        'Sector' : np.NaN,
                        'Revenue' : np.NaN,
                        'Average_Salary':page.locator("div [class*='7rpujz']").inner_text() if len(html_desc.css("div [class*='salaryTab']")) != 0 else np.NaN,
                        'Estimate_Salary':page.locator("div [class*='1d4p0fd']").first.inner_text() +" to "+ page.locator("div [class*='1d4p0fd']").last.inner_text() if len(html_desc.css("div [class*='salaryTab']")) != 0 else np.NaN,
                        'Job_Description': page.locator("div [class*='jobDescriptionContent']").inner_text() if len(html_desc.css("div [class*='jobDescriptionContent']"))  != 0 else np.NaN}
                        )

        # #Update the dictionaries with each other
        for z , zz in zip(df , df_desc):
            z.update(zz)
        Data_Frame = df
        

        return Data_Frame
    

    def Create_newfile(your_filename):
        # Check If the file is exists if not create new one
        '''
        This function take your file name to create a new file if
        the file dosen't exists and if not remove the exists file
        which's contains the old data and create new one that 
        will has the new data in it
        '''
        if os.path.exists(your_filename) :
                os.remove(your_filename)
                open(your_filename,'w').close()
        else:
            open(your_filename,'w').close()

    Create_newfile('Glassdoor.json')
        

    # Write data into json file
    def write_json(data , filename):
        '''
        This function takes the data that you wanna write
        and the file name and it'll automatice write the data
        and close the file 
        '''
        with open(filename , 'w') as file:    
            json.dump(data , file,indent=4)
            file.close()

    def append_new_data(new_data , filename):
        '''
        this function takes the new data that you wanna append to
        the json file and the file name and
        '''
        # first read the json file to load the old data
        with open(filename,'r') as file:
            old_data = json.load(file)
            for data in new_data:
                old_data.append(data) # loop through list of dict to append each dict 
            all_data = old_data
            write_json(all_data,filename)# now update the json file by writing all data 
            file.close()
    

    num_pages = int(page.locator("div[class='paginationFooter']").inner_text().split(' ')[-1]) # Extract the number of pages 
    counter = 0
    while counter < num_pages: # Loop for number of pages 
        
        if page.locator("div[class*='actionBar'] > button").count() == 1: # Check if there is register page
            page.locator("div[class*='actionBar'] > button").click() # Close the register page

        # else: # there is no register page
        data = scrape_data(page.inner_html('body')) # Extract the body of the page

        # Store The Data in json file
        #Using try and except to avoid the error which will happen because the empty file
        try:
            append_new_data(data , 'Glassdoor.json')#Second, the function will append the new data, and the first time the file will be empty of course I got an error so I should use the write function first to write the data
        except:    
            write_json(data , 'Glassdoor.json')#Third for only the first time I gonna use the right function directly but then I gonna use it from the append function to write the new data  

        if counter > 0 and page.locator('button[disabled]').count() == 1:# th break the last page
            break

        page.get_by_role('button',name='Next').click() # Move to the next page
        page.wait_for_selector("li[class*='react-job-listing']") # Wait untile the selector load
        
        page.wait_for_timeout(3000) # # Wait for several milliseconds    
           
        counter += 1

    page.close()
    


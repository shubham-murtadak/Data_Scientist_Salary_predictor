# -*- coding: utf-8 -*-

import glassdoor_scraper as gs 
import pandas as pd 

path = "D:/personal/salary_predictor/chromedriver/chromedriver.exe"

df = gs.get_jobs('data scientist',2, False, path, 2)

df.to_csv('Data\glassdoor_jobs1.csv', index = False)
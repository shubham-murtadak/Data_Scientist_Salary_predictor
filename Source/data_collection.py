# -*- coding: utf-8 -*-

import glassdoor_scraper as gs 
import pandas as pd 

path = "C:/Users/Ken/Documents/ds_salary_proj/chromedriver"

df = gs.get_jobs('data scientist',1000, False, path, 15)

df.to_csv('Data\glassdoor_jobs1.csv', index = False)
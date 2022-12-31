#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 00:56:27 2022

@author: paulmason
"""
#Program that will look at jobs posted within the last 24 hours with a specified description
#and location on simplyhired.com. 
#Go to the website https://www.simplyhired.com/ and enter the job description and location
#then can use that link to run this program. 

#import beautifulsoup and requests
from bs4 import BeautifulSoup
import requests
import time
import csv


def find_jobs():
    #Create a csv file to add information to
    csv_file = open('pythonJobData.csv', 'w')
    #Create csv writer object and add headers
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Company Name', 'Job Title', 'Date Posted', 'Minimum Salary', 'Link'])
    #Get the html of the simplyhired website
    html_text = requests.get('https://www.simplyhired.com/search?q=python&l=san+jose&job=6d-HRsPAaG0lxYF8tvXW-qkLUpTHRWBqHvZvn5C0kPWD6XIWntu_RQ').text
    
    #Create soup variable
    soup = BeautifulSoup(html_text, 'lxml')
    
    #Get the list of jobs
    jobs = soup.find('ul', class_ = 'jobs')
    
    #Loop through all jobs
    for job in jobs:
        #Use try with pass to ensure that no missing data breaks program
        try:
            #Get when the job was posted
            posted = job.find('time').text
            #Filter jobs so that only jobs that were posted recently enough to have data for when they were posted show up
            if posted != '':   
                #Get job title
                job_name = job.find('h3', class_ = 'jobposting-title')
                #Get the post's link as more info
                more_info = job_name.a['href']
                #Have to add the beginning of the url to more_info
                more_info = 'https://www.simplyhired.com' + more_info
                job_name = job_name.a.text
                #Get the name of the company posting the job
                company = job.find('span', class_ = 'JobPosting-labelWithIcon jobposting-company').text
                #Find the minimum salary the position offers
                salary = job.find('div', class_ = 'jobposting-salary SerpJob-salary').text
                #To get the min salary split by $ then by ' ' and that should be that
                min_sal = salary.split('$')[1]
                min_sal = salary.split(' ')[0]

                #Use fstring to print out info neatly
                print('Company Name: %s' % company)
                print('Job Title: %s' % job_name)
                print('Date Posted: %s' % posted)
                print('Link for More Information: %s' % more_info)
                print('Minimum Salary: %s' % min_sal)
                print()
                #Add info to the csv document
                csv_writer.writerow([company, job_name, posted, min_sal, more_info])
            
        except Exception as e:
            pass
        
    csv_file.close()
        
        
#Run program every 15 minutes or so        
if __name__ == '__main__':
    while True:
        find_jobs()
        min_wait = 10
        print('Waiting %d minutes...' % min_wait)
        time.sleep(min_wait * 60)
        
    


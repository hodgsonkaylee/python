# Go to desired working directory
import os
os.getcwd()
os.chdir('/Users/admin/Desktop/Work and School')
os.getcwd()

# Import the page source using the URL
import urllib.request
urldr = 'https://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html'
pagedr = urllib.request.urlopen(urldr).read()

# Import BeautifulSoup to use for scraping
from bs4 import BeautifulSoup

soupdr = BeautifulSoup(pagedr, 'lxml')
# soupelect

# Find the first and last names and strip to text
name = soupdr.find_all('tr')
# Don't include first one (0) - just the titles
name[1].contents[7].text # last name
name[1].contents[9].text # first name

# Locate url that connects to each statement
# first get all urls in html code
urls = soupdr.find_all(href=True)
urls[25].contents
urlls = []
for i in range(0,(len(urls)-1)):  
    # only pull url if it's for the last statement
    # and make sure the url is correct - some are different
    if 'Last' in urls[i].text:
        if urls[i]['href'][:7] == 'dr_info':
            urlls.append('https://www.tdcj.state.tx.us/death_row/'+urls[i]['href'])
        else:
            urlls.append('https://www.tdcj.state.tx.us'+urls[i]['href'])
    else:
        continue

# Go to each individual webpage and scrape data
statement = []
for i in range(0,553):
    # go to the url and put in BeautifulSoup
    pagedr1 = urllib.request.urlopen(urlls[i]).read()
    soupdr1 = BeautifulSoup(pagedr1, 'lxml')
    k = len(soupdr1.find_all('p')) - 1
    statement.append('') # In case no last statement, add blank row
    # look for the title "Last Statement" and pull the information after that
    for j in range(0,k):
        if 'Last Statement' in soupdr1.find_all('p')[j].text and len(soupdr1.find_all('p')) > j:
            statement[i] = soupdr1.find_all('p')[j+1].text
            pass
        else:
            continue
    
# Clean the statements - if they declined to make one or it says there are none, make those cells blank
statementclean = []
for i in range(0,553):
    if 'declined to make' in statement[i] or 'None' in statement[i]:
        statementclean.append('')
    else:
        statementclean.append(statement[i])
        
# Write data into a csv file
f = open('lastwords.csv', 'w')
f.write('lastname' + ',' + 'firstname' + 'laststatement' + '\n')
for i in range(0, 553):
    ln = name[i+1].contents[7].text
    fn = name[i+1].contents[9].text
    s = statementclean[i]
    f.write('"' + ln + '"' + ',' + '"' + fn + '"' + ',' + '"' + s + '"' + '\n')
f.close()




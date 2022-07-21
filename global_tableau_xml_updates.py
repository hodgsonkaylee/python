# CHANGE TABLEAU DASHBOARD DATA SOURCE FOR MULTIPLE ENTITIES
# WRITTEN BY: KAYLEE HODGSON

# import relevant packages

import pandas
from bs4 import BeautifulSoup

####################################################
#### INPUT TEMPLATE FILE INFORMATION ####

old_Folder = "Path_to_old_file"
old_Dashboard = "old_dashboard.twb"
old_Title = "Old Dashboard Title"
old_hyper_File = "old_hyper_file"
old_csv_File = "old_csv_file"

#### INPUT NEW FILE INFORMATION FOR EACH ENTITY ####

new_Info = pandas.read_csv('new_Info.csv')
# add the version number for the new workbook
version_NO = "2.0"
#################################################### 

for i in range(len(new_Info['Title'])):

    # Import old dashboard file as xml

    xml = old_Folder + '\\' + old_Dashboard
    soup = BeautifulSoup(open(xml, encoding='utf-8'), "lxml-xml")

    # Assign new information for the ith entity

    new_Folder = new_Info['File Path'][i]
    new_Dashboard = new_Info['Title'][i] + ' Dashboard ' + version_NO + '.twb'
    new_Title = new_Info['Title'][i]
    new_hyper_File = new_Info['Title'] + ' Tableau'
    new_csv_File = new_Info['Title'] + ' Worksheet'

    # Switch out .hyper file (Tableau extract file)

    for tag in soup.find_all("named-connection",{'name':'hyper.17awp6c06icswa1e45qhw1hj8ei4'}):
        tag['caption'] = new_hyper_File
        tag['dbname'] = new_Folder + '/' + new_hyper_File + '.hyper'
    
    for tag in soup.find_all("connection",{'dbname':old_Folder + old_hyper_File + '.hyper'}):
        tag['dbname'] = new_Folder + new_hyper_File + '.hyper'

    for tag in soup.find_all("datasource",{'name':'federated.1ht8ueb1xxzjf711no7zk0le9pdn'}):
        tag['caption'] = new_hyper_File

    # Switch out .csv file
    
    for tag in soup.find_all("named-connection",{'name':'textscan.00lhyjd1rom88y1a244ib0w0mudu'}):
        tag['caption'] = new_csv_File
        tag['directory'] = new_Folder
        tag['filename'] = new_csv_File + '.csv'
    
    for tag in soup.find_all("connection",{'directory':old_Folder}):
        tag['directory'] = new_Folder
        tag['filename'] = new_csv_File + '.csv'
    
    for tag in soup.find_all("relation",{'connection':'textscan.00lhyjd1rom88y1a244ib0w0mudu'}):
        tag['name'] = new_csv_File + '.csv'
        tag['table'] = new_csv_File + '#csv]'  
    
    for tag in soup.find_all("_.fcp.ObjectModelEncapsulateLegacy.false...relation",{'connection':'textscan.00lhyjd1rom88y1a244ib0w0mudu'}):
        tag['name'] = new_csv_File + '.csv'
        tag['table'] = new_csv_File + '#csv]'
    
    for tag in soup.find_all("_.fcp.ObjectModelEncapsulateLegacy.true...relation",{'connection':'textscan.00lhyjd1rom88y1a244ib0w0mudu'}):
        tag['name'] = new_csv_File + '.csv'
        tag['table'] = new_csv_File + '#csv]'

    for tag in soup.find_all("datasource",{'name':'federated.17w3cui0l03zr11cfauy916hu0rf'}):
        tag['caption'] = new_csv_File
        
    for i in range(0,5):  
        textreplace = soup.find(text=new_csv_File + '.csv]')
        textreplace.replace_with(new_csv_File + '.csv]')

    # Edit the dashboard title  
   
    textreplace = soup.find(text=old_Title)
    textreplace.replace_with(new_Title)

    # Clear the parameter selections

    for tag in soup.find_all("column",{'caption':'Parameter 1'}):
        tag['value'] = '""'
    
    for tag in soup.find_all("column",{'caption':'Parameter 2'}):
        tag['value'] = '""'

    # Export the New File

    with open(new_Folder + "\\" + new_Dashboard, "w", encoding='utf-16') as file:
        file.write(str(soup))
    

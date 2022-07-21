# python
This repository contains projects that demonstrate some of my python coding skills. The projects in each folder are described below.

**global_tableau_xml_updates.py**

Because no one to my knowledge had done this before, I published a blog post about this coding solution on Tableau's community page: https://community.tableau.com/s/question/0D54T00000C6kAMSAZ/how-to-programmatically-replace-dashboard-data-sources-using-beautifulsoup

This is a generic version of some code I wrote to change the data source in a Tableau Dashboard for multiple entities. I needed to create the same dashboard for multiple entities and the dashboard was connected to multiple data sources, so the process of going into the Tableau workbook, switching out all data sources, then saving in a new folder was long and tedious. I reached out to Tableau to try to find a solution to this issue and, to my knowledge, no one has been able to solve this. 

I wrote this code that uses the BeautifulSoup package to edit the XML code that backs the Tableau dashboard, change the data source for each specified entity, then save the new dashboard in a new folder location. The code is also used to change the dashboard title and reset any parameters. Before this discovery, we had been manually switching out the data for each new dashboard using the “Replace Data” option. We spent too much time correcting all of the features that broke each time we imported new data. For example, the color palette would sometimes change and we would have to reassign all of the aliases. This programmatic solution keeps the new data in the same format, with the same class categorization, automatically adjusts the filters for the new data, and keeps the same formatting in the dashboards, like color and placement choices.

**global_R_code_updates.py**

This is a generic version of some code I wrote to change specific lines of code in R scripts for multiple entities. Standard scripts are used for each entity and saved in separate folders. Because there are entity-specific adjustments added to each R script, there are slight deviations from the standard template for each entity. I needed to find a way to edit standard code across the multiple files without removing the entity-specific adjustments. We additionally need to track these updates on git, and the process of doing that for each individual file was long and tedious.

I wrote this code that replaces specified lines in the R script with the updated code for each entity. I track the success of each update to make sure that the updated file was edited and saved correctly. Finally, this code updates the edited script in our GitLab repository for each entity. This saves hours of work and reduces the chances of human error everytime code updates need to be implemented.

**web_scraping.py**

This code uses the BeautifulSoup package to scrape the last statements of executed inmates in Texas. It saves their first and last name from the main page, then goes into the link for each of their statements and scrapes that information as well. This data was scraped to build a word cloud, to visualize the most prevalent words used in these last statements. This project was completed for a data visualization class.

# web-scraping-academic

This GitHub Repository hosts my ongoing project that scrapes a Google Scholar user profile and does analysis on the article names, scholar info, co-authors info. The web scraping part is written with ```BeautifulSoup```. The project aims to help me with grad school research and hones my coding skills in general.

Current progress: completed the function to scrape author info, co-author info, and all the articles written by the author.

Last updated: 10/25/22

User Profile Scraping:
#### Reference: 
Medium Article I found about scraping google scholar [here](https://proxiesapi-com.medium.com/scraping-google-scholar-with-python-and-beautifulsoup-850cbdfedbcf)

Stackoverflow starter code [here](https://stackoverflow.com/questions/67146312/web-scraping-google-scholar-author-profiles)

Reference Medium Article from SerpeAPI [here](https://python.plainenglish.io/scrape-google-scholar-with-python-fc6898419305#daf8)

In general, use **selenium** if you need to interact with the webpage

You can also use scholarly package (mine didn't work because I keep getting fake user agent error)

Pagination solution: using 'cstart' and 'pagesize' to work with Show More option

Down the line: incoroporating object oriented programming - author could be a class

To get the text of current element and not its children: use contents
- example : <div> yes <a>no</a></div>
    - soup.find("div").contents[0]


### Hurdle for Getting CoAuthors
1. Write getting co_authors function
    - currently not able to find the co-authors ul tag .... bc the testing profile did not have co-authors section....
2. was only able to scrape the top 20 co-authors before we have to click "View All" and maybe use selenium
    - found alternative way by scraping a new view option offered by google scholar. Reference [here](https://datascience-enthusiast.com/R/google_scholar_R.html)
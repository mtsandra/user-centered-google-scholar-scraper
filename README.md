## Google Scholar Webscraper for Scholar & Institution Relationship Analysis

This webscraper allows you to explore the articles and affiliated institutions for up to second connection of coauthors using a seed scholar. By inputting the seed scholar's Google Scholar user ID, it will write an Excel file with the scholar's basic info, available articles, coauthor information, as well as a concatenated list of their coauthors' coauthors and a concatenated list of all the articles by their coauthors and second connection coauthors. Webscraping is done with BeautifulSoup.

You can use this tool to do graduate school research or industry job research if you have someone whose work you are particularly interested in. Simply get their Google Scholar user id and see where their coauthors and second connection coauthors are working at. I was able to narrow down my target schools this way and find professor doing similar research in a particular school.

Here I will go through an example of how you can use this tool.

## Usage Instruction

1. Clone this repository and create a virtual environment by typing into your command line:

    ```
    python3 -m venv gscholar-venv
    ```

2. Install all required packages by typing into your command line:

    ```
    python3 -m pip install -r requirements.txt
    ```

3. Get the user ID of the seed scholar that you want to base the research on. The user ID is in their Google Scholar profile, right after "user=" and before "&". Here we use the example of Julius Smith, the OG professor doing audio signal processing work at Stanford. 

    <img src="/assets/img/user_id.png" width="100%">

4. Open your terminal, change directory to where your repository lives, and run the command:

    ```
    python3 analysis.py
    ```

    Your command line will prompt you to input the user ID. Copy over the user ID from previous step.

    <img src="/assets/img/command_line_input.png" width="100%">

5. If the script runs successfully, you will see the seed scholar's coauthors' user IDs being printed in the command line. When it finishes, it will print ```File successfully saved for [Scholar Name] at the path [path/to/your/repository]!```

6. Now in your current working directory, there will be an Excel file with the seed scholar's name as the file name.

    <img src="/assets/img/output_example.png" width="100%">

### Next Steps
Currently this project just completed its first development stage, meaning that there are still processes that could be enhanced. Below are some current open items, you are welcome to open an issue and make suggestions if I missed out on anything.

1. The institution and position scraping is not perfect. The current version assumes that affiliation is always listed as "Position, Institution", which is not how all the users input their affiliation. This could get quite complicated because not all users input both their position and institution.
2. In some discipline such as chemistry, the article names have special characters that are hard to scrape and show up as blank when scraped.
3. Some CITED BY values are crossed out, which currently shows up as No Citation Available in the Excel file.
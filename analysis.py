import pandas as pd
import author_class as ac
import user_profile_scraping as ups
import os

#USER_ID = 'qc6CJjYAAAAJ'

def write_to_excel(author,coauthors_instance_dict):
    writer = pd.ExcelWriter(f'{author.name}.xlsx')
    author_info = pd.DataFrame.from_dict(ups.getting_author_info(author.user_id))
    author_info.to_excel(writer, sheet_name='Author Info', index = False)
    author.coauthors.to_excel(writer, sheet_name = "Coauthor Info", index = False)
    author.articles.to_excel(writer, sheet_name = "Author's Articles", index = False)
    second_conn_coauthors = author.merge_coauthors_of_coauthors(coauthors_instance_dict )
    second_conn_coauthors.to_excel(writer, sheet_name = "Second Connection Co-Authors Info", index = False)
    scc_group = second_conn_coauthors.groupby(by=["co_author_affiliated_institutions"]).count().sort_values(by='user_id', ascending=False)[[ "user_id"]]
    scc_group.columns = [ "count"]
    scc_group.to_excel(writer, sheet_name="Second Connection Co-Authors Institution Count", index = True)
    second_conn_articles = author.merge_articles_of_coauthors(coauthors_instance_dict)
    second_conn_articles.to_excel(writer, sheet_name = "Second Connection Co-Authors Articles", index=False)
    
    
    
    writer.save()
    pass


def main():
    USER_ID = input("What's the user ID of the seed Google Scholar?\n")
    author = ac.Author(USER_ID)
    coauthors_instance_dict = author.create_coauthors_instance_dict()
    write_to_excel(author, coauthors_instance_dict)
    print(f"File successfully saved for {author.name} at the path {os.getcwd()}!")
    pass

if __name__ == "__main__":
    main()
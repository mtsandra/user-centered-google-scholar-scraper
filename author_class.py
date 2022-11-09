import user_profile_scraping as ups
import pandas as pd


pd.set_option('display.max_colwidth', None)


class Author:
    def __init__(self, user_id) -> None:
        self.user_id = user_id
        self.name = ups.getting_author_info(user_id)["scholar_name"]
        self.position = ups.getting_author_info(user_id)["position"]
        self.affiliated_institution = ups.getting_author_info(user_id)["affiliated_institution"]
        self.tags = ups.getting_author_info(user_id)["tags"]
        self.coauthors = ups.getting_coauthors(user_id)
        self.articles = ups.getting_authors_articles(user_id)
        pass
    
    ## create a dictionary that contains each coauthor author instance
    def create_coauthors_instance_dict(self):
        coauthors_instance_dict = {}
        #self.coauthors[["co_author_positions","co_author_affiliated_institutions"]] = ""
        for idx, id in enumerate(self.coauthors["co_author_ids"]):
            coauthors_instance_dict["coauthor_%s" %idx] = Author(id)
            #self.coauthors.loc[idx,[ "co_author_positions", "co_author_affiliated_institutions"]] = [coauthors_instance_dict["coauthor_%s" %idx].position, coauthors_instance_dict["coauthor_%s" %idx].affiliated_institution]
            print(id)
        return coauthors_instance_dict
    
    ## put all coauthor's coauthors into a dataframe of unique authors
    def merge_coauthors_of_coauthors(self, coauthors_instance_dict ):
        merged_coauthor_df = self.coauthors
        for coauthor in coauthors_instance_dict.values():
            merged_coauthor_df = pd.concat([merged_coauthor_df, coauthor.coauthors], ignore_index=True)
        
        return merged_coauthor_df.drop_duplicates(subset=['co_author_name', 'co_author_ids', 'co_author_positions', 'co_author_affiliated_institutions'])
    
    ## put all coauthor's articles into one dataframe of unique articles
    def merge_articles_of_coauthors(self, coauthors_instance_dict):
        merged_articles = self.articles
        for coauthor in coauthors_instance_dict.values():
            merged_articles = pd.concat([merged_articles, coauthor.articles], ignore_index=True)
            #print(coauthor)
        return merged_articles.drop_duplicates(subset=['paper_titles', 'author_names', 'journals', 'published_years', 'citation_times', 'paper_urls']) 
    
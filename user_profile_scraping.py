from bs4 import BeautifulSoup as bs
import requests, lxml, os, re, pandas as pd

def institution_cleaning(institution):
    
    institution = str.upper(institution)
    institution = re.sub(r"[^\w\s]", " ", institution)
    
    return institution.strip()

# getting the position and institution from the affiliation field of an author profile
def position_institution(tag):
    if tag.find("a") != None:
        if tag.contents[0] == tag.find("a"):
            position = "No Position Available"
        else:
            position = tag.contents[0].replace(",", "").strip()
        institution = tag.find("a").string
    else:
        pos_ins = str(tag.get_text()).rsplit(",", 1)
        if len(pos_ins) > 1:
            position = pos_ins[0]
            institution = pos_ins[1]
        else:
            position = "No Position Available"
            institution = pos_ins[0]
        
    return position.strip(), institution_cleaning(institution)


def getting_author_info(user_id):
  headers = {
      'User-agent':
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
  }

  proxies = {
    'http': os.getenv('HTTP_PROXY')
  }
  params={
    'user':user_id,
    'hl':'en', 
    'cstart':0, 
    'pagesize':'100'
    }
  
  html = requests.get('https://scholar.google.com/citations', headers=headers, proxies=proxies, params=params).text
  soup = bs(html, 'lxml')
  profile = soup.find("div", id="gsc_prf_w")
  user_info = dict()
  user_info["user_id"] = user_id
  user_info["scholar_name"] = profile.find("div", id="gsc_prf_in").string
  # getting string for both institution and po
  pos_ins = profile.find("div", {"class":"gsc_prf_il"})
  user_info["position"], user_info["affiliated_institution"] = position_institution(pos_ins)

  tags = profile.find_all("a", {"class": "gsc_prf_inta gs_ibl"})
  user_info["tags"] = [tag.string for tag in tags]
  return user_info
  
  
 
def getting_coauthors(user_id):
    headers = {
      'User-agent':
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }

    proxies = {
        'http': os.getenv('HTTP_PROXY')
    }
    params={
        'user':user_id,
        'hl':'en'
        }

    
    
    html = requests.get('https://scholar.google.com/citations?view_op=list_colleagues', headers=headers, proxies=proxies, params=params).text
   
    soup = bs(html, 'lxml')
    co_authors = soup.find_all("div", {"class": "gs_ai_t gs_ai_pss"}) 
    all_ca_names, all_ca_user_ids, all_ca_positions, all_ca_institutions = ([] for _ in range(4))

    for co_author in co_authors:

        all_ca_names += [co_author.find("a").string]
        all_ca_user_ids += [re.search(r'(?<=user=)[^&#]*', co_author.find("a")["href"]).group(0)]
        pos_ins = co_author.find("div", {"class": "gs_ai_aff"})
        all_ca_positions += [position_institution(pos_ins)[0]]
        all_ca_institutions += [position_institution(pos_ins)[1]]



    df = pd.DataFrame({
            "user_id": user_id,
            "co_author_name": all_ca_names,
            "co_author_ids": all_ca_user_ids,
            "co_author_positions": all_ca_positions,
            "co_author_affiliated_institutions": all_ca_institutions
        })
    return df


def getting_authors_articles(user_id):
  headers = {
      'User-agent':
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
  }

  proxies = {
    'http': os.getenv('HTTP_PROXY')
  }
  params={
    'user':user_id,
    'hl':'en', 
    'cstart':0, 
    'pagesize':'100'
    }
  
  all_titles, all_urls, all_authors, all_years, all_journals, all_cite_times = ( [] for _ in range(6))

  while True:
    html = requests.get('https://scholar.google.com/citations', headers=headers, proxies=proxies, params=params).text

    soup = bs(html, 'lxml')
    table = soup.find("tbody", id="gsc_a_b")
    rows = table.find_all("tr", {"class": 'gsc_a_tr'})
    for row in rows:
      
      a_tag = row.find("a", {"class": "gsc_a_at"})
      ## extract paper titles
      all_titles += [a_tag.string]
      
      ## extract paper url
      if "href" in a_tag.attrs:
        all_urls += ["https://scholar.google.com"+a_tag["href"]]
      else: all_urls += ["No Link Available"]
      ## extract author names
      authors = row.select("td > a + div")
      if authors:
        all_authors += [author.string for author in authors]
      else: all_authors += ["No Author Available"]
      ## extract published year
      years = row.select("td > a + div + div span")
      if years:
        all_years += [str(years[0].string).replace(", ", "")]
      else: all_years += ["No Year Available"]

      ## extract journal name
      journals = row.select("td > a + div + div")
      
      ## extract citation times
      freq = row.find("a", {"class": "gsc_a_ac gs_ibl"})
      if freq == None:
        all_cite_times += ["No Citation Available"]
      else:
        all_cite_times += [row.find("a", {"class": "gsc_a_ac gs_ibl"}).string]
      
      ## check if there are multiple pages, if so, go to the next page
      if journals:
        all_journals += [re.sub(r', [0-9]{4}$', '', journal.get_text()) if journal.get_text() != ''
                         else 'No Journal Available'
                         for journal in journals]
      else: all_journals += ["No Journal Available"]
      
    if len(rows)<int(params['pagesize']):
      break
    else:
      params['cstart'] += 100
  #print(f'user_id: {len(user_id)}, all_titles: {len(all_titles)}, author_names {len(all_authors)}, journals {len(all_journals)}, published_years {len(all_years)}, citation_times {len(all_cite_times)}, paper_urls {len(all_urls)}')  
  df = pd.DataFrame({"user_id":user_id,"paper_titles": all_titles, "author_names": all_authors, 
                     "journals": all_journals, "published_years":all_years,
                     "citation_times": all_cite_times, "paper_urls": all_urls})
  
  return df






from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import string
from summary.summarizer_textrank_model import summarizer_textrank_get

def query_to_url(query, search_type, size):
  """convert query to usuable url

  Args:
      query (str): search query by user
      search_type (str): Search type (choice)
      size (int): number of items to query

  Returns:
      (str) the url for search
  """  

  # remove bad string & convert txt -> search keys
  query = query.translate(str.maketrans('', '', string.punctuation))
  query = query.replace(" ", "+")

  # get the correct mapping  
  mapping = {"All Fields": "",
             "Title": "title",
             "Abstract": "abstract"}
  
  search_type = mapping[search_type]

  #return the url
  return f"https://arxiv.org/search/?query={query}&searchtype={search_type}&abstracts=show&order=&size={size}"

def get_arxiv(query, search_type, size):
  """Get content from arxiv
  Args:
      query (str): search query by user
      search_type (str): Search type (choice)
      size (int): number of items to query

  Returns:
      output (list): list of abtracts, titles, etc.
      txt(str): the combined text
  """  

  # get fake agent to avoid blocking
  ua = UserAgent()

  # get_url
  url = query_to_url(query, search_type, size)

  # get response and start scraping
  response = requests.get(url, headers = {'User-Agent': ua.random})
  content = BeautifulSoup(response.content, 'html.parser')  

  # scrape contents
  urls = [val.find_all("a")[0]["href"] for val in content.find_all('p', class_="list-title is-inline-block")]
  titles = [val.text.replace("\n", "").strip() for val in content.find_all('p', class_ = "title is-5 mathjax")]
  abstracts = [summarizer_textrank_get(val.text[9:-16], 50)["sentences"] for val in content.find_all('span', class_ = "abstract-full has-text-grey-dark mathjax")]

  # store results to return
  output = []
  for i in range(int(len(urls))):
    output.append([urls[i], titles[i], abstracts[i]])

  # get the text for word cloud function
  txt = ""

  for val in output:
    txt += val[1] + " " + val[2] + " "

  return output, txt



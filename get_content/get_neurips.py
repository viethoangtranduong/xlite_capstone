from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import string
from summary.summarizer_textrank_model import summarizer_textrank_get

def get_url(query):
  """convert query to correct url

  Args:
      query (str): search term

  Returns:
      url (str): correct url
  """  
  url = "https://proceedings.neurips.cc/papers/search?q="
  query = query.translate(str.maketrans('', '', string.punctuation))
  query = query.replace(" ", "+")

  return url + query


def get_neurips(query, max_results = 10, summarize_option = False):
  """get the results from neurips page

  Args:
      query (str): search term
      max_results (int, optional): number of results. Defaults to 10.
      summarize_option (bool, optional): sumamrize or not. Defaults to False.

  Returns:
      output: list of information scraped
      text: combined text of all content
  """  

  # using fake agent to avoid being blocked
  ua = UserAgent()
  
  # get the correct url
  url = get_url(query)

  # scrape the content
  page = requests.get(url, headers = {'User-Agent': ua.random})
  soup = BeautifulSoup(page.text, 'html.parser')

  # get the page
  results = soup.find_all("a")[3:-1]

  output = []
  text = ""

  # send more requests to get the content of the papers and summarize them
  for i in range(min(max_results, len(results))):
    item = results[i]

    # get all content
    new_title = item.text
    year = item["href"].split("/")[2]
    new_url = "https://proceedings.neurips.cc/" + item["href"]
    new_page = requests.get(new_url, headers = {'User-Agent': ua.random})
    new_soup = BeautifulSoup(new_page.text, "html.parser")

    abstract = new_soup.find_all("p")[-1].text
    if summarize_option:
        # summarize if needed
        abstract = summarizer_textrank_get(abstract, 50)["sentences"]
    
    text += new_title + " " + abstract + " "

    output.append([year, new_url, new_title, abstract])
  
  return output, text


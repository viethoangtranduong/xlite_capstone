from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import string

def name_to_url(query):
  """convert query to correct url

  Args:
      query (str): search term

  Returns:
      url (str): correct url
  """  
  query = query.translate(str.maketrans('', '', string.punctuation))
  query = query.replace(" ", "%20")
  search = 'https://medium.com/search?q=' + query

  return search      

def clap_convert(txt):
  """convert string of clap values on medium to actualy number

  Args:
      txt (str): claps values

  Returns:
      number on claps (int)
  """ 

  # Medium annotation 
  if txt[-1] == "K":
    output = int(float(txt[:-1]) * 1000)
    return output
  else:
    return int(txt)


def get_query(query):
  """get the results from Medium search

  Args:
      query ([type]): [description]

  Returns:
      output: list of information scraped
      text: combined text of all content
  """  
  # fake user to avoid blocks
  ua = UserAgent()
  
  # get url
  url = name_to_url(query)

  # scrape content
  response = requests.get(url, headers = {'User-Agent': ua.random})
  content = BeautifulSoup(response.content, 'html.parser')
  stories = content.find_all('a', class_ = 'link link--darken')
  claps = content.find_all('button', class_='button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents')

  # storing all the content we need
  output = []
  txt = ""
  for story, clap in zip(stories, claps):
    new_url = story['href'].split("?")[0]

    new_response = requests.get(new_url, headers = {'User-Agent': ua.random})
    new_content = BeautifulSoup(new_response.content, 'html.parser')

    section_titles = new_content.find_all("h1")
    section_titles = [item.text for item in section_titles]
    title = section_titles[0]
    
    content = new_content.find_all('p')
    content = [item.text for item in content]

    for item in section_titles:
      txt += item + " "

    for item in content:
      txt += item + " "

    num_clap = clap_convert(clap.text)
    output.append([num_clap, title, url, section_titles])
    
  # sorting the results to show the most clapped version
  output = sorted(output, key=lambda x: x[0], reverse=True)
  return output, txt
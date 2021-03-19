import pandas as pd
from ast import literal_eval
from datetime import datetime


def time_convert(txt):
  """conver string of time to time data

  Args:
      txt (str): string of time data

  Returns:
      datetime of the given string
  """  
  return datetime.strptime(txt, '%d/%m/%Y')

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

def select_medium(entry, start_date, end_date, num_result = 10):
  """ get the content from Medium files

  Args:
      entry (str): publisher
      start_date (date): start date from querying
      end_date (date): end date for querying
      num_result (int, optional): number of returns. Defaults to 10.

  Returns:
      [type]: [description]
  """  

  # get all data
  data = pd.read_csv("/home/viethoangtranduong/xlite_capstone/medium_data/" + entry)

  # convert the data back to its original type
  data.paragraphs = data.paragraphs.apply(literal_eval)
  data.section_titles = data.section_titles.apply(literal_eval)

  # convert Medium annotation to normal annotation
  data['datetime'] = data.date.apply(time_convert)
  data['num_claps'] = data.claps.apply(clap_convert)

  # filter
  cur_data = data[data.datetime.between(start_date, end_date, inclusive=True)]

  # get all the txt for wordcloud
  txt = ""

  for val in list(cur_data.title):
    txt += val + " "


  # getting the content of the most clapped posts
  cur_data = cur_data.sort_values(by=['num_claps'], ascending = False)[:num_result]
  cur_data.reset_index(inplace = True, drop = True)

  output = []
  for idx in range(len(cur_data)):
      url = cur_data.story_url[idx].split("?")[0]
      section_titles = cur_data.section_titles[idx]
      claps = cur_data.num_claps[idx]
      title = cur_data.title[idx]
      output.append([claps, title, url, section_titles])

  return output, txt

def get_medium(entry, start_date, end_date, num_result = 10):
    """convert medium name to currect file name

    Args:
        entry (str): publisher
        start_date (date): start date from querying
        end_date (date): end date for querying
        num_result (int, optional): number of returns. Defaults to 10.

    Returns:
        [type]: [description]
    """    
    files = ['httpsuxdesigncc.csv',
            'httpsmediumcomzora.csv',
            'httpsmediumcomheated.csv',
            'httpsmediumcomhumanparts.csv',
            'httpsmediumcomswlh.csv',
            'httpsentrepreneurshandbookco.csv',
            'httpsmediumcompersonalgrowth.csv',
            'httpsuxplanetorg.csv',
            'httpswritingcooperativecom.csv',
            'httpsmediumcomthemission.csv',
            'httpsgenmediumcom.csv',
            'httpstowardsdatasciencecom.csv']

    names = ['UX Collective',
            'Zora (A publication for Black women)',
            'Heated (Food & everything)',
            'Human Parts (humanity & perspectives)',
            'The Startup',
            "Entrepreneur's handbook",
            "Personal Growth",
            "UX Planet",
            "The Writing Cooperative (Writers)",
            "The Mission (learning & podcast)",
            'GEN (politics, power & culture)',
            'Towards Data Science (AI/ML/Data)']

    mapping = dict(zip(names, files))

    # get result using the select_medium function
    results, text = select_medium(mapping[entry], start_date, end_date, num_result)

    return results, text


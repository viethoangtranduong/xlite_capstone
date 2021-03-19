import string
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import nltk
nltk.download('punkt') # one time execution
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import numpy as np
import time

def most_frequent_viz(txt, name, num_result = 30):
  """get the most frequent words viz

  Args:
      txt (str): the string we try to plot
      name (str): name of the file
      num_result (int, optional): number of bars (number of most frequent words). Defaults to 30.

  Returns:
      file location (str)
  """  
  try:
    # prep text: lower, split by words, and remove punctuation
    txt = txt.translate(str.maketrans(' ', ' ', string.punctuation + "”“-_"))
    txt = txt.lower()
    word_list = word_tokenize(txt)

    # remove stopwords
    stop_words = set(stopwords.words('english'))
    cleaned = []
    for val in word_list:
      if val not in stop_words and len(val) > 1:
        cleaned.append(val)

    # get the most frequent words by using Counter: key: word, value: number of ocurrence
    word_freq = Counter(cleaned)

    x = word_freq.most_common(num_result)

    # plot
    plt.figure(figsize=(20,20))
    plt.bar(range(num_result), np.array(x).T[1].astype('int'))
    plt.xticks(range(num_result), np.array(x).T[0], rotation='vertical')
    plt.xlabel('Word')
    plt.ylabel('Count')
    plt.title('Most frequent words')

    # if pythonanywhere, use the following url
    # plt.savefig(f"/home/viethoangtranduong/xlite_capstone/static/image_output/{name}_most_frequent_viz.png", dpi=500) 
    
    # if not pythonanywhere
    plt.savefig(f"./static/image_output/{name}_most_frequent_viz.png", dpi=500)

    print("done mfw", f"./static/image_output/{name}_most_frequent_viz.png")

    return f"static/image_output/{name}_most_frequent_viz.png"
  except:
    return "ERROR"
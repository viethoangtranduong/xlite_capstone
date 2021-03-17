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
  try:
    stop_words = set(stopwords.words('english'))
    txt = txt.translate(str.maketrans(' ', ' ', string.punctuation + "”“-_"))
    txt = txt.lower()
    word_list = word_tokenize(txt)

    cleaned = []
    for val in word_list:
      if val not in stop_words and len(val) > 1:
        cleaned.append(val)

    word_freq = Counter(cleaned)

    x = word_freq.most_common(num_result)

    plt.figure(figsize=(20,20))
    plt.bar(range(num_result), np.array(x).T[1].astype('int'))
    plt.xticks(range(num_result), np.array(x).T[0], rotation='vertical')
    plt.xlabel('Word')
    plt.ylabel('Count')
    plt.title('Most frequent words')
    # plt.show()
    plt.savefig(f"/home/viethoangtranduong/xlite_capstone/static/image_output/{name}_most_frequent_viz.png", dpi=500)
    print("done mfw", f"./static/image_output/{name}_most_frequent_viz.png")

    return f"static/image_output/{name}_most_frequent_viz.png"
  except:
    return "ERROR"
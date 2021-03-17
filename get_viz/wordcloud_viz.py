from wordcloud import WordCloud, STOPWORDS
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def wordcloud_viz(txt, name):
  try:
    txt = txt.lower()
    mpl.rcParams['font.size']=12                #10
    mpl.rcParams['savefig.dpi']=100             #72
    mpl.rcParams['figure.subplot.bottom']=.1

    stopwords = set(STOPWORDS)

    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=200,
        max_font_size=40,
        random_state=42
        ).generate(txt)

    plt.figure(figsize=(20,20))
    plt.imshow(wordcloud)
    plt.axis('off')
    # plt.show()
    plt.savefig(f"/home/viethoangtranduong/xlite_capstone/static/image_output/{name}_wordcloud_viz.jpg", dpi=500)
    print("done wordcloud", f"./static/image_output/{name}_wordcloud_viz.jpg")
    return f"static/image_output/{name}_wordcloud_viz.jpg"
  except:
    return "ERROR"
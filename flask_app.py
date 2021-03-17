from flask import Flask, render_template, request
# import requests
from get_content.read_url import read_url
from get_content.get_summary import get_summary
from get_content.get_medium import get_medium
from datetime import datetime
from get_content.get_query import get_query
from get_content.get_arxiv import get_arxiv
from get_content.get_neurips import get_neurips

from get_viz.show_viz_choice import show_viz_choice
import time
import string

application = Flask(__name__, static_url_path='/static')

@application.route('/')
def student():
   # method = "The summarization method will be here"
   # summary = "Your summary output"
   # length = "Length of the summary"
   return render_template('index.html')

@application.route('/info_summarize', methods = ['POST', 'GET'])
def info_summarize():
   print("haha")
   if request.method == 'POST':
      print("haha")
      print(request.form)

      url = request.form['info_summarize_url']
      text = request.form['info_summarize_text']
      method = request.form['info_summarize_method']
      percentage = float(request.form["info_summarize_len"])

      if url:
         text_out = read_url(url)
         if text_out != "ERROR!":
            text = text_out

      if not url and not text:
         return render_template('info_summarize.html', method = method, summary = "", original_text = "Cannot read url or text. Try again!")

      output = get_summary(text, percentage=percentage, method=method)
      summary = output['sentences']
      method = output['method']
      original_text = text

      return render_template('info_summarize.html', method = method, summary = summary, original_text = original_text)

@application.route('/medium_summarize', methods = ['POST', 'GET'])
def medium_summarize():
   print("hoho")
   if request.method == 'POST':
      print("haha")
      print(request.form)

      publisher = request.form['medium_summarize_publisher']
      start_date = request.form['medium_summarize_time_start']
      end_date = request.form['medium_summarize_time_end']
      time_period = f"From {start_date} to {end_date}"

      start_date = datetime.strptime(start_date, "%Y-%m-%d")
      end_date = datetime.strptime(end_date, "%Y-%m-%d")

      if start_date > end_date:
         time_period = "Invalid time range. " + time_period
         output = []
         return render_template('medium_summarize.html', publisher = publisher, outputs = output, time_period = time_period, show_viz = False, name = "")

      output, text = get_medium(publisher, start_date, end_date)

      show_viz = request.form['medium_summarize_visualize']
      name = f"medium_{publisher.translate(str.maketrans('', '', string.punctuation))}_{time.strftime('%Y%m%d-%H%M%S')}"
      name = name.replace(" ", "")
      name = name.lower()


      show_viz, wc_name, mf_name = show_viz_choice(name, show_viz, text)

      return render_template('medium_summarize.html', publisher = publisher, outputs = output, time_period = time_period, show_viz = show_viz, wc_name = wc_name, mf_name = mf_name)

@application.route('/query_summarize', methods = ['POST', 'GET'])
def query_summarize():
   if request.method == 'POST':
      print("haha")
      print(request.form)

      query = request.form['query_summarize']

      results, text = get_query(query)

      length = len(results)

      show_viz = request.form['query_summarize_visualize']
      name = f"query_{query.translate(str.maketrans('', '', string.punctuation))}_{time.strftime('%Y%m%d-%H%M%S')}"
      name = name.replace(" ", "")
      name = name.lower()

      show_viz, wc_name, mf_name = show_viz_choice(name, show_viz, text)

      return render_template('query_summarize.html', outputs = results, query = query, length = length, show_viz = show_viz, wc_name = wc_name, mf_name = mf_name)

@application.route('/arxiv_summarize', methods = ['POST', 'GET'])
def arxiv_summarize():
   if request.method == 'POST':
      print("haha")
      print(request.form)

      query = request.form['query_arxiv']
      search_type = request.form["arxiv_searchtype"]
      size = request.form["arxiv_size"]

      results, text = get_arxiv(query, search_type, size)

      length = len(results)

      show_viz = request.form['arxiv_summarize_visualize']
      name = f"arxiv_{query.translate(str.maketrans('', '', string.punctuation))}_{time.strftime('%Y%m%d-%H%M%S')}"
      name = name.replace(" ", "")
      name = name.lower()

      show_viz, wc_name, mf_name = show_viz_choice(name, show_viz, text)

      return render_template('arxiv_summarize.html', outputs = results, query = query, length = length, show_viz = show_viz, wc_name = wc_name, mf_name = mf_name)

@application.route('/neurips_summarize', methods = ['POST', 'GET'])
def neurips_summarize():
   if request.method == 'POST':
      print("haha")
      print(request.form)

      query = request.form['query_neurips']
      summarize_option = request.form['neurips_summarize'] == "Yes - with TextRank!"
      size = int(request.form["neurips_size"])

      results, text = get_neurips(query, size, summarize_option)

      length = len(results)

      show_viz = request.form['neurips_summarize_visualize']
      name = f"neurips_{query.translate(str.maketrans('', '', string.punctuation))}_{time.strftime('%Y%m%d-%H%M%S')}"
      name = name.replace(" ", "")
      name = name.lower()

      show_viz, wc_name, mf_name = show_viz_choice(name, show_viz, text)

      return render_template('neurips_summarize.html', outputs = results, query = query, length = length, show_viz = show_viz, wc_name = wc_name, mf_name = mf_name)

if __name__ == '__main__':
   # testing = True
   # application.run(debug = testing, use_reloader = testing, host='0.0.0.0')
   application.debug = True
   application.use_reloader = True
   application.run()

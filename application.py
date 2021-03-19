
from flask import Flask, render_template, request
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
   return render_template('index.html')

@application.route('/info_summarize', methods = ['POST', 'GET'])
def info_summarize():
   """summarize url/text web page

   Returns:
      summary webpage
   """   
   
   # print("checkpoint")
   if request.method == 'POST':
      print("checkpoint")
      print(request.form)

      # get request content
      url = request.form['info_summarize_url']
      text = request.form['info_summarize_text']
      method = request.form['info_summarize_method']
      percentage = float(request.form["info_summarize_len"])

      # check url
      if url:
         text_out = read_url(url)
         if text_out != "ERROR!":
            text = text_out
      
      # check content for error case
      if not url and not text:
         return render_template('info_summarize.html', method = method, summary = "", original_text = "Cannot read url or text. Try again!")
      
      # get summary
      output = get_summary(text, percentage=percentage, method=method)
      summary = output['sentences']
      method = output['method']
      original_text = text

      return render_template('info_summarize.html', method = method, summary = summary, original_text = original_text)


@application.route('/medium_summarize', methods = ['POST', 'GET'])
def medium_summarize():
   """web page for summarizing medium publishers

   Returns:
       web page for summarizing medium publishers
   """

   if request.method == 'POST':
      print("checkpoint")
      print(request.form)

      # chekc request
      publisher = request.form['medium_summarize_publisher']
      start_date = request.form['medium_summarize_time_start']
      end_date = request.form['medium_summarize_time_end']
      time_period = f"From {start_date} to {end_date}"

      # convert time to usuable data
      start_date = datetime.strptime(start_date, "%Y-%m-%d")
      end_date = datetime.strptime(end_date, "%Y-%m-%d")
      
      # edge case
      if start_date > end_date:
         time_period = "Start date later than end date: Invalid time range. " + time_period
         output = []
         return render_template('medium_summarize.html', publisher = publisher, outputs = output, time_period = time_period, show_viz = False, name = "")

      # get the content + summaries
      output, text = get_medium(publisher, start_date, end_date)

      # check the visualization version
      show_viz = request.form['medium_summarize_visualize']
      name = f"medium_{publisher.translate(str.maketrans('', '', string.punctuation))}_{time.strftime('%Y%m%d-%H%M%S')}"
      name = name.replace(" ", "")
      name = name.lower()


      show_viz, wc_name, mf_name = show_viz_choice(name, show_viz, text)

      return render_template('medium_summarize.html', publisher = publisher, outputs = output, time_period = time_period, show_viz = show_viz, wc_name = wc_name, mf_name = mf_name) 


@application.route('/query_summarize', methods = ['POST', 'GET'])
def query_summarize():
   """web page to summarize queries from Medium

   Returns:
       html page: web page to summarize queries from Medium
   """   
   if request.method == 'POST':
      print("checkpoint")
      print(request.form)

      # chekc request page
      query = request.form['query_summarize']

      # get results
      results, text = get_query(query)

      length = len(results)

      # check condition for visualization
      show_viz = request.form['query_summarize_visualize']
      name = f"query_{query.translate(str.maketrans('', '', string.punctuation))}_{time.strftime('%Y%m%d-%H%M%S')}"
      name = name.replace(" ", "")
      name = name.lower()

      show_viz, wc_name, mf_name = show_viz_choice(name, show_viz, text)

      return render_template('query_summarize.html', outputs = results, query = query, length = length, show_viz = show_viz, wc_name = wc_name, mf_name = mf_name)


@application.route('/arxiv_summarize', methods = ['POST', 'GET'])
def arxiv_summarize():
   """web page to summarize queries from Arxiv

   Returns:
       html page: web page to summarize queries from Arxiv
   """ 
   if request.method == 'POST':
      print("checkpoint")
      print(request.form)

      # check request content
      query = request.form['query_arxiv']
      search_type = request.form["arxiv_searchtype"]
      size = request.form["arxiv_size"]

      # summarize
      results, text = get_arxiv(query, search_type, size)

      length = len(results)
      
      # check condition for visualization
      show_viz = request.form['arxiv_summarize_visualize']
      name = f"medium_{query.translate(str.maketrans('', '', string.punctuation))}_{time.strftime('%Y%m%d-%H%M%S')}"
      name = name.replace(" ", "")
      name = name.lower()

      show_viz, wc_name, mf_name = show_viz_choice(name, show_viz, text)

      return render_template('arxiv_summarize.html', outputs = results, query = query, length = length, show_viz = show_viz, wc_name = wc_name, mf_name = mf_name)

@application.route('/neurips_summarize', methods = ['POST', 'GET'])
def neurips_summarize():
   """web page to summarize queries from NeurIPS

   Returns:
       html page: web page to summarize queries from MNeurIPS
   """ 
   if request.method == 'POST':
      print("checkpoint")
      print(request.form)

      # chekc request content
      query = request.form['query_neurips']
      summarize_option = request.form['neurips_summarize'] == "Yes - with TextRank!"
      size = int(request.form["neurips_size"])

      # summarize neurips
      results, text = get_neurips(query, size, summarize_option)

      length = len(results)
      
      # check condition for visualization
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

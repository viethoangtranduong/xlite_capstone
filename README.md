# What's new 
## _The web app repo_

The file structure for the web app running at ""

- application.py: the flask app framework
- requirements.txt: the packages required to run the flask app
- README.md: the introductory file
- summary: the folder containing the models for summarization codes
    - vecrtorization: the embeddings for vectorizing the text to float
    - summarizer_{x}_model.py: the function to summarize based on any given models 
- get_content: The folder containing python files to get content from external sourcesc(crawling functions)
-   - get_{x}.py: file to crawl the content from x website
- get_viz: The folder to contain the visualization code, including the word cloud and most frequent plot. 
    - {viz_type}_viz.py: the file to create the viz_type
    - show_viz_choice.py: the abstract file to handle edge cases for the visualization code
- medium_data: crawled data for Medium publishers
- static: css + image component for the web app
- template: HTML file for the web app


## Steps to run the code

Move the local directory to the current xlite_capstone folder

Step 1: virtual environment
1.1. Create virtual environment:
```
virtualenv xlite_capstone_venv
```

1.2. Activate virtual environment
On Windows: 
```
xlite_capstone_venv\Scripts\activate
```
On Linux/Ubuntu:
```
xlite_capstone_venv/bin/activate
```

Step 2: Install dependencies
```
pip install -r requirements.txt
```
(or pip3, depending on your default pip version)

Step 3: Unzip the embeddings
Unzip the embeddings file at ```xlite_capstone/summary/vectorization/glove.6B.50d.zip``` and store the ```glove.6B.50d.txt``` file under ```xlite_capstone/summary/vectorization/glove.6B.50d.txt```

Step 4: Run web app:
```
python application.py
```
(or python3, depending on your default python)

The web app should be ready at ```http://127.0.0.1:5000/``` or ```localhost:5000```
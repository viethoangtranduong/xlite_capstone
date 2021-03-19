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
    

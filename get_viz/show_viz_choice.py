
from get_viz.most_frequent_viz import most_frequent_viz
from get_viz.wordcloud_viz import wordcloud_viz

def show_viz_choice(name, show_viz, text):
    """abstract for viz: to handle error cases

    Args:
        name (str): filename
        show_viz (str): type of viz to show
        text (str): string to plot

    Returns:
        show_viz: feasible showing option
        wc_name, mf_name: file location for plots
    """    
    wc_name = ""
    mf_name = ""

    # not edge cases to handle errors
    if show_viz == "1":
        pass
    elif show_viz == "2":
        wc_name = wordcloud_viz(text, name)
        if wc_name == "ERROR":
            show_viz = "1"        

    elif show_viz == "3":
        mf_name = most_frequent_viz(text, name)
        if mf_name == "ERROR":
            Show_viz = "1"

    elif show_viz == "4":
        wc_name = wordcloud_viz(text, name)
        mf_name = most_frequent_viz(text, name)

        if wc_name == "ERROR" and mf_name == "ERROR":
            show_viz = "1"
        elif wc_name == "ERROR": 
            show_viz = "3"
        elif mf_name == "ERROR":
            show_viz = "2"

    return show_viz, wc_name, mf_name
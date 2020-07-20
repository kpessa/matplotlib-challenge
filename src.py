# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st
import numpy as np
import seaborn as sns
from matplotlib import cm
import ipywidgets as widgets
import importlib

import ipywidgets as widgets
import pandas as pd
from IPython.display import clear_output

global df

def get_df_from_dropdown(value):
    if value == "mouse metadata":
        return get_mouse_metadata()
    elif value == "study results":
        return get_study_results()
    elif value == "raw data":
        return get_raw_data()
    elif value == "first instance":
        return get_first_instance_data()
    elif value == "last instance":
        return get_first_instance_data()
    elif value == "promising treatments":
        return get_four_promising_treatments()

def show_dataset_dropdown(dropdown):
    
    display(dropdown)

    def dropdown_eventhandler(change):
        clear_output()
        display(dropdown)
        if change.new == "mouse metadata":
            df = get_mouse_metadata()
            display(df)
        elif change.new == "study results":
            display(get_study_results())
        elif change.new == "raw data":
            display(get_raw_data())
        elif change.new == "first instance":
            display(get_first_instance_data())
        elif change.new == "last instance":
            display(get_last_instance_data())
        elif change.new == "promising treatments":
            df = get_four_promising_treatments()
            display(df)
        
    dropdown.observe(dropdown_eventhandler, names='value')
    

def get_mouse_metadata():
    """Returns the mouse data"""
    mouse_metadata_path = "data/Mouse_metadata.csv"
    df = pd.read_csv(mouse_metadata_path)
    return df

def get_study_results():
    """Returns the study results"""
    study_results_path = "data/Study_results.csv"
    df = pd.read_csv(study_results_path)
    return df

# Functions to get different dataframes for analysis
def get_raw_data():
    df = pd.merge(get_mouse_metadata(),get_study_results(),on='Mouse ID',how='outer')
    df.drop_duplicates(keep='first',inplace=True)
    return df

def get_last_instance_data():
    df = get_raw_data().drop_duplicates('Mouse ID',keep='last')
    return df

def get_first_instance_data():
    df = get_raw_data().drop_duplicates('Mouse ID',keep='first') 
    return df

def get_four_promising_treatments():
    df = get_last_instance_data().set_index('Drug Regimen').loc[["Capomulin","Ramicane","Infubinol","Ceftamin"]].rename(columns={"Tumor Volume (mm3)":"Final Tumor Volume (mm3)"})[["Mouse ID","Sex","Final Tumor Volume (mm3)"]]
    return df
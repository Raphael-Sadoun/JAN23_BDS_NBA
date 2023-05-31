import streamlit as st

title = "Code structure and workflow"
sidebar_name = "Code structure"


def run():

    st.markdown("---")
    st.title(title)
    st.markdown("---")
    
    st.markdown(
        """
        As part of this project, we have developped our own python library which implements 
        the data processing pipeline starting from the raw data and ending with the training and 
        validation sets used for training and optimizing different Machine Learning models.
        
        The structure of our python library consists of several individual modules :
        - **utils** :  
            General commonly used utility functions and global variables
        - **scrappers** :  
            Functions used for scrapping data from various NBA related websites
        - **preprocessing** :   
            Merging and aggregating datasets, data preprocessing
        - **feature_engine** :  
            Feature engineering and feature selection
        - **modelling** :  
            Definition of machine Learning models used and optimization
        """
        )
        
    st.markdown("#")
        
    st.markdown("##### Code structure and data workflow visualization : ")
 
    st.image('assets/code_structure.gif')
        
    st.markdown("The code is available at : https://github.com/DataScientest-Studio/JAN23_BDS_NBA")
    
    st.markdown("#")
    
    

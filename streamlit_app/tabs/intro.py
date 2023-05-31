import streamlit as st


title = "NBA Shot Data Analysis"
sidebar_name = "Overview"


def run():

    st.image("assets/banner.png")

    st.title(title)

    st.markdown("---")

    st.markdown(
        """
        Data collection and analysis has become an integral part of the National Basketball Association (NBA) 
        and is linked to the evolution of basketball as a sport in general. 
        
        Player, team and shot related data is collected, compiled and processed at an increasingly 
        growing rate in order to better understand and improve player performance and game results. 

        The goals of this project is to construct and apply a Machine Learning model to estimate the 
        probability of success of individual NBA shots as a function of numerous shot 
        and player specific features, such as distance, shot type, player shooting efficiency, etc.

        """
    )
    
    st.markdown(
        """
        ### Primary data sources
        - Shot data between 1997 and 2019 :  
            https://www.kaggle.com/jonathangmwl/nba-shot-locations
        - Play-by-play data between 2000 and 2020 :  
            https://sports-statistics.com/sports-data/nba-basketball-datasets-csv-files/
        - Team rankings between 2014 and 2018 :  
            https://www.kaggle.com/nathanlauga/nba-games?select=ranking.csv
        - Player data :  
            https://www.kaggle.com/drgilermo/nba-players-stats?select=Players.csv
        
        """
        )
        
    st.markdown(
            """
            ### Secondary data sources
            - https://www.basketball-reference.com/
            - https://www.nba.com/stats
            - https://github.com/swar/nba_api
            
            """
            )

    st.markdown('#')
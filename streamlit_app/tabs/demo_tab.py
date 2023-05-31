# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 17:14:02 2023

@author: Raphael Sadoun
"""

# Importation des modules utilisés
import sys
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from joblib import load

sys.path.append('../')
from nba_common_library.utils.utils import get_shooting_distance, get_shooting_angle

title = "Put yourself in the shoes of a pro NBA player!"
sidebar_name = "Demo"

player_list = ['LeBron James', 'Kevin Durant', 'James Harden', 'Russell Westbrook',
               'Chris Paul', 'Stephen Curry', 'DeMar DeRozan', 'Damian Lillard',
               'Rudy Gay', 'Paul George', 'Giannis Antetokounmpo', 'Nikola Jokic',
               'Kyrie Irving', 'Anthony Davis', 'Brook Lopez', 'Bradley Beal',
               'Kevin Love', 'Kemba Walker', 'Blake Griffin', 'Joel Embiid']
shot_list = ['Dunk', 'Jump Shot', 'Layup', 'Turnaround Jump Shot']
shot_types = [f"shoot_type_{x}" for x in ['dunk', 'jump_shoot', 'layup', 'turnaround']]
feet_to_meters = 0.3048
meters_to_inches = 39.3701
court_width = 50*feet_to_meters
court_length = 94*feet_to_meters
basket_pos_l = 6.4*feet_to_meters
extent = [-basket_pos_l, court_length-basket_pos_l,
          -court_width/2, court_width/2]

model = load('../model.joblib')
player_data = pd.read_csv('top_players_data.csv')

def run():

    st.markdown("---")
    st.title(title)
    st.markdown("---")
    
    player = st.selectbox(label= 'Choose a player', 
                          options = player_list)
    
    shot = st.selectbox(label='Select the type of shot',
                        options = shot_list)
    
    x = st.slider(label='X Position (meters)',
                  value=court_length/2-basket_pos_l,
                  min_value=extent[0],
                  max_value=extent[1],
                  step=0.1,
                  format="%.1f")
    y = st.slider(label='Y Position (meters)',
                  value=0.0,
                  min_value=extent[2],
                  max_value=extent[3],
                  step=0.1,
                  format="%.1f")
    
    fig = plt.figure(frameon=False)
    image_court = plt.imread("assets/full_court.png")
    plt.imshow(image_court, extent=extent)
    plt.text(x+0.3, y+0.3, player, 
             fontsize=8, fontfamily='serif')
    plt.scatter([x],[y])
    plt.xlim(extent[:2])
    plt.ylim(extent[2:])
    plt.axis('off')
    st.pyplot(fig)
    
    pushed = st.button(label='Predict the outcome of the shot please')
    if pushed:
        X = player_data.loc[player_data['player_name']==player].drop('player_name', axis=1)
        X = X.reset_index(drop=True)
        X.loc[0,'shot_distance'] = meters_to_inches*get_shooting_distance(x,y)
        X.loc[0,'shot_angle'] = get_shooting_angle(y,x)
        for shot_name, shot_type in zip(shot_list, shot_types):
            if shot==shot_name:
                X.loc[0,shot_type] = 1
            else:
                X.loc[0,shot_type] = 0
        X = X[model.feature_name_]
        y_pred_proba = model.predict_proba(X)[0,1]
        st.markdown(f"##### There is *{round(100*y_pred_proba,1)}* % chance that the shot will be successful!")
    st.markdown('#')
        
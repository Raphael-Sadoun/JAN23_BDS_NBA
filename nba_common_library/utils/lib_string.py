# -*- coding: utf-8 -*-
"""
Created on 03/02/2023 16:02 
@authors: GiovanniMINGHELLI, Raphael Sadoun
"""
from enum import Enum
import os
from nba_api.stats.static import teams

"""
Brief : This document contains all the strings used in the different code. To uniformize the code
and to get the same string everywhere, it is advised to use a variable to call this string.
Now, this library has to be imported in your python script file.
To get all the variables, do: from nba_common_library.lib_string import *
"""

##### RACINE DU PROJET ########################################
project_path = os.getcwd()
while os.path.basename(project_path) != "JAN23_BDS_NBA":
    project_path = os.path.dirname(project_path)

data = 'data'
if 'giovanni' in project_path:
    data = 'data.nosync'

database_path = os.path.join(project_path, data)


#### DIRS #############################################
raw_data = 'raw_data'
scrapped_data = 'scrapped_data'
transformed_data = 'transformed_data'
nba_common_library = 'nba_common_library'
utils = 'utils'
##### POSTES ##########################################
SG, SF, PG, C, PF, G, F = 'SG', 'SF', 'PG', 'C', 'PF', 'G', 'F'
starter_position = [SG, SF, PG, C, PF]

postes = {PG: 'Meneur',
          SG: 'Arrière',
          SF: 'Ailier',
          PF: 'Ailier fort',
          C: 'Pivot'}

postes_type = {'INT': [C, PF, SF, 'F-C'],
               'EXT': [SG, PG, G, F, 'G-F', 'F-G']}

#### NBA_API ##########################################

teams_data = teams.get_teams()
teams_ids = [team['id'] for team in teams_data]
teams_names = [team['abbreviation'] for team in teams_data]

##### DIMENSION ET LOCALISATION (DÉCIPIEDS) ##############################
X_lim = [-250, 250]
Y_lim = [-40, 900]
half_court_Y_lim = [Y_lim[0], Y_lim[1] / 2]
hoop_x, hoop_y = 0, 0

##### TYPES DE TIRS ##############################
shoot_types = {'layup': ['Layup Shot', 'Driving Layup Shot', 'Reverse Layup Shot', 'Running Layup Shot',
                         'Alley Oop Layup shot', 'Driving Finger Roll Layup Shot', 'Running Finger Roll Layup Shot',
                         'Running Reverse Layup Shot', 'Putback Layup Shot', 'Finger Roll Layup Shot',
                         'Driving Reverse Layup Shot', 'Tip Layup Shot', 'Cutting Layup Shot',
                         'Running Alley Oop Layup Shot', 'Cutting Finger Roll Layup Shot'],

               'dunk': ['Slam Dunk Shot', 'Dunk Shot', 'Driving Dunk Shot', 'Alley Oop Dunk Shot', 'Reverse Dunk Shot',
                        'Running Dunk Shot', 'Follow Up Dunk Shot', 'Putback Dunk Shot', 'Putback Dunk Shot',
                        'Driving Slam Dunk Shot', 'Reverse Slam Dunk Shot', 'Putback Slam Dunk Shot',
                        'Running Slam Dunk Shot', 'Putback Reverse Dunk Shot',
                        'Cutting Dunk Shot', 'Tip Dunk Shot', 'Running Alley Oop Dunk Shot',
                        'Driving Reverse Dunk Shot', 'Running Reverse Dunk Shot'],

               'jump_shoot': ['Jump Shot', 'Tip Shot', 'Running Jump Shot', 'No Shot', 'Driving Finger Roll Shot',
                              'Finger Roll Shot', 'Running Tip Shot', 'Fadeaway Jump Shot', 'Jump Bank Shot',
                              'Floating Jump shot', 'Pullup Jump shot', 'Running Bank shot',
                              'Step Back Jump shot', 'Driving Jump shot', 'Driving Bank shot',
                              'Fadeaway Bank shot', 'Pullup Bank shot', 'Running Bank Hook Shot',
                              'Running Pull-Up Jump Shot', 'Driving Floating Jump Shot',
                              'Driving Floating Bank Jump Shot', 'Step Back Bank Jump Shot',
                              'Running Finger Roll Shot'],

               'turnaround': ['Turnaround Jump Shot', 'Turnaround Hook Shot', 'Turnaround Finger Roll Shot',
                              'Turnaround Fadeaway shot', 'Turnaround Bank shot', 'Turnaround Bank Hook Shot',
                              'Turnaround Fadeaway Bank Jump Shot', 'Driving Hook Shot', 'Driving Bank Hook Shot',
                              'Jump Bank Hook Shot', 'Hook Bank Shot', 'Running Hook Shot', 'Jump Hook Shot',
                              'Hook Shot']}

##### VARIABLES ASSIGNÉES ##############################
game_id = 'game_id'
game_event_id = 'game_event_id'
event_num = 'event_num'
player_id = 'player_id'
player_name = 'player_name'
player_nickname = 'player_nickname'
team_id = 'team_id'
home_team_id = 'home_team_id'
away_team_id = 'away_team_id'
team_abb = 'team_abb'
team_city = 'team_city'
position = 'position'
league_id = 'league_id'
season_id = 'season_id'
season_year = 'season_year'
conference = 'conference'
team_name = 'team_name'
period = 'period'
minutes_remain = 'minutes_remain'
seconds_remain = 'seconds_remain'
action_type = 'action_type'
shot_type = 'shot_type'
shot_zone_basic = 'shot_zone_basic'
shot_zone_area = 'shot_zone_area'
shot_zone_range = 'shot_zone_range'
shot_distance = 'shot_distance'
shot_x_location = 'shot_x_location'
shot_y_location = 'shot_y_location'
shot_made_flag = 'shot_made_flag'
game_date = 'game_date'
home_team = 'home_team'
away_team = 'away_team'
season_type = 'season_type'
height = 'height'
weight = 'weight'
college = 'college'
dob = 'dob'
birth_city = 'birth_city'
birth_state = 'birth_state'
event_msg_action_type = 'event_msg_action_type'
event_msg_type = 'event_msg_type'
home_description = 'home_description'
neutral_description = 'neutral_description'
visitor_description = 'visitor_description'
pc_timestring = 'pc_timestring'
wc_timestring = 'wc_timestring'
person_1_type = 'person_1_type'
person_2_type = 'person_2_type'
person_3_type = 'person_3_type'
player_1_id = 'player_1_id'
player_2_id = 'player_2_id'
player_3_id = 'player_3_id'
player_1_name = 'player_1_name'
player_2_name = 'player_2_name'
player_3_name = 'player_3_name'
player_1_team_abb = 'player_1_team_abb'
player_2_team_abb = 'player_2_team_abb'
player_3_team_abb = 'player_3_team_abb'
player_1_team_city = 'player_1_team_city'
player_2_team_city = 'player_2_team_city'
player_3_team_city = 'player_3_team_city'
player_1_team_id = 'player_1_team_id'
player_2_team_id = 'player_2_team_id'
player_3_team_id = 'player_3_team_id'
player_1_team_nickname = 'player_1_team_nickname'
player_2_team_nickname = 'player_2_team_nickname'
player_3_team_nickname = 'player_3_team_nickname'
score = 'score'
score_margin = 'score_margin'
game_played = 'game_played'
game_won = 'game_won'
game_loss = 'game_loss'
won_ratio = 'won_ratio'
home_record = 'home_record'
away_record = 'away_record'
return_to_play = 'return_to_play'
unnamed = 'unnamed'
winning_team = 'winning_team'
game_time = 'game_time'
url = 'url'
game_type = 'game_type'
location = 'location'
away_team_abb = 'away_team_abb'
home_team_abb = 'home_team_abb'
away_score = 'away_score'
home_score = 'home_score'
shooter = 'shooter'
assister = 'assister'
blocker = 'blocker'
foul_type = 'foul_type'
fouler = 'fouler'
fouled = 'fouled'
rebounder = 'rebounder'
rebound_type = 'rebound_type'
violation_player = 'violation_player'
violation_type = 'violation_type'
timeout_team = 'timeout_team'
free_throw_shooter = 'free_throw_shooter'
free_throw_outcome = 'free_throw_outcome'
free_throw_num = 'free_throw_num'
enter_game = 'enter_game'
leave_game = 'leave_game'
turnover_player = 'turnover_player'
turnover_type = 'turnover_type'
turnover_cause = 'turnover_cause'
turnover_causer = 'turnover_causer'
jumpball_away_player = 'jumpball_away_player'
jumpball_home_player = 'jumpball_home_player'
jumpball_poss = 'jumpball_poss'
year_start = 'year_start'
year_end = 'year_end'
pts = 'pts'
pts_rank = 'pts_rank'
is_active = 'is_active'
Age = 'Age'
Tm = 'Tm'
G = 'G'
GS = 'GS'
MP = 'MP'
PER = 'PER'
TS_PCT = 'TS%'
FG3PAr = '3PAr'
FTr = 'FTr'
ORB_PCT = 'ORB%'
DRB_PCT = 'DRB%'
TRB_PCT = 'TRB%'
AST_PCT = 'AST%'
STL_PCT = 'STL%'
BLK_PCT = 'BLK%'
TOV_PCT = 'TOV%'
USG_PCT = 'USG%'
OWS = 'OWS'
DWS = 'DWS'
WS = 'WS'
WS_per_48 = 'WS/48'
OBPM = 'OBPM'
DBPM = 'DBPM'
BPM = 'BPM'
VORP = 'VORP'
FG = 'FG'
FGA = 'FGA'
FG_PCT = 'FG%'
FG3P = '3P'
FG3PA = '3PA'
FG3P_PCT = '3P%'
FG2P = '2P'
FG2PA = '2PA'
FG2P_PCT = '2P%'
eFG_PCT = 'eFG%'
FT = 'FT'
FTA = 'FTA'
FT_PCT = 'FT%'
ORB = 'ORB'
DRB = 'DRB'
TRB = 'TRB'
AST = 'AST'
STL = 'STL'
BLK = 'BLK'
TOV = 'TOV'
PF = 'PF'
PTS_home = 'PTS_home'
FG_PCT_home = 'FG%_home'
FT_PCT_home = 'FT%_home'
FG3_PCT_home = 'FG3%_home'
AST_home = 'AST_home'
REB_home = 'REB_home'
PTS_away = 'PTS_away'
FG_PCT_away = 'FG%_away'
FT_PCT_away = 'FT%_away'
FG3_PCT_away = 'FG3%_away'
AST_away = 'AST_away'
REB_away = 'REB_away'
is_home_team_wins = 'is_home_team_wins'
is_3pt_shot = '3pt_shot'
won_ratio_at_home = 'won_ratio_at_home'
won_ratio_away = 'won_ratio_away'

### Variables inutiles pour la modélisation ##############################
unused_variables = [player_id,              # Identifiant du joueur
                    player_name,            # Nom du joueur
                    game_id,                # Identifiant du match
                    game_event_id,          # Identifiant de l'action au cours du match
                    team_id,                # Identifiant de l'équipe
                    team_name,              # Nome de l'équipe
                    minutes_remain,         # Redondant avec la variable time_remain_curper ajouté par feature_engineering
                    seconds_remain,         # Redondant avec la variable time_remain_curper ajouté par feature_engineering
                    game_date,              # Date du match
                    home_team,              # Nom de l'équipe qui joue à domicile
                    away_team,              # Nom de l'équipe qui joue à l'extérieur
                    season_type,            # Saison régulière ou playoffs, dans notre cas uniquement saison régulière
                    college,                # Université du joueur
                    dob,                    # Date de naissance
                    birth_city,             # Ville de naissance
                    birth_state,            # Pays ou etat (si citoyen US) de naissance du joueur
                    league_id,              # Identifiant de la ligue de basket, ici uniquement la NBA (valeur unique)
                    season_id,              # Identifiant de la saison NBA 
                                            # INUTILE TANT QUE L'ON TRAVAILLE SUR UNE SAISON UNIQUE
                    home_record,            # String donnant le nombre de victoires/défaites à domicile
                                            # Converti en un ratio lors du feature_engineering
                    away_record,            # Pareil qu'au dessus mais pour les matchs à l'exterieur
                    return_to_play,         # Indique si l'équipe a recommencé à jouer après le covid, inutile pour nos saisons
                                            # et ne contient que des valeurs manquantes
                    action_type,            # Catégorie de tir, redondant avec shoot_type ajouté par feature_engineering
                    shot_type,              # Indique si le tir est à 3pt ou non, converti en variable binaire par le feature_engineering
                    home_description,       # String expliquant le détail de l'action pour le joueur qui joue à domicile
                    visitor_description,    # Pareil qu'au dessus mais pour le joueur qui joue à l'extérieur
                    neutral_description,    # Pareil qu'au dessus mais pour le 3e joueur impliqué dans l'action s'il y en a
                    pc_timestring,          # String indiquant quand a eu lieu l'action dans le quart-temps en cours
                                            # redondant avec time_remain_curper ajouté par feature_engineering
                    wc_timestring,          # String indiquant l'heure à laquelle l'action a eu lieue
                    event_msg_type,         # Identifiant du type d'action, dans notre case redondant avec la variable cible
                    event_msg_action_type,  # Sous-catégories de event_msg_type, redondant avec shoot_type ajouté par feature engineering
                    event_num,              # Identifiant de l'action pendant le match
                    player_1_id,            # Identifiant du joueur 1 participant à l'action
                    player_1_name,          # Nom du joueur 1 participant à l'action
                    player_1_team_abb,      # Nom abrégé de l'equipe du joueur 1 participant à l'action
                    player_1_team_city,     # Ville de l'equipe du joueur 1 participant à l'action
                    player_1_team_nickname, # Surnom de l'equipe du joueur 1 participant à l'action
                    player_1_team_id,       # Identifiant de l'equipe du joueur 1 participant à l'action
                    player_2_id,            # Identifiant du joueur 2 participant à l'action
                    player_2_name,          # Nom du joueur 2 participant à l'action
                    player_2_team_abb,      # Nom abrégé de l'equipe du joueur 2 participant à l'action
                    player_2_team_city,     # Ville de l'equipe du joueur 2 participant à l'action
                    player_2_team_nickname, # Surnom de l'equipe du joueur 2 participant à l'action
                    player_2_team_id,       # Identifiant de l'equipe du joueur 2 participant à l'action
                    player_3_id,            # Identifiant du joueur 3 participant à l'action
                    player_3_name,          # Nom du joueur 3 participant à l'action
                    player_3_team_abb,      # Nom abrégé de l'equipe du joueur 3 participant à l'action
                    player_3_team_city,     # Ville de l'equipe du joueur 3 participant à l'action
                    player_3_team_nickname, # Surnom de l'equipe du joueur 3 participant à l'action
                    player_3_team_id,       # Identifiant de l'equipe du joueur 3 participant à l'action
                    score                   # Indique le score du match au moment du tir, redondant avec score_margin
                    ]

### Variables utiles pour la modélisation ##############################
useful_features = ['period', 
                   'shot_zone_basic',
                   'shot_zone_area',
                   'shot_zone_range',
                   'shot_distance',
                   'conference',
                   'game_played',
                   'game_won',
                   'game_loss',
                   'won_ratio',
                   'won_ratio_at_home',
                   'won_ratio_away',
                   'score_margin',
                   'height',
                   'weight',
                   'player_1_position',
                   'player_1_pos_type',
                   'shot_angle',
                   'dominant_hand',
                   'quadrant',
                   'time_remain_curper', 
                   'total_time_remain',
                   'is_at_home',
                   'shoot_type',
                   '3pt_shot',
                   'games_played',  
                   'minutes_played',        
                   'player_efficiency_rating',      
                   'true_shooting_percentage',       
                   'three_point_attempt_rate',      
                   'free_throw_attempt_rate',       
                   'offensive_rebound_percentage',   
                   'defensive_rebound_percentage',   
                   'total_rebound_percentage',  
                   'assist_percentage',  
                   'steal_percentage',   
                   'block_percentage',  
                   'turnover_percentage',  
                   'usage_percentage',  
                   'offensive_win_shares',   
                   'defensive_win_shares',   
                   'win_shares',   
                   'win_shares_per_48_minutes',   
                   'offensive_box_plus_minus',   
                   'defensive_box_plus_minus',  
                   'box_plus_minus',   
                   'value_over_replacement_player',               
                   'fg_score',  
                   'fg3_score', 
                   'ft_score',  
                   'mp_per_game',  
                   'opp_fg_per_game',  
                   'opp_fga_per_game',  
                   'opp_fg_percent',  
                   'opp_x3p_per_game', 
                   'opp_x3pa_per_game',  
                   'opp_x3p_percent',  
                   'opp_x2p_per_game',  
                   'opp_x2pa_per_game', 
                   'opp_x2p_percent', 
                   'opp_ft_per_game',  
                   'opp_fta_per_game',  
                   'opp_ft_percent',  
                   'opp_pf_per_game', 
                   'opp_pts_per_game'  
                   ]

## Variable catégorielles non ordonnées
# elle sont encodées avec un OneHotEncoder lors du preprocessing
one_hot_features = ['shot_zone_basic', 
                    'shot_zone_area', 
                    'shot_zone_range',
                    'conference',
                    'dominant_hand',
                    'player_1_position',
                    'player_1_pos_type',
                    'quadrant',
                    'shoot_type'
                    ]

##### VARIABLES HARMONISÉS ##############################
conventional_naming = {game_id: ['game_id', 'Game ID', 'GAME_ID'],
                       game_event_id: ['game_event_id', 'Game Event ID'],
                       event_num: ['event_num', 'EVENTNUM'],
                       player_id: ['player_id', 'Player ID', 'PLAYER_ID'],
                       player_name: ['player_name', 'Player Name', 'Player', 'name', 'PLAYER_NAME'],
                       player_nickname: ['player_nickname', 'NICKNAME'],
                       team_id: ['team_id', 'Team ID', 'TEAM_ID'],
                       home_team_id: ['home_team_id', 'HOME_TEAM_ID', 'TEAM_ID_home'],
                       away_team_id: ['away_team_id', 'VISITOR_TEAM_ID', 'TEAM_ID_away'],
                       team_abb: ['team_abb', 'TEAM_ABBREVIATION', 'abbreviation'],
                       team_city: ['team_city', 'TEAM_CITY'],
                       position: ['position', 'Pos', 'START_POSITION'],
                       league_id: ['league_id', 'LEAGUE_ID'],
                       season_id: ['season_id', 'SEASON_ID'],
                       season_year: ['season_year', 'SEASON', 'Year'],
                       conference: ['conference', 'CONFERENCE'],
                       team_name: ['team_name', 'Team Name', 'TEAM'],
                       period: ['period', 'Period', 'Quarter', 'PERIOD'],
                       minutes_remain: ['minutes_remain', 'Minutes Remaining'],
                       seconds_remain: ['seconds_remain', 'Seconds Remaining', 'SecLeft'],
                       action_type: ['action_type', 'Action Type'],
                       shot_type: ['shot_type', 'Shot Type', 'ShotType'],
                       shot_zone_basic: ['shot_zone_basic', 'Shot Zone Basic'],
                       shot_zone_area: ['shot_zone_area', 'Shot Zone Area'],
                       shot_zone_range: ['shot_zone_range', 'Shot Zone Range'],
                       shot_distance: ['shot_distance', 'Shot Distance', 'ShotDist'],
                       shot_x_location: ['shot_x_location', 'X Location'],
                       shot_y_location: ['shot_y_location', 'Y Location'],
                       shot_made_flag: ['shot_made_flag', 'Shot Made Flag', 'ShotOutcome'],
                       game_date: ['game_date', 'Game Date', 'STANDINGSDATE', 'Date', 'GAME_DATE_EST'],
                       home_team: ['home_team', 'Home Team'],
                       away_team: ['away_team', 'Away Team'],
                       season_type: ['season_type', 'Season Type', 'GAME_STATUS_TEXT'],
                       height: ['height'],
                       weight: ['weight'],
                       college: ['college', 'collage'],
                       dob: ['dob', 'born', 'birth_date'],
                       birth_city: ['birth_city'],
                       birth_state: ['birth_state'],
                       event_msg_action_type: ['event_msg_action_type', 'EVENTMSGACTIONTYPE'],
                       event_msg_type: ['event_msg_type', 'EVENTMSGTYPE'],
                       home_description: ['home_description', 'HOMEDESCRIPTION', 'HomePlay'],
                       neutral_description: ['neutral_description', 'NEUTRALDESCRIPTION'],
                       visitor_description: ['visitor_description', 'VISITORDESCRIPTION', 'AwayPlay'],
                       pc_timestring: ['pc_timestring', 'PCTIMESTRING'],
                       wc_timestring: ['wc_timestring', 'WCTIMESTRING', 'Time'],
                       person_1_type: ['person_1_type', 'PERSON1TYPE'],
                       person_2_type: ['person_2_type', 'PERSON2TYPE'],
                       person_3_type: ['person_3_type', 'PERSON3TYPE'],
                       player_1_id: ['player_1_id', 'PLAYER1_ID'],
                       player_2_id: ['player_2_id', 'PLAYER2_ID'],
                       player_3_id: ['player_3_id', 'PLAYER3_ID'],
                       player_1_name: ['player_1_name', 'PLAYER1_NAME'],
                       player_2_name: ['player_2_name', 'PLAYER2_NAME'],
                       player_3_name: ['player_3_name', 'PLAYER3_NAME'],
                       player_1_team_abb: ['player_1_team_abb', 'PLAYER1_TEAM_ABBREVIATION'],
                       player_2_team_abb: ['player_2_team_abb', 'PLAYER2_TEAM_ABBREVIATION'],
                       player_3_team_abb: ['player_3_team_abb', 'PLAYER3_TEAM_ABBREVIATION'],
                       player_1_team_city: ['player_1_team_city', 'PLAYER1_TEAM_CITY'],
                       player_2_team_city: ['player_2_team_city', 'PLAYER2_TEAM_CITY'],
                       player_3_team_city: ['player_3_team_city', 'PLAYER3_TEAM_CITY'],
                       player_1_team_id: ['player_1_team_id', 'PLAYER1_TEAM_ID'],
                       player_2_team_id: ['player_2_team_id', 'PLAYER2_TEAM_ID'],
                       player_3_team_id: ['player_3_team_id', 'PLAYER3_TEAM_ID'],
                       player_1_team_nickname: ['player_1_team_nickname', 'PLAYER1_TEAM_NICKNAME'],
                       player_2_team_nickname: ['player_2_team_nickname', 'PLAYER2_TEAM_NICKNAME'],
                       player_3_team_nickname: ['player_3_team_nickname', 'PLAYER3_TEAM_NICKNAME'],
                       score: ['score', 'SCORE'],
                       score_margin: ['score_margin', 'SCOREMARGIN', 'PLUS_MINUS'],
                       game_played: ['game_played', 'G'],
                       game_won: ['game_won', 'W'],
                       game_loss: ['game_loss', 'L'],
                       won_ratio: ['won_ratio', 'W_PCT'],
                       home_record: ['home_record', 'HOME_RECORD'],
                       away_record: ['away_record', 'ROAD_RECORD'],
                       return_to_play: ['return_to_play', 'RETURNTOPLAY'],
                       unnamed: ['unnamed', 'unnamed.1', 'Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 40', 'blanl',
                                 'blank2', 'COMMENT'],
                       winning_team: ['winning_team', 'WinningTeam'],
                       game_time: ['game_time', 'MIN'],

                       url: ['url', 'URL'],
                       game_type: ['game_type', 'GameType'],
                       location: ['location', 'Location'],
                       away_team_abb: ['away_team_abb', 'AwayTeam'],
                       home_team_abb: ['home_team_abb', 'HomeTeam'],
                       away_score: ['away_score', 'AwayScore'],
                       home_score: ['home_score', 'HomeScore'],
                       shooter: ['shooter', 'Shooter'],
                       assister: ['assister', 'Assister'],
                       blocker: ['blocker', 'Blocker'],
                       foul_type: ['foul_type', 'FoulType'],
                       fouler: ['fouler', 'Fouler'],
                       fouled: ['fouled', 'Fouled'],
                       rebounder: ['rebounder', 'Rebounder'],
                       rebound_type: ['rebound_type', 'ReboundType'],
                       violation_player: ['violation_player', 'ViolationPlayer'],
                       violation_type: ['violation_type', 'ViolationType'],
                       timeout_team: ['timeout_team', 'TimeoutTeam'],
                       free_throw_shooter: ['free_throw_shooter', 'FreeThrowShooter'],
                       free_throw_outcome: ['free_throw_outcome', 'FreeThrowOutcome'],
                       free_throw_num: ['free_throw_num', 'FreeThrowNum'],
                       enter_game: ['EnterGame', 'enter_game'],
                       leave_game: ['LeaveGame', 'leave_game'],
                       turnover_player: ['turnover_player', 'TurnoverPlayer'],
                       turnover_type: ['turnover_type', 'TurnoverType'],
                       turnover_cause: ['turnover_cause', 'TurnoverCause'],
                       turnover_causer: ['turnover_causer', 'TurnoverCauser'],
                       jumpball_away_player: ['jumpball_away_player', 'JumpballAwayPlayer'],
                       jumpball_home_player: ['jumpball_home_player', 'JumpballHomePlayer'],
                       jumpball_poss: ['jumpball_poss', 'JumpballPoss'],
                       year_start: ['year_start'],
                       year_end: ['year_end'],
                       pts: ['pts', 'PTS'],
                       pts_rank: ['pts_rank', 'PTS_RANK'],
                       is_active: ['is_active', 'IS_ACTIVE_FLAG'],

                       # https://www.basketball-reference.com/about/glossary.html

                       Age: ['Age'],
                       Tm: ['Tm'],
                       G: ['G'],
                       GS: ['GS'],
                       MP: ['MP'],
                       PER: ['PER'],
                       TS_PCT: ['TS%'],
                       FG3PAr: ['3PAr'],
                       FTr: ['FTr'],
                       ORB_PCT: ['ORB%'],
                       DRB_PCT: ['DRB%'],
                       TRB_PCT: ['TRB%'],
                       AST_PCT: ['AST%'],
                       STL_PCT: ['STL%'],
                       BLK_PCT: ['BLK%'],
                       TOV_PCT: ['TOV%'],
                       USG_PCT: ['USG%'],
                       OWS: ['OWS'],
                       DWS: ['DWS'],
                       WS: ['WS'],
                       WS_per_48: ['WS/48'],
                       OBPM: ['OBPM'],
                       DBPM: ['DBPM'],
                       BPM: ['BPM'],
                       VORP: ['VORP'],
                       FG: ['FG'],
                       FGA: ['FGA'],
                       FG_PCT: ['FG%', 'FG_PCT'],
                       FG3P: ['3P', 'FG3M'],
                       FG3PA: ['3PA', 'FG3A'],
                       FG3P_PCT: ['3P%', 'FG3_PCT'],
                       FG2P: ['2P', 'FGM'],
                       FG2PA: ['2PA', 'FGA'],
                       FG2P_PCT: ['2P%', 'FG_PCT'],
                       eFG_PCT: ['eFG%'],
                       FT: ['FT', 'FTM'],
                       FTA: ['FTA'],
                       FT_PCT: ['FT%', 'FT_PCT'],
                       ORB: ['ORB', 'OREB'],
                       DRB: ['DRB', 'DREB'],
                       TRB: ['TRB', 'REB'],
                       AST: ['AST'],
                       STL: ['STL'],
                       BLK: ['BLK'],
                       TOV: ['TOV', 'TO'],
                       PF: ['PF'],

                       PTS_home: ['PTS_home'],
                       FG_PCT_home: ['FG%_home', 'FG_PCT_home'],
                       FT_PCT_home: ['FT%_home', 'FT_PCT_home'],
                       FG3_PCT_home: ['FG3%_home', 'FG3_PCT_home'],
                       AST_home: ['AST_home'],
                       REB_home: ['REB_home'],
                       PTS_away: ['PTS_away'],
                       FG_PCT_away: ['FG%_away', 'FG_PCT_away'],
                       FT_PCT_away: ['FT%_away', 'FT_PCT_away'],
                       FG3_PCT_away: ['FG3%_away', 'FG3_PCT_away'],
                       AST_away: ['AST_away'],
                       REB_away: ['REB_away'],
                       is_home_team_wins: ['is_home_team_wins', 'HOME_TEAM_WINS']

                       }


class EventMsgType(Enum):
    FIELD_GOAL_MADE = 1
    FIELD_GOAL_MISSED = 2
    FREE_THROW = 3
    REBOUND = 4
    TURNOVER = 5
    FOUL = 6
    VIOLATION = 7
    SUBSTITUTION = 8
    TIMEOUT = 9
    JUMP_BALL = 10
    EJECTION = 11
    PERIOD_BEGIN = 12
    PERIOD_END = 13

# %%

# -*- coding: utf-8 -*-
"""
Created on 31/01/2023 15:54
@author: GiovanniMINGHELLI
"""
import math
from nba_common_library.utils.lib_string import *
import pandas as pd
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

"""
Brief : This file contains all the main functions needed in the project. To uniformize the code
and to get the same returns everywhere, it is advised to use theses functiuns to process the data.
This library has to be imported in your python script file.
To get all the function, do: from nba_common_library.utils import *
"""


def get_path_file(file):
    for dirs, root, files in os.walk(database_path):
        if file in files:
            return os.path.join(dirs, file)
        if file + '.csv' in files:
            return os.path.join(dirs, file + '.csv')
    return None


def convert_us_height(height_):
    """
    Cette fonction convertis les tailles américaines représentés sous la
    forme 7-9 (feet-inches) en taille centimètre
    7 pied*(30.48cm) + 9 pouces*(2.54cm)

    :param height_:
    height (str) : La taille au format string séparée par un tiret -

    :return:
    int : un entier de la taille en centimètre

    Example :
    >>> convert_us_height('7-9')
    206
    """
    try:
        split_height = list(map(int, str(height_).split("-")))
    except AttributeError or ValueError:
        split_height = list(map(int, height_.split("-")))
    return math.ceil((split_height[0] * 30.48) + (split_height[1] * 2.54))


def feet_to_meters(feet_distance):
    """
    Convertit une valeur exprimée en pieds en mètres.

    :param feet_distance: La valeur en pieds à convertir, qui peut être un nombre en virgule flottante
            ou une chaîne de caractères représentant un nombre.
    :return: La valeur convertie en mètres, arrondie à 2 décimales.
    """
    try:
        feet = float(feet_distance)
    except ValueError:
        feet = float(feet_distance.split()[0])

    return round(feet * 0.3048, 2)


def inches_to_centimeters(inches_distance):
    """
    Convertit une valeur exprimée en pouces en centimètres.

    :param inches_distance: La valeur en pouces à convertir, qui peut être un nombre en virgule flottante
            ou une chaîne de caractères représentant un nombre.
    :return: La valeur convertie en mètres, arrondie à 2 décimales.
    """
    try:
        inches = float(inches_distance)
    except ValueError:
        inches = float(inches_distance.split()[0])

    return round(inches * 2.54, 2)


def merge_dicts(*dict_args):
    """
    Fusionne plusieurs dictionnaires en un seul en supprimant les clés doublons.
    En cas de conflit, la paire clé-valeur la plus récente est prioritaire.

    Arguments :
    dict_args (tuple) : les dictionnaires à fusionner.

    Returns :
    dict : un nouveau dictionnaire qui est la fusion des dictionnaires fournis en entrée.

    Example :
    >>> d1 = {'a': 1, 'b': 2}
    >>> d2 = {'b': 3, 'c': 4}
    >>> merge_dicts(d1, d2)

    {'a': 1, 'b': 3, 'c': 4}
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def map_position():
    """
    Recupère et stock dans un dictionnaire le poste de chaque joueur présent
    dans au moins un deux fichiers CSV référencant les attributs des joueurs.

    Returns :
    dict : Un dictionnaire associant le nom d'un joueur à sa position.

    Example :
    >>> map_position()
    {'Hakeem Olajuwon': 'C', 'Kareem Abdul-Jabbar': 'C', ...}
    """

    file_path_1 = os.path.join(get_path_file('player_data.csv'))
    file_path_2 = os.path.join(get_path_file('seasons_stats.csv'))

    temp_dict = {}
    for file in [file_path_1, file_path_2]:
        if os.path.exists(file):
            temp_dict[file] = pd.read_csv(file, low_memory=False)
        else:
            raise FileNotFoundError

    return merge_dicts({player: pos_ for player, pos_ in zip(temp_dict[file_path_1].player_name,
                                                             temp_dict[file_path_1].position)},
                       {player: pos_ for player, pos_ in zip(temp_dict[file_path_2].player_name,
                                                             temp_dict[file_path_2].position)})


def get_shooting_distance(x, y):
    """Théroème de Pythagore
    :param: x (coté adjacent)
    :param: y (coté opposé)
    :return: float (hypothénus)
    """
    return math.sqrt(y ** 2 + x ** 2)


def get_shooting_angle(x, y):
    """
    Calcule l'angle absolu en degrés d'un tir au panier en fonction des coordonnées x et y du tir.
    L'angle calculé et celui sous la panier formé par le triangle rectangle le long de l'axe y (0, y),
    avec la position du panier (0, 0) et la position du shoot (x, y)
    :param: x (float): La coordonnée x du tir.
    :param: y (float): La coordonnée y du tir.
    :return: (int): L'angle en degrés du tir, compris entre -180 et 180.
    Exemples:
        >>> get_shooting_angle(0, 10)
        90
        >>> get_shooting_angle(-100, 50)
        153
        >>> get_shooting_angle(50, -30)
        30
    """

    abs_x, abs_y = abs(x), abs(y)
    sign_x, sign_y = math.copysign(1, x), math.copysign(1, y)

    if abs_y == 0:
        return 90.0 if x != 0 else 0.0

    if abs_x == 0:
        return 0.0 if sign_y >= 0 else 180.0

    angle = math.atan(abs_x / abs_y) * (180.0 / math.pi)

    if sign_y < 0 < sign_x:
        angle = 180.0 - angle
    elif sign_y < 0 and sign_x < 0:
        angle = angle - 180.0
    elif sign_y > 0 > sign_x:
        angle = -angle

    return int(abs(angle))


def get_shooting_quadrant(x, y):
    if x >= 0 and y >= 0:
        return 1
    elif x < 0 < y:
        return 2
    elif x <= 0 and y <= 0:
        return 3
    else:
        return 4


def dual_situation(row):
    row = row[['player_1_team_id', 'player_2_team_id', 'player_3_team_id']]
    return f'{sum(row == row[0])}v{len(row.dropna()) - sum(row == row[0])}'

def get_nba_season_dates(season=2019):
    """
    Fonction permettant d'obtenir les dates de début et de fin d'une saison nba

    -- nba_season: La saison NBA au format "xxxx-xx" (ex: "2000-01")

    Retourne un tuple contenant les dates de debut et de fin de saison au format datetime
    """

    # On parse le site de wikipédia pour trouver les dates officielles 
    # de début et de fin de la saison spécifiée
    url_wiki = f"https://en.wikipedia.org/wiki/{season-1}-{season % 1000}_NBA_season"
    page = urlopen(url_wiki)
    soup = BeautifulSoup(page, features="lxml")
    text = soup.findAll("td", {"class": "infobox-data"})[2].text
    text = text.split(" – ")
    start_date = text[0]
    if text[-1].split(",")[0].isnumeric():
        end_date = text[-2].split(" ")[-2] + " " + text[-1].split(" ")[0] + " " + text[-1].split(" ")[1]
    else:
        end_date = text[-1].split(" (")[0]

    # Conversion au format datetime
    start_date = datetime.strptime(start_date, "%B %d, %Y")
    end_date = datetime.strptime(end_date, "%B %d, %Y")
    return start_date, end_date


def get_type_duel(duel):
    poste_1, poste_2 = duel.split(" v ")
    type_1 = next((key for key, values in postes_type.items() if poste_1 in values), None)
    type_2 = next((key for key, values in postes_type.items() if poste_2 in values), None)
    if type_1 and type_2:
        return f"{type_1} v {type_2}"
    return None


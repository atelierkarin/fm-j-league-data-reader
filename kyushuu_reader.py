import csv
import re
import math
import pandas as pd

x = list(range(1, 91))

# 九州リーグのHTMLファイルをローカルにセーブし、それを読み込む
urls = [("kyushuu/" + str(i) + ".html") for i in x]

team_info = {}

for url in urls:

  # Read HTML
  print("Reading {}...".format(url))
  dfs = pd.read_html(url)

  # Get Tables
  table_team_info = dfs[1]
  table_sub_and_goals_info = dfs[6]
  table_home_members = dfs[10]
  table_away_members = dfs[11]

  # Team Info
  name_home_team = table_team_info[0][0].replace('\u3000', ' ').split('  キックオフ', 1)[0]
  name_away_team = table_team_info[2][0].replace('\u3000', ' ').split('  キックオフ', 1)[0]

  if not name_home_team in team_info.keys():
    team_info[name_home_team] = {}
  if not name_away_team in team_info.keys():
    team_info[name_away_team] = {}

  # Sub and Goal Info
  home_sub_list_raw = table_sub_and_goals_info[0][0]
  away_sub_list_raw = table_sub_and_goals_info[2][0]
  home_sub_list = []
  away_sub_list = []

  home_goal_list_raw = table_sub_and_goals_info[0][3]
  away_goal_list_raw = table_sub_and_goals_info[2][3]
  home_goal_list = []
  away_goal_list = []

  # Check nan
  if not type(home_sub_list_raw) == str: home_sub_list_raw = ''
  if not type(away_sub_list_raw) == str: away_sub_list_raw = ''
  if not type(home_goal_list_raw) == str: home_goal_list_raw = ''
  if not type(away_goal_list_raw) == str: away_goal_list_raw = ''

  # Subs
  home_sub_list_raw = re.split('  ', home_sub_list_raw)
  away_sub_list_raw = re.split('  ', away_sub_list_raw)

  for item in home_sub_list_raw:
    if '[in]' in item:
      home_sub_list.append(item.replace('[in]', '').replace('\u3000', '').replace(' ', ''))
  for item in away_sub_list_raw:
    if '[in]' in item:
      away_sub_list.append(item.replace('[in]', '').replace('\u3000', '').replace(' ', ''))

  # Goals
  home_goal_list_raw = re.split('\d+  分  ', home_goal_list_raw.replace('  ＋', ''))
  away_goal_list_raw = re.split('\d+  分  ', away_goal_list_raw.replace('  ＋', ''))
  for item in home_goal_list_raw:
    if len(item) > 0 and not item[0].isdigit():
      home_goal_list.append(item.replace('\u3000', '').split('（', 1)[0].replace(' ', ''))
  for item in away_goal_list_raw:
    if len(item) > 0 and not item[0].isdigit():
      away_goal_list.append(item.replace('\u3000', '').split('（', 1)[0].replace(' ', ''))

  # Home Members
  is_sub = False
  for column_name, item in table_home_members.iterrows():    
    if item[0] == "SUB":
      is_sub = True
    if type(item[7]) == str and item[7].isdigit():
      player_name = item[6].replace('\u3000', '').split('  （', 1)[0].replace(' ', '')
      app = 0
      if not is_sub:
        app = 1
      elif player_name in home_sub_list:
        app = 1

      if player_name in team_info[name_home_team].keys():
        base_app = team_info[name_home_team][player_name][0]
        base_goal = team_info[name_home_team][player_name][1]
        team_info[name_home_team][player_name] = [base_app+app,base_goal]
      else:
        team_info[name_home_team][player_name] = [app,0]
  
  for item in home_goal_list:
    if item == 'オウンゴール':
      pass
    else:
      base_info = team_info[name_home_team][item]
      update_base_info = [base_info[0], base_info[1] + 1]
      team_info[name_home_team][item] = update_base_info
  
  # Away Memebers
  is_sub = False
  for column_name, item in table_away_members.iterrows():    
    if item[0] == "SUB":
      is_sub = True
    if type(item[1]) == str and item[1].isdigit():
      player_name = item[2].replace('\u3000', '').split('  （', 1)[0].replace(' ', '')
      app = 0
      if not is_sub:
        app = 1
      elif player_name in away_sub_list:
        app = 1

      if player_name in team_info[name_away_team].keys():
        base_app = team_info[name_away_team][player_name][0]
        base_goal = team_info[name_away_team][player_name][1]
        team_info[name_away_team][player_name] = [base_app+app,base_goal]
      else:
        team_info[name_away_team][player_name] = [app,0]
  
  for item in away_goal_list:
    if item == 'オウンゴール':
      pass
    else:
      base_info = team_info[name_away_team][item]
      update_base_info = [base_info[0], base_info[1] + 1]
      team_info[name_away_team][item] = update_base_info

  # debug_counter = 0
  # for df in dfs:
  #   debug_counter += 1
  #   print(str.format("Counter: {}, TABLE: {}", debug_counter, df))

with open('kyushuu.csv', 'w', newline="", encoding='utf-8') as csv_file:  
    writer = csv.writer(csv_file)
    for team_name, value in team_info.items():
      for player_name, value2 in value.items():
       writer.writerow([player_name, team_name, value2[0], value2[1]])
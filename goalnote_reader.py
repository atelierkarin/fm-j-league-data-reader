import league_html_reader as r
import csv

# Goalnoteのページをそのまま読み込む、例は四国リーグ
x = list(range(59031, 59087))
urls = [("https://www.goalnote.net/detail-schedule-game.php?tid=9936&sid=" + str(i)) for i in x]

team_info = {"FC徳島": {}, "光洋シーリングテクノ": {}, "新商クラブ": {}, "llamas高知FC": {}, "多度津クラブ": {}, "アルヴェリオ高松": {}}

for url in urls:

  print("Reading {}...".format(url))

  home_team, away_team, home_team_full_list, away_team_full_list = r.get_league_data(url)

  if home_team in team_info.keys():
    for sq, info in home_team_full_list.items():
      player_name = info[0]
      if player_name in team_info[home_team]:
        team_info[home_team][player_name][0] += 1
        team_info[home_team][player_name][1] += info[1]
      else:
        team_info[home_team][player_name] = [1,info[1]]

  if away_team in team_info.keys():
    for sq, info in away_team_full_list.items():
      player_name = info[0]
      if player_name in team_info[away_team]:
        team_info[away_team][player_name][0] += 1
        team_info[away_team][player_name][1] += info[1]
      else:
        team_info[away_team][player_name] = [1,info[1]]

with open('shikoku.csv', 'w', newline="", encoding='utf-8') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in team_info.items():
       writer.writerow([key, value])
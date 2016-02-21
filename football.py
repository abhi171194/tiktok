import requests
from pprint import pprint
import json
host="http://api.football-data.org"    
year=input("Which season year to know starting from 2013 till 2016?")   # query of year
season="/v1/soccerseasons/"
soc_season=season+"?season="+str(year)
url=host+soc_season
r=requests.get(url)          # json object as j_season or j_table or j_player
j_season=json.loads(r.content)     
league={}
caption={}
i=1
for item in j_season:
    del item['_links']
    league[i]=item['league']
    caption[i]=item['caption']
    i=i+1
print (j_season)    
# print (caption)
'''
sea=input("which league to know ?")     # query of league
sea_id=j_season[sea-1]['id']                  #Got the season id in sea_id
sea_table=host+season+str(sea_id)+"/leagueTable"
table1=requests.get(sea_table)
j_table=json.loads(table1.content)
sea_table=[]
player_link={}
teams_name={}                          # dictionary of index : name
if 'error' in j_table:
    print (j_table['error'])
    
else:    
    #for item in j_team['teams']:
    matchday=j_table['matchday']
    i=0
    for item in j_table['standing']:
        sea_table.append({'rank':item['position'],'team':item['teamName'],'Game_played':item['playedGames'],'Won':item['wins'],'Draw':item['draws'],
                      'Loss':item['losses'],'Goal_Scored':item['goals'],'Goals_Against':item['goalsAgainst'],'Goals_Diff':item['goalDifference'],
                      'Points':item['points']})
        teams_name[i]=item['teamName']
        player_link[i]=item['_links']['team']['href']
        i=i+1
print (teams_name)                              # query of team
team_id=input("Enter the number showing before team name to enquire team players data?")            
player_url=player_link[team_id]+"/players"
player1=requests.get(player_url)
j_player=json.loads(player1.content)
'''



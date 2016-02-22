# 1 localhost/footseason/year
# 2 localhost/footseason/season_id/leaguetable
# 3 localhost/footteam/team_id/playerinfo
from flask import Flask,jsonify
from pprint import pprint
app= Flask(__name__)
import requests
from pprint import pprint
import json
 
    
@app.route('/',methods=['GET'])
def get_task():
    #return jsonify({'tasks':tasks})
    return jsonify(Info='football')

@app.route('/footseason/<string:year>',methods=['GET'])
def season(year):
    host="http://api.football-data.org"
    season="/v1/soccerseasons/"
    url_season=host+season+"?season="+year
    
    r=requests.get(url_season,headers = { 'X-Auth-Token':'649ae96933574e51a97ef5dcca3b6340', 'X-Response-Control': 'minified' })
    j_season=json.loads(r.content)
    if 'error' in j_season or len(j_season)==0 :
        return jsonify({'Seasons':'No Data present Enter year from 2013 to 2016'}) 
    return jsonify({'Seasons':j_season})

@app.route('/footseason/<string:season_id>/leaguetable',methods=['GET'])
def season_table(season_id):
    host="http://api.football-data.org"
    table="/v1/soccerseasons/"+season_id+"/leagueTable"
    url_table=host+table
    r=requests.get(url_table,headers = { 'X-Auth-Token':'649ae96933574e51a97ef5dcca3b6340'})
    j=json.loads(r.content)
    sea_table=[]
    if 'error' in j:
        return jsonify(j)
    for item in j['standing']:

        s=str(item['_links']['team']['href']).replace("http://api.football-data.org/v1/teams/","")
        sea_table.append({'Team_id':s,'rank':item['position'],'team':item['teamName'],'Game_played':item['playedGames'],'Won':item['wins'],'Draw':item['draws'],
                      'Loss':item['losses'],'Goal_Scored':item['goals'],'Goals_Against':item['goalsAgainst'],'Goals_Diff':item['goalDifference'],
                      'Points':item['points']})
        
    return jsonify({'PointsTable':sea_table})

@app.route('/footteam/<string:team_id>/playerinfo',methods=['GET'])
def team_player(team_id):
    url="http://api.football-data.org/v1/teams/"+team_id+"/players"
    r=requests.get(url,headers = { 'X-Auth-Token':'649ae96933574e51a97ef5dcca3b6340','X-Response-Control':  'minified'})
    j=json.loads(r.content)
    if 'error' in j:
        return jsonify(j)
    
    return jsonify({'Team_players_info':j})


if __name__== '__main__':
    app.run(port=100)

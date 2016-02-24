from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth
import mysql.connector
import requests
import json
from bs4 import BeautifulSoup
import time
app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

conn = mysql.connector.connect(user="root",password='',host='127.0.0.1',database='sports')


@auth.get_password
def get_password(username):
    cur = conn.cursor()
    cur.execute('SELECT `username`, `password` FROM `login`')
    rv = cur.fetchall()
    for abc in rv:
        if username == abc[0]:
         return abc[1]
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/')
def ho():
    return jsonify({"registration" : "/register/username/password"})

@app.route('/register/<string:username>/<string:password>')
def reg(username,password):
    cur = conn.cursor()
    cur.execute("SELECT * FROM login WHERE username = '" + username + "'")
    ry = cur.fetchall()
    if(len(ry)!=0):
        return make_response(jsonify( { 'error': 'username already exist' } ), 409)
    else:
     cur.execute("INSERT INTO login VALUES ( '" + username + "','" + password + "')")
     conn.commit()
     return jsonify({"accepted" : username})




@app.route('/footseason/<string:year>',methods=['GET'])   #
@auth.login_required
def season(year):
    host="http://api.football-data.org"
    season="/v1/soccerseasons/"
    url_season=host+season+"?season="+year

    cur = conn.cursor()
    cur.execute('SELECT `id`, `caption`, `currentmatchday`, `lastupdated`, `league`, `numberOfGames`, `numberOfMatchdays`, `numberOfTeams`, `year` FROM `leaguesinfo` WHERE year = ' + year)
    rv = cur.fetchall()
    str1 = ""
    if(len(rv)!=0):
     sea_table2=[]
     for abc in rv:
      sea_table2.append({"id":abc[0], "caption":abc[1], "currentmatchday":abc[2], "lastUpdated":abc[3], "league":abc[4], "numberOfGames":abc[5], "numberOfMatchdays":abc[6], "numberOfTeams":abc[7], "year":abc[8], })
     cur.execute("UPDATE leaguesinfo SET count = count+1 WHERE year = " + year)
     return jsonify({'SeasonTable':sea_table2})
    else:
        r=requests.get(url_season,headers = { 'X-Auth-Token':'649ae96933574e51a97ef5dcca3b6340', 'X-Response-Control': 'minified' })
        j_season=json.loads(r.content)
        if 'error' in j_season or len(j_season)==0 :
          return jsonify({'Seasons':'No Data present Enter year from 2013 to 2016'})

        cur.execute("SELECT COUNT(*) FROM leaguesinfo")
        rs = cur.fetchone()

        if rs[0]>25:
            cur.execute("SELECT COUNT(*) FROM leaguesinfo having MAX(count)")
            rs1 = cur.fetchone()
            if(rs1[0]>18):
               cur.execute("""DELETE FROM leaguesinfo WHERE count = ( SELECT mino
         FROM
           ( SELECT MIN(count) AS mino
             FROM leaguesinfo
           ) AS tmp
        )""")


        for abc2 in j_season:
            cur = conn.cursor()
            cur.execute("INSERT INTO leaguesinfo VALUES ( '" + str(abc2["caption"]) + "'," + "32" + "," + str(int(abc2["id"])) + ",'" + str(abc2["lastUpdated"]) + "','" + str(abc2["league"]) + "'," + str(int(abc2["numberOfGames"])) + "," + str(int(abc2["numberOfMatchdays"])) + "," + str(int(abc2["numberOfTeams"])) + "," + str(int(abc2["year"])) + "," + "1" + ",'" + str(time.strftime("%Y/%m/%d")) + str(time.strftime("%H:%M:%S")) + "')" )
            conn.commit()

            #print  str(abc["caption"]) + "`," + str(int(abc["currentMatchday"])) + "," + str(int(abc["id"])) + ",`" + str(abc["lastUpdated"]) + "`,`" + str(abc["league"]) + "`," + str(int(abc["numberOfGames"])) + "," + str(int(abc["numberOfMatchdays"])) + "," + str(int(abc["numberOfTeams"])) + "," + str(int(abc["year"]))
            #str1 = "INSERT INTO leaguesinfo VALUES ( `" + str(abc["caption"]) + "`," + str(int(abc["currentMatchday"])) + "," + str(int(abc["id"])) + ",`" + str(abc["lastUpdated"]) + "`,`" + str(abc["league"]) + "`," + str(int(abc["numberOfGames"])) + "," + str(int(abc["numberOfMatchdays"])) + "," + str(int(abc["numberOfTeams"])) + "," + str(int(abc["year"])) + ")"

            #cur.execute(str1)
            #conn.commit()

        return jsonify({'Seasons':j_season})

@app.route('/footseason/<string:season_id>/leaguetable',methods=['GET'])    # shows league table
@auth.login_required
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

host="https://www.youtube.com/results?search_query="

@app.route('/youtube_search/<string:search>',methods=['GET'])
@auth.login_required
def club_info(search):


    search=search.replace("_","+")
    url=host+search       #"&page="+page
    r=requests.get(url)
    soup=BeautifulSoup(r.content)
    s=soup.find_all("h3",{"class":"yt-lockup-title "})
    list1=[]
    ab2=[]
    cur = conn.cursor()
    cur.execute("SELECT * FROM searchinfo WHERE searched = '" +  search + "'")
    rg = cur.fetchall()
    if(len(rg)!=0):
        for links in rg:
         ab2.append({"Video_name":links[1],"link":links[4],"Duration":links[5]})
         cur.execute("UPDATE searchinfo SET count = count+1 WHERE searched = '" + search + "'")
        return jsonify({'List_complete_top_5':ab2})
    else:
     print "here"
     cur.execute("SELECT COUNT(*) FROM searchinfo ")
     rf = cur.fetchone()
     print rf[0]
     if(rf[0]>50):
         cur.execute("""SELECT searched FROM searchinfo WHERE count = ( SELECT mino
         FROM
           ( SELECT MIN(count) AS mino
             FROM searchinfo
           ) AS tmp
         )""")
         rj = cur.fetchone()
         cur.execute("DELETE FROM searchinfo where searched = '" + rj[0] + "'")
         conn.commit()
     ab=[]
     for item in s:
        li=item.find_all("a")
        dur=str(item.find_all("span")[0].text)
        st=str(li[0].get("href"))
        st="https://www.youtube.com"+st
        title=li[0].text
        list1.append({"Video_name":title,"link":st,"Duration":dur})

    t=1
    for a in list1:
        if(t<6):
            ab.append(a)
            t+=1
        else:
            break
    for v in ab:
      cur.execute("INSERT INTO searchinfo VALUES ( '" + search + "','" + v["Video_name"] +  "','" + str(time.strftime("%Y/%m/%d")) + str(time.strftime("%H:%M:%S")) + "'," + '1' + ",'" + str((v["link"])) + "','" + str(v["Duration"]) + "')")

    conn.commit()
    return jsonify({'List_complete_top_5':ab})


@app.route('/foot1',methods=['GET'])
@auth.login_required
def get_foot():
    url="http://www.football365.com/top-story/page/1"
    r=requests.get(url)
    soup=BeautifulSoup(r.content)
    c=soup.find_all("ul",{"class":"articleList__list"})[0].contents
    li=[]
    d1=[]
    for item in c:
        if str(item)!= '\n':
            li.append(item)
    i=1
    for item in li:
        link=str(item.a['href'])  # str if no unicode error .anchor tag ["attribute_key"] to get value
        headline=item.h3.text
        d1.append({"Index":i,"heading":headline,"link":link})
        i+=1
    t=1
    d2=[]
    for a in d1:
        if(t<6):
            d2.append(a)
            t+=1
    return jsonify({'News_Feed':d2})

@app.route('/foot2/<int:id_>',methods=['GET'])
@auth.login_required
def get_detail(id_):
    url="http://www.football365.com/top-story/page/1"
    r=requests.get(url)
    soup=BeautifulSoup(r.content)
    c=soup.find_all("ul",{"class":"articleList__list"})[0].contents
    li=[]
    d1=[]
    for item in c:
        if str(item)!= '\n':
            li.append(item)
    i=1
    for item in li:
        link=str(item.a['href'])  # str if no unicode error .anchor tag ["attribute_key"] to get value
        headline=item.h3.text
        d1.append({"Index":i,"heading":headline,"link":link})
        i+=1

    link1=d1[id_-1]['link']
    r1=requests.get(link)
    soup1=BeautifulSoup(r1.content)
    data=soup1.find_all('section',{'class':'article__body'})[0]
    list1=data.find_all("p")
    list2=[]
    j=1
    for item in list1:
        txt=item.text
        txt=txt.replace("\u","")
        list2.append({'Para'+str(j):txt})
        j+=1
    return jsonify({"Latest_News_detail":list2})




if __name__ == "__main__":
 app.run(debug=True, port=5000)
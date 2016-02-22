import requests

from flask import Flask,jsonify
app= Flask(__name__)
from pprint import pprint
import json
from bs4 import BeautifulSoup

@app.route('/',methods=['GET'])
def get_youtube():
    #return jsonify({'tasks':tasks})
    return jsonify(Infotat='Youtube')

# NOT WORKING /FOOTBALLNEWS  but    WORKS IN NEWS.PY UNDER LOCALHOST/FOOT
@app.route('/f_news',methods=['GET'])
def get_news():
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
    return jsonify({'News_Feed':d1})
    


# Search using word1_word2
@app.route('/youtube_search/<string:search>',methods=['GET'])
def club_info(search):
    search=search.replace("_","+")
    host="https://www.youtube.com/results?search_query="
    url=host+search       #"&page="+page
    r=requests.get(url)
    sleep(1)
    soup=BeautifulSoup(r.content)
    s=soup.find_all("h3",{"class":"yt-lockup-title "})
    list1=[]
    
    for item in s:
        li=item.find_all("a")
        dur=str(item.find_all("span")[0].text)
        st=str(li[0].get("href"))
        st="https://www.youtube.com"+st
        title=li[0].text
        list1.append({"Video_name":title,"link":st,"Duration":dur})
    return jsonify({'List_complete':list1})



if __name__== '__main__':
    #app.debug=True
    app.run(port=100)

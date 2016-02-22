import requests

from flask import Flask,jsonify
app= Flask(__name__)
from pprint import pprint
import json
from bs4 import BeautifulSoup

@app.route('/',methods=['GET'])
def get_task():
    #return jsonify({'tasks':tasks})
    return jsonify(Info='football')


host="https://www.youtube.com/results?search_query="
# Search using word1_word2
@app.route('/youtube_search/<string:search>',methods=['GET'])
def club_info(search):
    
    
    search=search.replace("_","+")
    url=host+search       #"&page="+page
    r=requests.get(url)
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

import requests
from flask import Flask,jsonify
app= Flask(__name__)
from pprint import pprint
import json
from bs4 import BeautifulSoup


@app.route('/foot',methods=['GET'])
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
    return jsonify({'News_Feed':d1})

@app.route('/foot/<int:id_>',methods=['GET'])
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

if __name__== '__main__':
    #app.debug=True
    app.run(port=50)
    

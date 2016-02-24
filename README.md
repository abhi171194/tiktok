# Football updates API

Prerequistes
- it uses MySQL , so a MySQL server should be present with username = root and password = ""
- database name is sports
- it consist of 3 tables named leaguesinfo,login,searchinfo 
- leaguesinfo has 11 coloumns caption,currentmatchday,id,lastupdated,league,numberOfGames
  numberOfMatchdays,numberOfTeams,year,count,lastadded - *used for caching league info
- login has 2 coloumns username and password
- searchinfo has  6 coloumns searched,name,lastsearched,count,link,duration

INFORMATION
- it has a single file named sportsapi which runs on 127.0.0.1 server 
- Aunthetication by the client must be provided in the headers as username and password
- It gives info about different leagues around the world,league table of that league  
- It gives link,duration,title of youtube videos related to keyword given by user. 
- It gives newsheadlines and link to get detailed info about that news.
- Selecting the reqd id of link , it provides the detailed description of th headline 
- Involves use of web APIs and web scraping with BeautifulSoup library in python.
- the Api cannot be accessed by a browser. It can only be accessed through Postman or by using the Api in an app and 
  sending headers
- REGISTRATION of a user facility is also provided which can be done through browser
## API Calls
<> denotes entry by user 

**/register/yourusername/yourpassword**
- enter the username and password to register yourself in the above yourusername and yourpassword
 
**/footseason/<year>**
- seasonInfo
- Displays different leagues in the enquired year
- information of 2 years is cached. if another new distinct query is made , then information about one of the year is deleted .
- cache algorthim used is LFU(Least Frequently Used ) . so all the entries that are least used are deleted when stored data exceeds. 

**/footseason/<season id>/leaguetable**
- LeagueTable of the enquired league ordered by ranks of team in increasing order (1,2,3 and so on)


**/youtube_search/<Word_to_be_searched>**
- YouTube Search  
- It displays video's[link,duration,title] of Top 5 search results 
- searches are cached. if another new distinct query is made , then it checks if the required storage capacity exceeds or not.
- if yes it deletes an entry using LFU algorithim else it saves the entry.
- the cached memory stores the link, duration and name of the video item.
- cache algorthim used is LFU(Least Frequently Used ) . so all the entries that are least used are deleted when stored data exceeds. 


**/foot1**
- It gives most viral NewsHeadlines and link to know detailed information about that headlines 

**/foot2/<headline id>**
- It gives detailed information about enquired headline
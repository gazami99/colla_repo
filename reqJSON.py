# reqJSON.py 

import pandas as pd
import requests
import xmltodict # xml을 json으로 변환


class ServerManager:

    def __init__(self,url,params):
        
        self.response = requests.get(url, params=params)
        self.urlCheck = (self.response.status_code == 200)   # 200 이면  요청한 url 링크가 정상접속 
    
    def toDataFrame(self):
        
        tmp = xmltodict.parse(self.response.text)
        
        return pd.DataFrame.from_dict(tmp["response"]["body"]["items"]["item"])



url = 'http://apis.data.go.kr/1352000/ODMS_COVID_05/callCovid05Api'
params ={'serviceKey' : '8a9K+8YsLdMkCpBZbqqksp85xu/d2dmUSaw3tamfh9QDthpu9xkpYsTN4D0VZCUjq7G/jBPzUesPOT3EhzdynQ==', 'pageNo' : '1', 'numOfRows' : '500', 'apiType' : 'json', 'create_dt' : '2022-01-08' }

    
a = ServerManager(url,params)

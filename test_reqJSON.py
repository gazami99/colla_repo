#test_reqJSON.py
from reqJSON import ServerManager

def test_run_stuff():
    url = 'http://apis.data.go.kr/1352000/ODMS_COVID_05/callCovid05Api'
    params ={'serviceKey' : '8a9K+8YsLdMkCpBZbqqksp85xu/d2dmUSaw3tamfh9QDthpu9xkpYsTN4D0VZCUjq7G/jBPzUesPOT3EhzdynQ==', 'pageNo' : '1', 'numOfRows' : '500', 'apiType' : 'json', 'create_dt' : '2022-01-08' } 
    result = ServerManager(url,params)
    
    assert result.urlCheck == True

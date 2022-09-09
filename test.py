import json
import pandas as pd
import requests
import xmltodict # xml을 json으로 변환

url = 'http://apis.data.go.kr/1352000/ODMS_COVID_05/callCovid05Api'
params ={'serviceKey' : '8a9K+8YsLdMkCpBZbqqksp85xu/d2dmUSaw3tamfh9QDthpu9xkpYsTN4D0VZCUjq7G/jBPzUesPOT3EhzdynQ==', 'pageNo' : '1', 'numOfRows' : '500', 'apiType' : 'json', 'create_dt' : '2022-01-08' }
response = requests.get(url, params=params)
temp1 = xmltodict.parse(response.text)
json_dump = json.dumps(temp1)
json_body = json.loads(json_dump)
df = pd.DataFrame.from_dict(json_body["response"]["body"]["items"]["item"])
df.columns = ['확진자수','확진율', '등록일자', '치명율', '사망자수', '사망률', '구분명']
# print(json_body["response"]["body"]["items"]["item"])

df = pd.DataFrame.from_dict(json_body["response"]["body"]["items"]["item"])
print(df.sort_values(by="gubun"))
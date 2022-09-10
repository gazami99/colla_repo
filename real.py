import json
import pandas as pd
import requests
import xmltodict # xml을 json으로 변환
import pymysql
 # mysql과 파이썬이 소통할 수 있게 하는 라이브러리

# pymysql사용해서 Db에 등록일자가 등록되어 있으면 db에서 select하게 만약 없으면 api활용해서 받아오고 저장한다음 select하게?

# pk값은 auto incresment로 그냥 주고 등록일자로 검색하게 하는게 좋을라나?

# 조회할 날짜 변수 나중에 flask로 웹에서 변수 받아서 넣는것으로 바꿀예정 리턴값으로 데이터프레임 받아옴
def getCovidinfo(date):
    url = 'http://apis.data.go.kr/1352000/ODMS_COVID_05/callCovid05Api'
    params ={'serviceKey' : '8a9K+8YsLdMkCpBZbqqksp85xu/d2dmUSaw3tamfh9QDthpu9xkpYsTN4D0VZCUjq7G/jBPzUesPOT3EhzdynQ==', 'pageNo' : '1', 'numOfRows' : '500', 'apiType' : 'json', 'create_dt' : date }
    response = requests.get(url, params=params)
    temp1 = xmltodict.parse(response.text)
    json_dump = json.dumps(temp1)
    json_body = json.loads(json_dump)
    df = pd.DataFrame.from_dict(json_body["response"]["body"]["items"]["item"])
    df.columns = ['확진자수','확진율', '등록일자', '치명율', '사망자수', '사망률', '구분명']
    return df
# print(getCovidinfo('2022-05-01').iloc[0][0])
# df = getCovidinfo('2022-05-01')

# datas = [
#     [int(df.iloc[0][0]), int(df.iloc[0][1]), df.iloc[0][2], int(df.iloc[0][3]), int(df.iloc[0][4]), int(df.iloc[0][5]), df.iloc[0][6]],
#     [int(df.iloc[1][0]), int(df.iloc[1][1]), df.iloc[1][2], int(df.iloc[1][3]), int(df.iloc[1][4]), int(df.iloc[1][5]), df.iloc[1][6]]
# ]

# print(datas)
# Db에 저장하는 함수
# 반복문 써야되기때문에 pandas의 to_sql을 쓸 예정

def loadInfo():
    df = getCovidinfo('2022-05-01')
    datas = [
        [int(df.iloc[0][0]), int(df.iloc[0][1]), df.iloc[0][2], int(df.iloc[0][3]), int(df.iloc[0][4]), int(df.iloc[0][5]), df.iloc[0][6]],
        [int(df.iloc[1][0]), int(df.iloc[1][1]), df.iloc[1][2], int(df.iloc[1][3]), int(df.iloc[1][4]), int(df.iloc[1][5]), df.iloc[1][6]]
    ]
	
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS covidinfo (
                                             
 	 confcase INT(11) NOT NULL,                        
 	 confcaseRate VARCHAR(20) NULL,                       
 	 creaeDt DATE NULL,                                   
 	 criticalRate DECIMAL(7,2) NULL,                                 
 	 death  INT(11) NULL,
	 deathRate DECIMAL(7,2) NULL,
	 gubun VARCHAR(255) NULL

	 ) default character set utf8 collate utf8_general_ci
    '''
	
    sql = "insert into covidinfo(confcase, confcaseRate, creaeDt, criticalRate, death, deathRate, gubun) values (%s, %s, %s, %s, %s, %s, %s)"
    with pymysql.connect(host='127.0.0.1', port=3306, user='bigdata', password='bigdata', db='test', charset='utf8') as connection:
        with connection.cursor() as cursor:
            IsConn = connection.open
            cursor.execute(create_table_sql)
            cursor.executemany(sql, datas)
            connection.commit()
            
    return IsConn
         

         


import json
import pandas as pd
import requests
import xmltodict # xml을 json으로 변환
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib ## 이거랑 밑에거는 맥환경이랑 한글 폰트 설정때문에 한거
from matplotlib import rc
import numpy as np
from dbutil import getConnect
import pymysql

# 메인 함수 날짜를 받아서 해당 날짜 정보가 db에 있으면 db에서 없으면 api에서 데이터를 받아와 데이터프레임으로 리턴
# 구분값 디폴트는 전체조회 만약 다른 정보가 들어오면 해당 컬럼만 선택해서 출력
def main_pipeline(date, gubun="전체조회"):
    if gubun == "전체조회":
        if check_date(date):
            result = covid_info_db(date)
        else:
            result = covid_info_api(date)
            if result.empty:
                return result
            load_info(result)
    else:
        if check_date(date):
            result = covid_info_db(date)
            result = result[result['gubun']==gubun]
        else:
            result = covid_info_api(date)
            if result.empty:
                return result
            load_info(result)
            result = result[result['gubun']==gubun]
    return result

# 데이터 베이스에 해당 날짜 데이터가 있는지 확인하는 함수
def check_date(date):
    try:
        sql = 'select create_dt from covid_info where create_dt =%s'
        with pymysql.connect(host='127.0.0.1', port=3306, user='bigdata', password='bigdata', db='test', charset='utf8') as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, (date, ))  
                result = cursor.fetchone()
    except Exception as e:
        print(e)
    return result


# 리턴값으로 데이터프레임 받아옴
# 구분값으로 자동 정렬
def covid_info_api(date):
    url = 'http://apis.data.go.kr/1352000/ODMS_COVID_05/callCovid05Api'
    params ={'serviceKey' : '8a9K+8YsLdMkCpBZbqqksp85xu/d2dmUSaw3tamfh9QDthpu9xkpYsTN4D0VZCUjq7G/jBPzUesPOT3EhzdynQ==', 'pageNo' : '1', 'numOfRows' : '500', 'apiType' : 'json', 'create_dt' : date }
    response = requests.get(url, params=params)

    temp1 = xmltodict.parse(response.text)
    json_dump = json.dumps(temp1)
    json_body = json.loads(json_dump)
    temp2 = []
    if 'items' in json_body["response"]["body"]:
        df = pd.DataFrame.from_dict(json_body["response"]["body"]["items"]["item"])

        df = df.sort_values(by=['gubun'])
        # df.columns = ['확진자수','확진율', '등록일자', '치명율', '사망자수', '사망률', '구분명']
        df.columns = ['conf_case','conf_caserate', 'create_dt', 'critical_rate', 'death', 'death_rate', 'gubun']
        # print(df[['critical_rate']])
        if df['critical_rate'][1][-1] =='%':
            for a in df['critical_rate']:
                temp2.append(int(a[2:-1]))
            df['critical_rate'] = temp2
        return df    
    else:
        return pd.DataFrame()



# 특정 날짜 DB에 저장된 정보 가지고 오기
def covid_info_db(date):
    try:
        sql = 'select * from covid_info where create_dt =%s'
        with pymysql.connect(host='127.0.0.1', port=3306, user='bigdata', password='bigdata', db='test', charset='utf8') as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, (date, ))  
                result = cursor.fetchall()
                df = pd.DataFrame(result, columns=['temp','conf_case','conf_caserate', 'create_dt', 'critical_rate', 'death', 'death_rate', 'gubun'])
                df.drop('temp', axis=1, inplace=True)
    except Exception as e:
        print(e)
    return df

# df통채로 db에 저장
def load_info(df):
    # df = getCovidinfo('2022-05-01')
    try:
        db_conn = getConnect()
        conn = db_conn.connect()
        df.to_sql(name="covid_info", con=db_conn, if_exists='append', index=False)
    except Exception as e:
        print(e)
    finally:
        conn.close()

# 시작 날짜와 끝 날짜 가지고 중간 포함해서 리스트에 넣어서 리턴
def date_range(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    
    dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end-start).days+1)]
    return dates


# 확진자수 일별 라인 그래프 그리기
def draw_line_chart(df):
    matplotlib.pyplot.switch_backend('Agg') 
    rc('font', family='Malgun Gothic') 			
    plt.rcParams['axes.unicode_minus'] = False 

    df = df[(df['gubun'] == '남성')|(df['gubun'] == '여성')]
    df['conf_case'] = df['conf_case'].astype('int')
    df = df.groupby('create_dt').sum()
    plt.figure(figsize=(20,10))
    plt.plot(df.index, df['conf_case'], marker='o')
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.grid(visible=True, linestyle='--')
    plt.title('일자별 확진자수', fontsize = 20)
    plt.show()
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plt.savefig('./static/img/line_covid.png')
    result = './static/img/line_covid.png'
    return result

# 사망자수 일별 라인 그래프 그리기
def draw_death_line_chart(df):
    matplotlib.pyplot.switch_backend('Agg') 
    rc('font', family='Malgun Gothic') 			
    plt.rcParams['axes.unicode_minus'] = False 

    df = df[(df['gubun'] == '남성')|(df['gubun'] == '여성')]
    df['death'] = df['death'].astype('int')
    df = df.groupby('create_dt').sum()
    plt.figure(figsize=(20,10))
    plt.plot(df.index, df['death'], marker='o')
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.grid(visible=True, linestyle='--')
    plt.title('일자별 사망자수', fontsize = 20)
    plt.show()
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plt.savefig('./static/img/death_line_covid.png')
    result = './static/img/death_line_covid.png'
    return result

# 연령별 확진자수 막대그래프 그리기
def draw_age_chart(df):
    matplotlib.pyplot.switch_backend('Agg') 
    rc('font', family='Malgun Gothic') 	 			## 이 두 줄을 
    plt.rcParams['axes.unicode_minus'] = False 
    
    age_df = df[(df['gubun'] != '남성') & (df['gubun'] != '여성')]
    age_df['conf_case'] = age_df['conf_case'].astype('int')
    age_df = age_df.groupby('gubun').sum()
    ratio = age_df['conf_case']
    labels = age_df.index
    x = np.arange(len(age_df))
    fig = plt.figure(figsize = (10,10))
    cmap = plt.get_cmap("tab20c")
    colors = cmap(np.array([1, 2, 3, 4, 5, 6, 7, 8]))
    plt.bar(x, ratio, color = colors)
    plt.xticks(x, labels, fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.grid(visible=True, linestyle='--')
    plt.title('연령별 확진자수', fontsize = 20)
    plt.show()
    plt.savefig('./static/img/age_covid.png')
    result = './static/img/age_covid.png'
    return result

# 연령별 사망자수 막대그래프 그리기
def draw_death_age_chart(df):
    matplotlib.pyplot.switch_backend('Agg') 
    rc('font', family='Malgun Gothic') 	 			 
    plt.rcParams['axes.unicode_minus'] = False 
    
    age_df = df[(df['gubun'] != '남성') & (df['gubun'] != '여성')]
    age_df['death'] = age_df['death'].astype('int')
    age_df = age_df.groupby('gubun').sum()
    ratio = age_df['death']
    labels = age_df.index
    x = np.arange(len(age_df))
    fig = plt.figure(figsize = (10,10))
    cmap = plt.get_cmap("tab20c")
    colors = cmap(np.array([1, 2, 3, 4, 5, 6, 7, 8]))
    plt.bar(x, ratio, color = colors)
    plt.xticks(x, labels, fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.grid(visible=True, linestyle='--')
    plt.title('연령별 사망자수', fontsize = 20)
    plt.show()
    plt.savefig('./static/img/death_age_covid.png')
    result = './static/img/death_age_covid.png'
    return result

# 확진자수 성비 파이그래프 그리기
def draw_gender_chart(df):
    matplotlib.pyplot.switch_backend('Agg') 
    rc('font', family='Malgun Gothic') 			 
    plt.rcParams['axes.unicode_minus'] = False 
    
    gender_df = df[(df['gubun'] == '남성') | (df['gubun'] == '여성')]
    gender_df['conf_case'] = gender_df['conf_case'].astype('int')
    gender_df = gender_df.groupby('gubun').sum()
    ratio = gender_df['conf_case']
    labels = gender_df.index
    explode = [0.05, 0.05]
    fig = plt.figure(figsize = (10,10))
    cmap = plt.get_cmap("tab20c")
    colors = cmap(np.array([1, 5]))
    plt.pie(ratio, labels=labels, autopct='%.1f%%', startangle=260, counterclock=False, colors = colors, explode = explode, shadow=True, textprops={'fontsize': 16})
    plt.title('확진자수 성비', fontsize = 20)
    plt.show()
    plt.savefig('./static/img/gender_covid.png')
    result = './static/img/gender_covid.png'
    return result

# 사망자수 성비 파이그래프 그리기
def draw_death_gender_chart(df):
    matplotlib.pyplot.switch_backend('Agg') 
    rc('font', family='Malgun Gothic') 			 
    plt.rcParams['axes.unicode_minus'] = False 
    
    gender_df = df[(df['gubun'] == '남성') | (df['gubun'] == '여성')]
    gender_df['death'] = gender_df['death'].astype('int')
    gender_df = gender_df.groupby('gubun').sum()
    ratio = gender_df['death']
    labels = gender_df.index
    explode = [0.05, 0.05]
    fig = plt.figure(figsize = (10,10))
    cmap = plt.get_cmap("tab20c")
    colors = cmap(np.array([1, 5]))
    plt.pie(ratio, labels=labels, autopct='%.1f%%', startangle=260, counterclock=False, colors = colors, explode = explode, shadow=True, textprops={'fontsize': 16})
    plt.title('사망자수 성비', fontsize = 20)
    plt.show()
    plt.savefig('./static/img/death_gender_covid.png')
    result = './static/img/death_gender_covid.png'
    return result
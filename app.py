from flask import Flask, request, render_template
from dao import draw_death_age_chart, draw_death_line_chart, main_pipeline, date_range, draw_line_chart, draw_age_chart, draw_gender_chart, draw_death_age_chart, draw_death_line_chart, draw_death_gender_chart
import pandas as pd

app = Flask(__name__)

@app.route("/")
def intro():
    return render_template("new.html")

# 화면에 테이블 출력
@app.route("/infodate", methods=['post'])
def check():
    datemin = request.form.get("datemin")
    datemax = request.form.get("datemax")
    gubun = request.form.get("gubun")
    gubun = gubun.split(",")
    dates = date_range(datemin,datemax)
    df = pd.DataFrame(columns=['conf_case','conf_caserate', 'create_dt', 'critical_rate', 'death', 'death_rate', 'gubun'])
    if '전체조회' in gubun:
        for i in dates:
            temp = main_pipeline(i)
            if(temp.empty):
                return '{"test" : "없음"}'
            df = df.append(temp)
    else:
        for i in dates:
            for a in gubun:
                temp = main_pipeline(i, a)
                if(temp.empty):
                    return '{"test" : "없음"}'
                df = df.append(temp)
    
    result = df.to_json(orient='records')
    return result 

# 차트 생성 및 저장하고 출력
@app.route("/chart", methods=['post'])
def chart():
    chart = request.form.get("chart")
    datemin = request.form.get("datemin")
    datemax = request.form.get("datemax")
    dates = date_range(datemin, datemax)
    df = pd.DataFrame(columns=['conf_case','conf_caserate', 'create_dt', 'critical_rate', 'death', 'death_rate', 'gubun'])
    for i in dates:
        temp = main_pipeline(i)
        if(temp.empty):
            return '{"test" : "없음"}'
        df = df.append(temp)
    
    if chart == "line1":
        img = draw_line_chart(df)
    elif chart == "line2":
        img = draw_death_line_chart(df)
    elif chart =="bar1":
        img = draw_age_chart(df)
    elif chart =="bar2":
        img = draw_death_age_chart(df)
    elif chart == "pie1":
        img = draw_gender_chart(df)
    elif chart == "pie2":
        img = draw_death_gender_chart(df)
    result = {"url" : img}
    return result

if __name__ == "__main__":
    app.run(debug=True, port=5001)
from flask import Flask, render_template, redirect, url_for
from dateutil.relativedelta import relativedelta
import datetime
from flask import request
from flask_fontawesome import FontAwesome
from flask_restful import reqparse
import os
import re
import pandas as pd

app = Flask(__name__)
fa = FontAwesome(app)
global_result=[]
check=[]

def parse_arg_from_requests(arg, **kwargs):
    parse = reqparse.RequestParser()
    parse.add_argument(arg, **kwargs)
    args = parse.parse_args()
    return args[arg]

# 식단추출페이지
@app.route("/")
def template_test():
    return render_template(
                'index.html',                      #렌더링 html 파일명
                title="Flask Template Test",       #title 텍스트 바인딩1
                my_str="시니어 세대를 위한 건강식단 추천 기능 개발",             #my_str 텍스트 바인딩2
                my_list=[x + 1 for x in range(30)] #30개 리스트 선언(1~30)
            )
@app.route('/result', methods=['POST', 'get'])
def select_diet():
    # gender=parse_arg_from_requests('gender')
    if (request.method=="POST"):
        today = datetime.date.today()
        dayslater = today + datetime.timedelta(days=7)
        dt=datetime.datetime.now()
        days1=dt.weekday()

        gender=request.form['gender']
        age=request.form['result_age']
        # age=66
        height=request.form['height']
        weight=request.form['weight']
        actlevel=request.form['activelevel']

        BMI=int(weight) / (int(height) * int(height))*100*100

        if(gender=='남성'):
            gender=0
        else:
            gender=1

        age=int(age)
        if (age>=75):
            age=2
        elif(age>64 and age<75):
            age=1
        elif(age>49 and age<65):
            age=0

        if (BMI > 30):
            BMI_label = 4
        elif (BMI <= 30 and BMI > 25):
            BMI_label = 3
        elif (BMI <= 25 and BMI > 23):
            BMI_label = 2
        elif (BMI <= 23 and BMI > 18.5):
            BMI_label = 1
        else:
            BMI_label = 0

        if actlevel == '낮음':
            actlevelrate = 1
        elif actlevel == '보통':
            actlevelrate = 2
        elif actlevel == '활발':
            actlevelrate = 3

        check_str=str(2)+str(gender)+str(age)+str(BMI_label)+str(actlevelrate)
        check.append(check_str)
        # check_str=str(0001)
        origin_path = 'D:\고령식단\Final_diet'
        bre_combilist = os.listdir(origin_path + '\Breakfast')
        lun_combilist = os.listdir(origin_path + '\lunch')
        din_combilist = os.listdir(origin_path + '\dinner')

        final_plan_bre = []
        final_plan_lun = []
        final_plan_din = []
        # print(lun_combilist, len(lun_combilist))
        # print(din_combilist, len(din_combilist))
        j = 0
        type1 = []
        f_b = []
        f_l = []
        f_d = []

        for a in range(len(bre_combilist)):
            f = open(origin_path + '\Breakfast' + '\\' + bre_combilist[a] + '\\' + check_str + '.csv', 'r', encoding='utf-8')
            f.readline()
            f_b.append([a, f.readlines()])

        for a in range(len(lun_combilist)):
            f = open(origin_path + '\lunch' + '\\' + lun_combilist[a] + '\\' + check_str + '.csv', 'r', encoding='utf-8')
            f.readline()
            f_l.append([a, f.readlines()])

        for b in range(len(din_combilist)):
            f = open(origin_path + '\dinner' + '\\' + din_combilist[b] + '\\' + check_str + '.csv', 'r', encoding='utf-8')
            f.readline()
            f_d.append([b, f.readlines()])

        while (len(final_plan_bre) < 30):

            for d in range(20):
                if (len(final_plan_bre) < 30):
                    for f in range(len(f_b)):
                        try:
                            final_plan_bre.append(f_b[f][1][d])
                        except:
                            continue
                else:
                    break

        while (len(final_plan_lun) < 30):

            for d in range(20):
                if (len(final_plan_lun) < 30):
                    for f in range(len(f_l)):
                        try:
                            final_plan_lun.append(f_l[f][1][d])
                        except:
                            continue
                else:
                    break

        while (len(final_plan_din) < 30):

            for d in range(20):
                if (len(final_plan_din) < 30):
                    for f in range(len(f_d)):
                        try:
                            final_plan_din.append(f_d[f][1][d])
                        except:
                            continue
                else:
                    break

        df_list_bre = []

        for b in final_plan_bre:
            bsplit = b.split(",")
            dic = {
                "basic": bsplit[0],
                "soup": bsplit[1],
                "main": bsplit[2],
                "side": bsplit[3],
                "sim": bsplit[4],
                "tcal": bsplit[5],
                "protein":bsplit[6],
                "fat":bsplit[7],
                "carbo":bsplit[8],
                "sweet":bsplit[9],
                "Nat":bsplit[18],
            }
            df_list_bre.append(dic)

        df_result_bre = pd.DataFrame(df_list_bre)
        df_list = []
        for b in final_plan_lun:
            bsplit = b.split(",")
            dic = {
                "basic": bsplit[0],
                "soup": bsplit[1],
                "main": bsplit[2],
                "side": bsplit[3],
                "sim": bsplit[4],
                "tcal": bsplit[5],
                "protein":bsplit[6],
                "fat":bsplit[7],
                "carbo":bsplit[8],
                "sweet":bsplit[9],
                "Nat":bsplit[18],
            }
            df_list.append(dic)

        df_result = pd.DataFrame(df_list)

        df_list_din = []

        for b in final_plan_din:
            bsplit = b.split(",")
            dic = {
                "basic": bsplit[0],
                "soup": bsplit[1],
                "main": bsplit[2],
                "side": bsplit[3],
                "sim": bsplit[4],
                "tcal":bsplit[5],
                "protein":bsplit[6],
                "fat":bsplit[7],
                "carbo":bsplit[8],
                "sweet":bsplit[9],
                "Nat":bsplit[18],
            }
            df_list_din.append(dic)

        df_result_din = pd.DataFrame(df_list_din)

        breakfast_final=df_result_bre
        # lunch_final = df_result.drop_duplicates(['basic', 'soup'], keep='first')
        lunch_final = df_result
        dinner_final = df_result_din

        all_result = {}
        days = [0, 1, 2, 3, 4, 5, 6]
        thisweek = []
        preweek = []
        nextweek = []
        for i in range(21):
            if (i < 7):
                thisweek.append({days[i]:
                                     [[breakfast_final.iloc[i]["basic"], breakfast_final.iloc[i]["soup"],
                                       breakfast_final.iloc[i]["main"],
                                       breakfast_final.iloc[i]["side"], breakfast_final.iloc[i]["sim"],
                                       breakfast_final.iloc[i]["tcal"],
                                       breakfast_final.iloc[i]["protein"], breakfast_final.iloc[i]["fat"],
                                       breakfast_final.iloc[i]["carbo"],
                                       breakfast_final.iloc[i]["sweet"], breakfast_final.iloc[i]["Nat"]],
                                      [lunch_final.iloc[i]["basic"], lunch_final.iloc[i]["soup"],
                                       lunch_final.iloc[i]["main"],
                                       lunch_final.iloc[i]["side"], lunch_final.iloc[i]["sim"],
                                       lunch_final.iloc[i]["tcal"],
                                       lunch_final.iloc[i]["protein"], lunch_final.iloc[i]["fat"],
                                       lunch_final.iloc[i]["carbo"],
                                       lunch_final.iloc[i]["sweet"], lunch_final.iloc[i]["Nat"]],
                                      [dinner_final.iloc[i]["basic"], dinner_final.iloc[i]["soup"],
                                       dinner_final.iloc[i]["main"],
                                       dinner_final.iloc[i]["side"], dinner_final.iloc[i]["sim"],
                                       dinner_final.iloc[i]["tcal"],
                                       dinner_final.iloc[i]["protein"], dinner_final.iloc[i]['fat'],
                                       dinner_final.iloc[i]['carbo'],
                                       dinner_final.iloc[i]['sweet'], dinner_final.iloc[i]["Nat"]]]
                                 })
            elif (i >= 7 and i < 14):
                preweek.append({days[i - 7]:
                                    [[breakfast_final.iloc[i]["basic"], breakfast_final.iloc[i]["soup"],
                                      breakfast_final.iloc[i]["main"],
                                      breakfast_final.iloc[i]["side"], breakfast_final.iloc[i]["sim"],
                                      breakfast_final.iloc[i]["tcal"],
                                      breakfast_final.iloc[i]["protein"], breakfast_final.iloc[i]["fat"],
                                      breakfast_final.iloc[i]["carbo"],
                                      breakfast_final.iloc[i]["sweet"], breakfast_final.iloc[i]["Nat"]],
                                     [lunch_final.iloc[i]["basic"], lunch_final.iloc[i]["soup"],
                                      lunch_final.iloc[i]["main"],
                                      lunch_final.iloc[i]["side"], lunch_final.iloc[i]["sim"],
                                      lunch_final.iloc[i]["tcal"],
                                      lunch_final.iloc[i]["protein"], lunch_final.iloc[i]["fat"],
                                      lunch_final.iloc[i]["carbo"],
                                      lunch_final.iloc[i]["sweet"], lunch_final.iloc[i]["Nat"]],
                                     [dinner_final.iloc[i]["basic"], dinner_final.iloc[i]["soup"],
                                      dinner_final.iloc[i]["main"],
                                      dinner_final.iloc[i]["side"], dinner_final.iloc[i]["sim"],
                                      dinner_final.iloc[i]["tcal"],
                                      dinner_final.iloc[i]["protein"], dinner_final.iloc[i]['fat'],
                                      dinner_final.iloc[i]['carbo'],
                                      dinner_final.iloc[i]['sweet'], dinner_final.iloc[i]["Nat"]]]
                                })
            else:
                nextweek.append({days[i - 14]:
                                     [[breakfast_final.iloc[i]["basic"], breakfast_final.iloc[i]["soup"],
                                       breakfast_final.iloc[i]["main"],
                                       breakfast_final.iloc[i]["side"], breakfast_final.iloc[i]["sim"],
                                       breakfast_final.iloc[i]["tcal"],
                                       breakfast_final.iloc[i]["protein"], breakfast_final.iloc[i]["fat"],
                                       breakfast_final.iloc[i]["carbo"],
                                       breakfast_final.iloc[i]["sweet"], breakfast_final.iloc[i]["Nat"]],
                                      [lunch_final.iloc[i]["basic"], lunch_final.iloc[i]["soup"],
                                       lunch_final.iloc[i]["main"],
                                       lunch_final.iloc[i]["side"], lunch_final.iloc[i]["sim"],
                                       lunch_final.iloc[i]["tcal"],
                                       lunch_final.iloc[i]["protein"], lunch_final.iloc[i]["fat"],
                                       lunch_final.iloc[i]["carbo"],
                                       lunch_final.iloc[i]["sweet"], lunch_final.iloc[i]["Nat"]],
                                      [dinner_final.iloc[i]["basic"], dinner_final.iloc[i]["soup"],
                                       dinner_final.iloc[i]["main"],
                                       dinner_final.iloc[i]["side"], dinner_final.iloc[i]["sim"],
                                       dinner_final.iloc[i]["tcal"],
                                       dinner_final.iloc[i]["protein"], dinner_final.iloc[i]['fat'],
                                       dinner_final.iloc[i]['carbo'],
                                       dinner_final.iloc[i]['sweet'], dinner_final.iloc[i]["Nat"]]]
                                 })

        all_result['thisweek']= thisweek
        all_result['preweek']=preweek
        all_result['nextweek']=nextweek
        global_result.append(all_result)
        week='thisweek'
        return render_template('diet_result.html', date=today, date2=dayslater, all_result=all_result, days=days1, week=week, check_str=check_str)
    else:
        today = datetime.date.today()
        dayslater = today + datetime.timedelta(days=7)
        days1 = int(request.args.get('days'))
        check_str = request.args.get('check')
        week=request.args.get('week')
        # check.append(check_str)
        # check_str=str(0001)
        origin_path = 'D:\고령식단\Final_diet'
        bre_combilist = os.listdir(origin_path + '\Breakfast')
        lun_combilist = os.listdir(origin_path + '\lunch')
        din_combilist = os.listdir(origin_path + '\dinner')

        final_plan_bre = []
        final_plan_lun = []
        final_plan_din = []
        # print(lun_combilist, len(lun_combilist))
        # print(din_combilist, len(din_combilist))
        j = 0
        type1 = []
        f_b = []
        f_l = []
        f_d = []

        for a in range(len(bre_combilist)):
            f = open(origin_path + '\Breakfast' + '\\' + bre_combilist[a] + '\\' + check_str + '.csv', 'r', encoding='utf-8')
            f.readline()
            f_b.append([a, f.readlines()])
            f.close()

        for a in range(len(lun_combilist)):
            f = open(origin_path + '\lunch' + '\\' + lun_combilist[a] + '\\' + check_str + '.csv', 'r',
                     encoding='utf-8')
            f.readline()
            f_l.append([a, f.readlines()])
            f.close()

        for b in range(len(din_combilist)):
            f = open(origin_path + '\dinner' + '\\' + din_combilist[b] + '\\' + check_str + '.csv', 'r',
                     encoding='utf-8')
            f.readline()
            f_d.append([b, f.readlines()])
            f.close()

        while (len(final_plan_bre) < 30):

            for d in range(20):
                if (len(final_plan_bre) < 30):
                    for f in range(len(f_b)):
                        try:
                            final_plan_bre.append(f_b[f][1][d])
                        except:
                            continue
                else:
                    break

        while (len(final_plan_lun) < 30):

            for d in range(20):
                if (len(final_plan_lun) < 30):
                    for f in range(len(f_l)):
                        try:
                            final_plan_lun.append(f_l[f][1][d])
                        except:
                            continue
                else:
                    break

        while (len(final_plan_din) < 30):

            for d in range(20):
                if (len(final_plan_din) < 30):
                    for f in range(len(f_d)):
                        try:
                            final_plan_din.append(f_d[f][1][d])
                        except:
                            continue
                else:
                    break

        df_list_bre = []

        for b in final_plan_bre:
            bsplit = b.split(",")
            dic = {
                "basic": bsplit[0],
                "soup": bsplit[1],
                "main": bsplit[2],
                "side": bsplit[3],
                "sim": bsplit[4],
                "tcal": bsplit[5],
                "protein": bsplit[6],
                "fat": bsplit[7],
                "carbo": bsplit[8],
                "sweet": bsplit[9],
                "Nat": bsplit[18],
            }
            df_list_bre.append(dic)

        df_result_bre = pd.DataFrame(df_list_bre)

        df_list = []

        for b in final_plan_lun:
            bsplit = b.split(",")
            dic = {
                "basic": bsplit[0],
                "soup": bsplit[1],
                "main": bsplit[2],
                "side": bsplit[3],
                "sim": bsplit[4],
                "tcal": bsplit[5],
                "protein": bsplit[6],
                "fat": bsplit[7],
                "carbo": bsplit[8],
                "sweet": bsplit[9],
                "Nat": bsplit[18],
            }
            df_list.append(dic)

        df_result = pd.DataFrame(df_list)

        df_list_din = []

        for b in final_plan_din:
            bsplit = b.split(",")
            dic = {
                "basic": bsplit[0],
                "soup": bsplit[1],
                "main": bsplit[2],
                "side": bsplit[3],
                "sim": bsplit[4],
                "tcal": bsplit[5],
                "protein": bsplit[6],
                "fat": bsplit[7],
                "carbo": bsplit[8],
                "sweet": bsplit[9],
                "Nat": bsplit[18],
            }
            df_list_din.append(dic)

        df_result_din = pd.DataFrame(df_list_din)

        breakfast_final = df_result_bre
        # lunch_final = df_result.drop_duplicates(['basic', 'soup'], keep='first')
        lunch_final=df_result
        dinner_final = df_result_din

        all_result = {}
        days = [0, 1, 2, 3, 4, 5, 6]
        thisweek = []
        preweek = []
        nextweek = []
        for i in range(21):
            if (i < 7):
                thisweek.append({days[i]:
                                     [[breakfast_final.iloc[i]["basic"], breakfast_final.iloc[i]["soup"],
                                       breakfast_final.iloc[i]["main"],
                                       breakfast_final.iloc[i]["side"], breakfast_final.iloc[i]["sim"],
                                       breakfast_final.iloc[i]["tcal"],
                                       breakfast_final.iloc[i]["protein"], breakfast_final.iloc[i]["fat"],
                                       breakfast_final.iloc[i]["carbo"],
                                       breakfast_final.iloc[i]["sweet"], breakfast_final.iloc[i]["Nat"]],
                                      [lunch_final.iloc[i]["basic"], lunch_final.iloc[i]["soup"],
                                       lunch_final.iloc[i]["main"],
                                       lunch_final.iloc[i]["side"], lunch_final.iloc[i]["sim"],
                                       lunch_final.iloc[i]["tcal"],
                                       lunch_final.iloc[i]["protein"], lunch_final.iloc[i]["fat"],
                                       lunch_final.iloc[i]["carbo"],
                                       lunch_final.iloc[i]["sweet"], lunch_final.iloc[i]["Nat"]],
                                      [dinner_final.iloc[i]["basic"], dinner_final.iloc[i]["soup"],
                                       dinner_final.iloc[i]["main"],
                                       dinner_final.iloc[i]["side"], dinner_final.iloc[i]["sim"],
                                       dinner_final.iloc[i]["tcal"],
                                       dinner_final.iloc[i]["protein"], dinner_final.iloc[i]['fat'],
                                       dinner_final.iloc[i]['carbo'],
                                       dinner_final.iloc[i]['sweet'], dinner_final.iloc[i]["Nat"]]]
                                 })
            elif (i >= 7 and i < 14):
                preweek.append({days[i - 7]:
                                    [[breakfast_final.iloc[i]["basic"], breakfast_final.iloc[i]["soup"],
                                      breakfast_final.iloc[i]["main"],
                                      breakfast_final.iloc[i]["side"], breakfast_final.iloc[i]["sim"],
                                      breakfast_final.iloc[i]["tcal"],
                                      breakfast_final.iloc[i]["protein"], breakfast_final.iloc[i]["fat"],
                                      breakfast_final.iloc[i]["carbo"],
                                      breakfast_final.iloc[i]["sweet"], breakfast_final.iloc[i]["Nat"]],
                                     [lunch_final.iloc[i]["basic"], lunch_final.iloc[i]["soup"],
                                      lunch_final.iloc[i]["main"],
                                      lunch_final.iloc[i]["side"], lunch_final.iloc[i]["sim"],
                                      lunch_final.iloc[i]["tcal"],
                                      lunch_final.iloc[i]["protein"], lunch_final.iloc[i]["fat"],
                                      lunch_final.iloc[i]["carbo"],
                                      lunch_final.iloc[i]["sweet"], lunch_final.iloc[i]["Nat"]],
                                     [dinner_final.iloc[i]["basic"], dinner_final.iloc[i]["soup"],
                                      dinner_final.iloc[i]["main"],
                                      dinner_final.iloc[i]["side"], dinner_final.iloc[i]["sim"],
                                      dinner_final.iloc[i]["tcal"],
                                      dinner_final.iloc[i]["protein"], dinner_final.iloc[i]['fat'],
                                      dinner_final.iloc[i]['carbo'],
                                      dinner_final.iloc[i]['sweet'], dinner_final.iloc[i]["Nat"]]]
                                })
            else:
                nextweek.append({days[i - 14]:
                                     [[breakfast_final.iloc[i]["basic"], breakfast_final.iloc[i]["soup"],
                                       breakfast_final.iloc[i]["main"],
                                       breakfast_final.iloc[i]["side"], breakfast_final.iloc[i]["sim"],
                                       breakfast_final.iloc[i]["tcal"],
                                       breakfast_final.iloc[i]["protein"], breakfast_final.iloc[i]["fat"],
                                       breakfast_final.iloc[i]["carbo"],
                                       breakfast_final.iloc[i]["sweet"], breakfast_final.iloc[i]["Nat"]],
                                      [lunch_final.iloc[i]["basic"], lunch_final.iloc[i]["soup"],
                                       lunch_final.iloc[i]["main"],
                                       lunch_final.iloc[i]["side"], lunch_final.iloc[i]["sim"],
                                       lunch_final.iloc[i]["tcal"],
                                       lunch_final.iloc[i]["protein"], lunch_final.iloc[i]["fat"],
                                       lunch_final.iloc[i]["carbo"],
                                       lunch_final.iloc[i]["sweet"], lunch_final.iloc[i]["Nat"]],
                                      [dinner_final.iloc[i]["basic"], dinner_final.iloc[i]["soup"],
                                       dinner_final.iloc[i]["main"],
                                       dinner_final.iloc[i]["side"], dinner_final.iloc[i]["sim"],
                                       dinner_final.iloc[i]["tcal"],
                                       dinner_final.iloc[i]["protein"], dinner_final.iloc[i]['fat'],
                                       dinner_final.iloc[i]['carbo'],
                                       dinner_final.iloc[i]['sweet'], dinner_final.iloc[i]["Nat"]]]
                                 })

        all_result['thisweek']=thisweek
        all_result['preweek']=preweek
        all_result['nextweek']= nextweek
        global_result.append(all_result)
        return render_template('diet_result.html', date=today, date2=dayslater, all_result=all_result, days=days1,
                               check_str=check_str, week=week)

# 식단분석페이지
# @app.route("/analysis", methods=['POST'])
# def page():
#     today = datetime.date.today()
#     dayslater = today + datetime.timedelta(days=7)
#     if request.method=="POST":
#         return render_template('analysis.html', date=today, date2=dayslater)
#     else:
#         return render_template('analysis.html', date=today, date2=dayslater)

@app.route("/analysis")
@app.route("/analysis", methods=['POST'])
def analysis():
    # diet_list=request.post['diet_list']
    today = datetime.date.today()
    dayslater = today + datetime.timedelta(days=7)
    dt = datetime.datetime.now()
    days1 = dt.weekday()

    if request.method=="POST":
        diet_list=request.args.get('diet_list')
        check_str = request.args.get('check_str')
        return render_template(
            'analysis.html',  date=today, date2=dayslater, diet_list=global_result, check=check
        )
    else:
        return render_template(
            'analysis.html', date=today, date2=dayslater, diet_list=global_result, day=days1,
      check=check)

if __name__ == '__main__':
    app.run(debug=True)
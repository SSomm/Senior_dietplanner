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


# 영양제 크롤링
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from IPython.core.display import HTML


# 이미지 링크를 html 태그로 바꿔주는 함수 작성
def path_to_image_html(path):
    return '<img src="' + path + '" width="60" >'


def get_supplements(nutrition):
    # 최종 저장 데이터 프레임을 위한 리스트
    # list_for_df 에는 각각의 영양제 정보가 리스트 형태로 들어감
    # 각각의 영양제 정보는 ["이미지", "제품명","평점(5점 만점)","가격(원)","링크"] 순서로 들어감
    list_for_df = []

    # 어린이용 영양제 제거를 위한 키워드 설정
    kids_list = ["어린이", "유아", "영아", "kids", "baby", "infant", "toddler", "청소년", "성장기", "성장", "발달", "쑥쑥", "우리아이", "아이"]

    # 검색하려는 영양소를 keyword로 설정
    keyword = nutrition

    # sr=2 옵션: 판매량이 많은 순서로 정렬
    r = requests.get(f"https://kr.iherb.com/search?kw={keyword}&sr=2").text
    b = BeautifulSoup(r, 'html.parser')

    k = b.select("#FilteredProducts > div > div:nth-of-type(2) > div > div")
    for i in k:
        # 별점이 4점 미만이면 pass
        raw_rate = i.select_one("a.stars")["title"]
        rate = re.sub("[/].*", "", raw_rate)
        rate = float(rate)
        if rate < 4:
            continue
        else:
            # print(f"4점을 넘긴 이 상품의 점수는 {rate}")

            # 영양제 이름을 title로 받음
            title = i.select_one("div.product-title").text
            # title 명 앞뒤에 있는 개행문자 없애기(strip이용)
            title = title.strip()
            # 어린이용 영양제인 경우 pass
            if any(x in title for x in kids_list):
                continue
            # print(title)

            # 영양제 가격정보를 price로 받음
            price = i.select_one("span.price ").text
            price = re.sub("\D", "", price)
            # print(price)

            # 영양제 이미지 정보를 image로 받음
            image = str(i.select_one("span.product-image > img")["src"])

            # 영양제 링크 정보를 link로 받음
            link = i.select_one("div.absolute-link-wrapper > a")["href"]
            # print(link)

            # 영양제 정보를 하나의 리스트에 담음
            temp_list = [image, title, rate, price, link]

            # 해당 영양제 정보(리스트)를 최종 리스트에 append 해줌
            list_for_df.append(temp_list)

            # 만약 최종 리스트의 길이가 5와 같거나 크면 크롤링을 중단함
            if len(list_for_df) >= 5:
                break
    # supplement_df = pd.DataFrame(list_for_df)
    # supplement_df.columns = ["이미지", "제품명", "평점(5점 만점)", "가격(원)", "링크"]
    # pd.set_option('display.max_colwidth', -1)
    return list_for_df

pill_list={}
all_pill=[]

cal_mag = get_supplements("칼슘 마그네슘")
ribo    = get_supplements("리보플라빈")
sele    = get_supplements("셀레늄")
coen    = get_supplements("코엔자임q10")
omega   = get_supplements("오메가3")

pill_list['cal_mag']=cal_mag[0]
pill_list['ribo']=ribo[0]
pill_list['sele']=sele[0]
pill_list['coen']=coen[0]
pill_list['omega']=omega[0]

all_pill.append(pill_list)

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

def analysis_method(week):
    days=[0,1,2,3,4,5,6]
    meals=[0,1,2]
    cosine=[]
    nat=[]
    sweet=[]
    carbo=[]
    protein=[]
    fat=[]

    for i in days:
        for j in meals:
            cosine.append(float(global_result[0][week][i][i][j][4]))
            nat.append(float(global_result[0][week][i][i][j][10]))
            sweet.append(float(global_result[0][week][i][i][j][9]))
            protein.append(float(global_result[0][week][i][i][j][6]))
            fat.append(float(global_result[0][week][i][i][j][7]))
            carbo.append(float(global_result[0][week][i][i][j][8]))
    com_cosine=sum(cosine)/len(cosine)
    com_na=sum(nat)/len(nat)
    com_sweet=sum(sweet)/len(sweet)
    com_protein=sum(protein)/len(protein)
    com_carbo=sum(carbo)/len(carbo)
    com_fat=sum(fat)/len(fat)
    com_rate=[com_protein, com_carbo, com_fat]
    nutri_all=com_protein + com_carbo + com_fat
    rating=[com_protein/nutri_all, com_carbo/nutri_all, com_fat/nutri_all]
    answer=[{
     'com_cosine':com_cosine,
     'com_na':nat,
     'com_sweet':sweet,
     'com_rate':com_rate,
     'rating':rating
    }]
    return (answer)

# 식단분석페이지
@app.route("/analysis")
@app.route("/analysis", methods=['POST'])
def analysis():
    # diet_list=request.post['diet_list']
    today = datetime.date.today()
    dayslater = today + datetime.timedelta(days=7)
    dt = datetime.datetime.now()
    days1 = dt.weekday()

# 식단 분석표 정보 출력을 위한 back 작업
# 이번주 식단 분석 정보
    this=analysis_method('thisweek')
# 지난주 식단 분석 정보
    pre = analysis_method('preweek')
# 다음주 식단 분석 정보
    next = analysis_method('nextweek')

    if request.method=="POST":
        diet_list=request.args.get('diet_list')
        check_str = request.args.get('check_str')
        return render_template(
            'analysis.html',  date=today, date2=dayslater, diet_list=global_result, check=check, all_pill=all_pill,
        this=this, pre=pre, next=next)
    else:
        return render_template(
            'analysis.html', date=today, date2=dayslater, diet_list=global_result, day=days1,
      check=check, all_pill=all_pill, this=this, pre=pre, next=next)

if __name__ == '__main__':
    app.run(debug=True)
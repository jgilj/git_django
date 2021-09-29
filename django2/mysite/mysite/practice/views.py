#from .models import Post
import json
from django.db import connection
import pandas as pd
# from .models import Post
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
import json
import pandas as pd
from django.db import connection
from django.shortcuts import render, redirect
from datetime import datetime,timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from wordcloud import WordCloud
from collections import Counter
import string
import random
import string
# Create your views here.

#################################################################################
## 유튜브
def youtube_pop(st_cd):
    cursor = connection.cursor()
    result_re = pd.DataFrame()
    finacedata = []

    if type(st_cd) == str:

        st_cd = [st_cd]
    else:
        st_cd = st_cd

    for cd in st_cd:
        # ############ DB에서 데이터 가져오기 ################
        query2 = 'SELECT * FROM `youtube_hk_{}` order by date desc limit 1;'.format(cd)
        result = cursor.execute(query2)
        globals()['youtube_hk_{}'.format(cd)] = pd.DataFrame(cursor.fetchall())

        result_re=result_re.append(globals()['youtube_hk_{}'.format(cd)])
        # result.reset_index(inplace=True)
    connection.commit()
    connection.close()
    for i in range(len(result_re)):
        row = {
            'st_n': result_re.iloc[i][0],
            'st_cd': result_re.iloc[i][1],
            'title': result_re.iloc[i][4],
            # 'url': result_re.iloc[i][9],
            'url': result_re.iloc[i][5],
        }
        finacedata.append(row)
    newsJSON = json.dumps(finacedata)
    return newsJSON
#################################################################################
### 뉴스
def news_pop(st_cd):
    cursor = connection.cursor()
    result_re = pd.DataFrame()
    finacedata = []

    if type(st_cd) == str:

        st_cd = [st_cd]
    else:
        st_cd = st_cd

    for cd in st_cd:
        # ############ DB에서 데이터 가져오기 ################
        #query2 = 'SELECT * FROM `youtube_hk_{}` order by date desc limit 1;'.format(cd)
        #query2 = 'SELECT * FROM proj.accuracy_point where st_cd = {} order by ratio desc limit 1;'.format(cd)
        # query2 = 'SELECT * FROM `asia_news_craw_{}` order by date desc limit 1;'.format(cd)
        # result = cursor.execute(query2)
        # globals()['asia_news_craw_{}'.format(cd)] = pd.DataFrame(cursor.fetchall())
        # result_re = result_re.append(globals()['asia_news_craw_{}'.format(cd)])

        ## accuracy
        query2 = 'SELECT * FROM accuracy_point where st_cd = {} order by ratio desc limit 1;'.format(cd)
        result = cursor.execute(query2)
        globals()['accuracy_{}'.format(cd)] = pd.DataFrame(cursor.fetchall())
        result_re = result_re.append(globals()['accuracy_{}'.format(cd)])
    connection.commit()
    connection.close()
    for i in range(len(result_re)):
        row = {
            'st_cd': result_re.iloc[i][0],
            'st_n': result_re.iloc[i][1],
            'news': result_re.iloc[i][2],
            'datetime':result_re.iloc[i][3][:8],
            'title': result_re.iloc[i][4],
            'url': result_re.iloc[i][5],
            'Tokenization': result_re.iloc[i][6],
            'Positive_Score': str(result_re.iloc[i][7]),
            'Negative_Score': str(result_re.iloc[i][8]),
            'Ratio': str(round(result_re.iloc[i][9],)),
            'Rred': str(result_re.iloc[i][10]),
        }
        # row = {
        #     'st_n': result_re.iloc[i][0],
        #     'st_cd': result_re.iloc[i][1],
        #     'title': result_re.iloc[i][4],
        #     'url': result_re.iloc[i][5],
        # }
        finacedata.append(row)
    newsJSON = json.dumps(finacedata)
    return newsJSON

### index_정확도
def index_accuracy(st_nm):
    cursor = connection.cursor()
    result_re = pd.DataFrame()
    finacedata = []
    dates = "SELECT datetime FROM proj.accuracy_point order by datetime desc limit 1;"
    cursor.execute(dates)
    dates = pd.DataFrame(cursor.fetchall())
    dates= str(dates[0][0])[:8]
    if st_nm == 0:
        query2 = "SELECT news,avg(Ratio) FROM accuracy_point where datetime like '{}%' group by news;".format(dates)
    else:
        query2 = "SELECT news,avg(Ratio) FROM accuracy_point where st_cd like'%{}%' and datetime like '{}%' group by news;".format(st_nm,dates)
    result = cursor.execute(query2)
    result = pd.DataFrame(cursor.fetchall())
    connection.commit()
    connection.close()
    result_re = result_re.append(result)
    for i in range(len(result_re)):
        row = {
            'news': result_re.iloc[i][0],
            'Ratio': str(round(result_re.iloc[i][1]*100,1)),
        }
        finacedata.append(row)
    index_acc = json.dumps(finacedata)

    return index_acc


########################################################################################################
### 코스피 연도별 그래프
def result(request, yearid):
    finacedata = []
    result=kospi_search(request)

    if yearid != 0:
        yearid = str(yearid)
        result=result[result['Date'].str.contains(yearid)]
    else:
        # result['dates'] = '0'
        for i in range(len(result)):
            result['Date'][i] = result['Date'][i][:7]
        result=result.groupby(['Date']).mean()
        result.reset_index(inplace=True)
    for i in range(len(result)):
        row = {
            'dates': result.iloc[i][0],
            'changes': str(round(result.iloc[i][1], 1))
        }
        finacedata.append(row)
    finacedataJSON = json.dumps(finacedata)

    # st_cd = ['000660','005380','005930','051910','068270']
    # newsJSON=news_pop(st_cd)
    # return render(request,'index.html',{'finacedataJSON':finacedataJSON,'newsJSON':newsJSON})
    return finacedataJSON
######################################################################################################
### 코스피 데이터 가져오기
def kospi_search(request):
    ############################## 데이터 칼럼 가져 오기
    cursor = connection.cursor()
    query1 = 'show full columns from `kospi`'
    cursor.execute(query1)
    select = pd.DataFrame(cursor.fetchall())
    col = list()
    for i in select[0]:
        col.append(i)

    query2 = 'SELECT * FROM `kospi`;'
    cursor.execute(query2)
    result = pd.DataFrame(cursor.fetchall(), columns=col)
    connection.commit()
    connection.close()
    return result

######################################################################################################################
## finance data
# def finance_data(request, st_cd ,yearid=0):
#     cursor = connection.cursor()
#     finacedata=[]
#     if(yearid==0):
#         query2 = 'SELECT * FROM `financedata`;'
#     else:
#         query2 = 'SELECT * FROM `financedata` where st_cd = "{}" and date like % "{}"%;'.format(st_cd)
#
#     result = cursor.execute(query2)
#     result = pd.DataFrame(cursor.fetchall())
#     connection.commit()
#     connection.close()
#     if yearid == 0:
#         for i in range(len(result)):
#             result['Date'][i] = result['Date'][i][:7]
#         result = result.groupby(['Date']).mean()
#         result.reset_index(inplace=True)
#
#     for i in range(len(result)):
#         row = {
#             'dates': result.iloc[i][0][:10],
#             'changes': str(round(result.iloc[i][4], 3))
#         }
#
#         finacedata.append(row)
#     finacedataJSON = json.dumps(finacedata)
#     return finacedataJSON



#############################################################################
## 개별 종목
##
def finance_data(st_cd,yearid=0):
    finacedata = []
    ############################## 데이터 칼럼 가져 오기
    cursor = connection.cursor()
    query1 = 'show full columns from `financedata`'
    cursor.execute(query1)
    select = pd.DataFrame(cursor.fetchall())
    col = list()
    for i in select[0]:
        col.append(i)
    ############################## 데이터
    if yearid ==0:
        query2 = 'SELECT * FROM `financedata` where st_cd = "{}";'.format(st_cd)
        result = cursor.execute(query2)
        result = pd.DataFrame(cursor.fetchall(), columns=col)
        if yearid == 0:
            for i in range(len(result)):
                result['Date'][i] = result['Date'][i][:7]
            result = result.groupby(['Date']).mean()
            result.reset_index(inplace=True)
    else:
        query2 = 'SELECT * FROM `financedata` where st_cd = "{}" and date like "{}%";'.format(st_cd,yearid)
        result = cursor.execute(query2)
        result = pd.DataFrame(cursor.fetchall(), columns=col)
    connection.commit()
    connection.close()

    for i in range(len(result)):
        row = {
            'dates': result.iloc[i][0][:10],
            'changes': str(round(result.iloc[i][4], 3))
        }

        finacedata.append(row)
    finacedataJSON = json.dumps(finacedata)
    return finacedataJSON
def date_finance_data(st_cd):

    finacedata = []
    ############################## 데이터 칼럼 가져 오기
    cursor = connection.cursor()
    query2 = 'SELECT * FROM `financedata` where st_cd = "{}" order by Date desc limit 1;'.format(st_cd)

    result = cursor.execute(query2)
    result = pd.DataFrame(cursor.fetchall())
    connection.commit()
    connection.close()

    row = {
        'dates': result.iloc[0][0][:10],
        'close': str(result.iloc[0][4]),
        'volume': str(result.iloc[0][5]),
        'changes': str(round(result.iloc[0][6], 3))
    }
    finacedata.append(row)
    datefinacedataJSON = json.dumps(finacedata)
    return datefinacedataJSON

######################################################################################################################
### 워드 클라우드
def wordcloud_maker(request,st_cd):
    ## DB 연결
    cursor = connection.cursor()
    dates = "SELECT datetime FROM proj.accuracy_point order by datetime desc limit 1;"
    cursor.execute(dates)
    dates = pd.DataFrame(cursor.fetchall())
    dates = str(dates[0][0])[:8]

    if st_cd == '0':
        query2 = 'SELECT * FROM accuracy_point where datetime like "{}%";'.format(dates)
        result = cursor.execute(query2)
        result = pd.DataFrame(cursor.fetchall())
        # result = result.groupby([0], as_index=False).mean()

    else:
        # query2 = 'SELECT * FROM proj.accuracy_point where st_cd = {} order by ratio desc limit 1;'.format(st_cd)
        query2 = "SELECT * FROM accuracy_point where st_cd = {} and datetime like '%{}%';".format(st_cd,dates)
        result = cursor.execute(query2)
        result = pd.DataFrame(cursor.fetchall())
    connection.commit()
    connection.close()

    # 한글 형태소 분석하기

    # # 단어 숫자 세기
    li = []

    for i in range(len(result)):
        li.extend(result.loc[i][6].split(' '))

    count = Counter(li)
    tags = count.most_common()
    tags= dict(tags)
    # tags=sorted(tags.items(), key=lambda x: x[1], reverse=True)
    #

    for index, (key, value) in list(enumerate(tags.items())):
        if index >= 50:
            # print('abcx')
            del tags[key]
        # if value <= 10:
        #     del tags[key]
        # print(index)
    wordcloudJSON = json.dumps(tags)
    return wordcloudJSON



######################################################################################################################
def index(request, yearid=0):
    # finacedataJSON = kospi_search(request)

    ##### 주가 데이터
    finacedataJSON=result(request, yearid)
    st_cd = ['000660','005380','005930','051910','068270']
    ###### 뉴스
    newsJSON=news_pop(st_cd)

    ##### 정확도
    # accuracyJson=accuracy(request,'0')
    accuracyJson=index_accuracy(0)

    #### 워드클라우드
    wordcloudJSON=wordcloud_maker(request,'0')

    return render(request,'index.html',{'finacedataJSON':finacedataJSON,'newsJSON':newsJSON,'accuracyJson':accuracyJson,'wordcloudJSON':wordcloudJSON})

def samsung(request,yearid=0):
    st_cd= '005930'
    st_n = '5930'
    finacedataJSON=finance_data(st_cd,yearid)
    datefinacedataJSON=date_finance_data(st_cd)

    newsJSON=news_pop(st_cd)
    # accuracyJson = accuracy(request, st_cd)
    accuracyJson = index_accuracy(st_n)

    #### 워드클라우드
    wordcloudJSON = wordcloud_maker(request, st_n)

    return render(request, 'samsung.html', {'finacedataJSON': finacedataJSON,'datefinacedataJSON':datefinacedataJSON,
                                            'newsJSON':newsJSON,'accuracyJson':accuracyJson,'wordcloudJSON':wordcloudJSON})

def sk_hynicx(request,yearid=0):
    st_cd = '000660'
    st_n = '660'
    finacedataJSON = finance_data(st_cd, yearid)
    datefinacedataJSON = date_finance_data(st_cd)

    newsJSON = news_pop(st_cd)
    # accuracyJson = accuracy(request, st_cd)
    accuracyJson = index_accuracy(st_n)
    #### 워드클라우드
    wordcloudJSON = wordcloud_maker(request, st_n)

    return render(request, 'sk_hynicx.html',
                  {'finacedataJSON': finacedataJSON, 'datefinacedataJSON': datefinacedataJSON, 'newsJSON': newsJSON,'accuracyJson':accuracyJson,'wordcloudJSON':wordcloudJSON})

def hyundai(request,yearid=0):
    st_cd = '005380'
    st_n = '5380'
    finacedataJSON = finance_data(st_cd, yearid)
    datefinacedataJSON = date_finance_data(st_cd)

    newsJSON = news_pop(st_cd)
    # accuracyJson = accuracy(request, st_cd)
    accuracyJson = index_accuracy(st_n)

    #### 워드클라우드
    wordcloudJSON = wordcloud_maker(request, st_n)
    return render(request, 'hyundai.html',
                  {'finacedataJSON': finacedataJSON, 'datefinacedataJSON': datefinacedataJSON, 'newsJSON': newsJSON,'accuracyJson':accuracyJson,'wordcloudJSON':wordcloudJSON})

def lg_chem(request,yearid=0):
    st_cd = '051910'
    st_n = '51910'
    finacedataJSON = finance_data(st_cd, yearid)
    datefinacedataJSON = date_finance_data(st_cd)

    newsJSON = news_pop(st_cd)
    # accuracyJson = accuracy(request, st_cd)
    accuracyJson = index_accuracy(st_n)

    #### 워드클라우드
    wordcloudJSON = wordcloud_maker(request, st_n)
    return render(request, 'lg_chem.html',
                  {'finacedataJSON': finacedataJSON, 'datefinacedataJSON': datefinacedataJSON, 'newsJSON': newsJSON,'accuracyJson':accuracyJson,'wordcloudJSON':wordcloudJSON})

def celltrion(request,yearid=0):
    st_cd = '068270'
    st_n = '68270'
    finacedataJSON = finance_data(st_cd, yearid)
    datefinacedataJSON = date_finance_data(st_cd)

    newsJSON = news_pop(st_cd)
    # accuracyJson = accuracy(request, st_cd)
    accuracyJson = index_accuracy(st_n)

    #### 워드클라우드
    wordcloudJSON = wordcloud_maker(request, st_n)
    return render(request, 'celltrion.html',
                  {'finacedataJSON': finacedataJSON, 'datefinacedataJSON': datefinacedataJSON, 'newsJSON': newsJSON,'accuracyJson':accuracyJson,'wordcloudJSON':wordcloudJSON})


# def charts(request):
#     return render(request,'charts.html')
#


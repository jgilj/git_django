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
from django.views.decorators.http import require_POST
from django.http import JsonResponse

# Create your views here.


def result(request):
    data=request.GET.get('data2')
    ss=index(request,data)
    print(ss)
    return ss

def index(request, yearss=0):

    finacedata = []
    finacedata_dic = {}
    # try:
    ############################## 데이터 칼럼 가져 오기
    cursor = connection.cursor()
    query1 = 'show full columns from `kospi`'
    cursor.execute(query1)
    select = pd.DataFrame(cursor.fetchall())
    col = list()
    for i in select[0]:
        col.append(i)
    ############################## DB에서 데이터 가져오기
    # query2 = 'SELECT * FROM `financedata` where st_cd = "000660";'
    if yearss != 0:
        query2 = 'SELECT * FROM `kospi` where Date like "{}%";'.format(yearss)
    else:
        query2 = 'SELECT * FROM `kospi`;'
    result=cursor.execute(query2)
    result=pd.DataFrame(cursor.fetchall(),columns=col)
    connection.commit()
    connection.close()

    #### 필요한 데이터만 뽑기
    ################################################
    # print(result)
    for i in range(len(result)):
        result['Date'][i] = result['Date'][i][:7]
    result = result.groupby(['Date']).mean()[['Close']]
    result.reset_index(inplace=True)

    for i in range(len(result)):
        row = {
                'dates' : result.iloc[i][0],
               'changes': str(round(result.iloc[i][1],1))
        }

        finacedata.append(row)
    finacedataJSON = json.dumps(finacedata)
    
    if yearss != 0:
        return render(request, 'index.html', {'finacedataJSONss': finacedataJSON})
        #return HttpResponse({'finacedataJSON':finacedataJSON},content_type='index.html')
    else:
        return render(request,'index.html',{'finacedataJSON':finacedataJSON})

def samsung(request):
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
    query2 = 'SELECT * FROM `financedata` where st_cd = "005930";'

    result = cursor.execute(query2)
    result = pd.DataFrame(cursor.fetchall(), columns=col)
    connection.commit()
    connection.close()
    # print(result)
    for i in range(len(result)):
        result['Date'][i] = result['Date'][i][:7]
    result = result.groupby(['Date']).mean()[['Change']]
    result.reset_index(inplace=True)

    for i in range(len(result)):
        row = {
            'dates': result.iloc[i][0][:10],
            'changes': str(round(result.iloc[i][1], 3))
        }

        finacedata.append(row)
    finacedataJSON = json.dumps(finacedata)
    print(finacedataJSON)
    return render(request, 'samsung.html', {'finacedataJSON': finacedataJSON})

def sk_hynicx(request):
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
    query2 = 'SELECT * FROM `financedata` where st_cd = "000660";'

    result = cursor.execute(query2)
    result = pd.DataFrame(cursor.fetchall(), columns=col)
    connection.commit()
    connection.close()
    # print(result)
    # for i in range(len(result)):
    #     result['Date'][i] = result['Date'][i][:7]
    # result = result.groupby(['Date']).mean()[['Change']]
    # result.reset_index(inplace=True)

    for i in range(len(result)):
        row = {
            'dates': result.iloc[i][0][:10],
            'changes': str(round(result.iloc[i][1], 3))
        }

        finacedata.append(row)
    finacedataJSON = json.dumps(finacedata)

    # print(finacedataJSON)
    return render(request,'sk_hynicx.html',{'finacedataJSON': finacedataJSON})

def hyundai(request):
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
    query2 = 'SELECT * FROM `financedata` where st_cd = "005380";'

    result = cursor.execute(query2)
    result = pd.DataFrame(cursor.fetchall(), columns=col)
    connection.commit()
    connection.close()
    # print(result)
    # for i in range(len(result)):
    #     result['Date'][i] = result['Date'][i][:7]
    # result = result.groupby(['Date']).mean()[['Change']]
    # result.reset_index(inplace=True)

    for i in range(len(result)):
        row = {
            'dates': result.iloc[i][0][:10],
            'changes': str(round(result.iloc[i][1], 3))
        }

        finacedata.append(row)
    finacedataJSON = json.dumps(finacedata)

    # print(finacedataJSON)
    return render(request, 'hyundai.html', {'finacedataJSON': finacedataJSON})

def lg_chem(request):
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
    query2 = 'SELECT * FROM `financedata` where st_cd = "051910";'

    result = cursor.execute(query2)
    result = pd.DataFrame(cursor.fetchall(), columns=col)
    connection.commit()
    connection.close()
    # print(result)
    # for i in range(len(result)):
    #     result['Date'][i] = result['Date'][i][:7]
    # result = result.groupby(['Date']).mean()[['Change']]
    # result.reset_index(inplace=True)

    for i in range(len(result)):
        row = {
            'dates': result.iloc[i][0][:10],
            'changes': str(round(result.iloc[i][1], 3))
        }

        finacedata.append(row)
    finacedataJSON = json.dumps(finacedata)

    # print(finacedataJSON)
    return render(request, 'lg_chem.html', {'finacedataJSON': finacedataJSON})

def celltrion(request):
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
    query2 = 'SELECT * FROM `financedata` where st_cd = "068270";'

    result = cursor.execute(query2)
    result = pd.DataFrame(cursor.fetchall(), columns=col)
    connection.commit()
    connection.close()
    # print(result)
    # for i in range(len(result)):
    #     result['Date'][i] = result['Date'][i][:7]
    # result = result.groupby(['Date']).mean()[['Change']]
    # result.reset_index(inplace=True)

    for i in range(len(result)):
        row = {
            'dates': result.iloc[i][0][:10],
            'changes': str(round(result.iloc[i][1], 3))
        }

        finacedata.append(row)
    finacedataJSON = json.dumps(finacedata)

    # print(finacedataJSON)
    return render(request, 'celltrion.html', {'finacedataJSON': finacedataJSON})
def charts(request):
    return render(request,'charts.html')



import requests
import os
import pandas as pd
from pandas import DataFrame,Series
import json
import numpy as np
import time
import datetime
import sqlite3
#下载地址 http://npm.taobao.org/mirrors/chromedriver/
from selenium import webdriver  # 用来驱动浏览器的
from selenium.webdriver import ActionChains  # 破解滑动验证码的时候用的 可以拖动图片
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys  # 键盘按键操作
from selenium.webdriver.support import expected_conditions as EC  # 和下面WebDriverWait一起用的
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素

    
def TestChrome():
    # 往百度发送请求
    driver.get('https://www.baidu.com/')
    driver.implicitly_wait(10)
    
    # 1、find_element_by_link_text  通过链接文本去找
    # 根据登录
    # send_tag = driver.find_element_by_link_text('登录')
    # send_tag.click()
    
    # 2、find_element_by_partial_link_text 通过局部文本查找a标签
    login_button = driver.find_element_by_partial_link_text('登')
    login_button.click()
    time.sleep(1)
    
    # 3、find_element_by_class_name 根据class属性名查找
    login_tag = driver.find_element_by_class_name('tang-pass-footerBarULogin')
    login_tag.click()
    time.sleep(1)
    
    # 4、find_element_by_name 根据name属性查找
    username = driver.find_element_by_name('userName')
    username.send_keys('15622792660')
    time.sleep(1)
    
    # 5、find_element_by_id 通过id属性名查找
    password = driver.find_element_by_id('TANGRAM__PSP_10__password')
    password.send_keys('*******')
    time.sleep(1)
    
    # 6、find_element_by_css_selector  根据属性选择器查找
    # 根据id查找登录按钮
    login_submit = driver.find_element_by_css_selector('#TANGRAM__PSP_10__submit')
    # driver.find_element_by_css_selector('.pass-button-submit')
    login_submit.click()
    
    # 7、find_element_by_tag_name  根据标签名称查找标签
    div = driver.find_element_by_tag_name('div')
    print(div.tag_name)
    
    time.sleep(10)
    
def TodayAsInt():
    nowTm = datetime.datetime.now()
    retVal = nowTm.year*10000 + nowTm.month * 100 + nowTm.day #2014 03 27
    return retVal
def TodayAsInt2(dayOffset = 0):
    nowTm = datetime.datetime.now() + datetime.timedelta(days=dayOffset)
    ret = '%d-%02d-%02d'%(nowTm.year, nowTm.month, nowTm.day)
    return ret
def get_excel(url,path,page1,page2):
    

    print(Data)
    #label = ["基金代码", "基金简称", "日期", "单位净值", "累计净值", "日增长率", "近1周", "近1月", "近3月", "近6月",
             #"近1年", "近2年", "近3年", "今年来", "成立来", "自定义", "手续费"]
    #df = DataFrame(Data, columns=label)
    #df.to_excel(path, index=False)
START_TIME = TodayAsInt2(-365)
END_TIME = TodayAsInt2()
WORK_PATH=os.getcwd()

Headers = {
    "Cookie": "waptgshowtime="+str(TodayAsInt())+"; qgqp_b_id=080aa9f400733f83916e6bd81ca9b63a; st_si=32158012380995; st_asi=delete; ASP.NET_SessionId=1bugmx5okytkzn1myh23gqsn; st_pvi=78362626087654; st_sp=2020-07-14%2008%3A51%3A00; st_inirUrl=https%3A%2F%2Fwww.eastmoney.com%2F; st_sn=7; st_psi=20200714090705802-0-0042861501",
    "Referer": "http://fund.eastmoney.com/data/fundranking.html",
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}
def DownLoadAllFundName():#下载所有基金代码和名称
    t1=time.time()

    sortSelect = 'sc=dm&st=asc'#dm 基金代码排序 st=asc 小到大
    #pn=50表示每次下载50个
    EACH_PAGE_NUM = 50
    url = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&%s&sd" \
           "=%s&ed=%s&qdii=&tabSubtype=,,,,,&pi={}&pn=%d&dx=1&v=0.7666071361308657"%(sortSelect, START_TIME, END_TIME, EACH_PAGE_NUM)

    allRecords = 8000

    hasRecvNum = 0
    iterTimes = 0
    allPages = allRecords / EACH_PAGE_NUM
    while hasRecvNum < allRecords and iterTimes <= allPages:
        iterTimes += 1
        page = int(hasRecvNum/EACH_PAGE_NUM) + 1
        tmpurl = url.format(page)
        print(tmpurl)
        datas = requests.get(tmpurl, headers=Headers).content.decode("utf-8")
        # 取出json部分
        datas = datas[datas.find('{'):datas.find('}')+1] # 从出现第一个{开始，取到}

        # 给json各字段名添加双引号
        datas = datas.replace('datas', '\"datas\"')
        dataPairs = datas.split('],')
        completJson = dataPairs[0] + '],'
        for k in dataPairs[1].split(','):
            k = k.replace(':', '":')
            completJson += '"' + k + ','
        completJson = completJson[0:len(completJson) - 1]
        
        jsonBody = json.loads(completJson)
        allRecords = int(jsonBody['allRecords'])
        allPages = int(jsonBody['allPages'])
        
        data = jsonBody['datas']
        hasRecvNum += len(data)
        print("当前页数", iterTimes, allPages, hasRecvNum, allRecords)
        
        Title = [("FundID",0), ("Name", 1), ("Nameen",2), ("CreateDate",16)]
        sql = 'insert OR IGNORE into FundBase '
        sql += '('
        tmpVal = ''
        for m in Title:
            if tmpVal:
                tmpVal += ','
            tmpVal += "%s"%(m[0])
        sql += tmpVal + ') values '
        
        for row in data:
            rowdata = row.replace('"', '').split(',')
            #tmpData = {}
            sql += '('
            tmpVal = ''
            for m in Title:
                #tmpData[k[0]] = rowdata[m[1]]
                if tmpVal:
                    tmpVal += ','
                tmpVal += "'%s'"%(rowdata[m[1]])
            sql += tmpVal + '),'
        sql = sql[0:len(sql) - 1]    
            
        print(sql)
        QueryDB(sql)
        time.sleep(1)
    t2=time.time()
    print("总共消耗时间：",t2-t1)
SQL_INIT_TABLE = '''CREATE TABLE "FundBase" (
  "FundID" text NOT NULL,
  "Name" TEXT NOT NULL,
  "Nameen" TEXT DEFAULT '',
  "CreateDate" TEXT DEFAULT '',
  "FundType" TEXT DEFAULT '',
  "FundSize" REAL DEFAULT 0,
  "Manager" TEXT DEFAULT '',
  "Manager2" TEXT DEFAULT '',
  "Manager3" TEXT DEFAULT '',
  "Company" TEXT DEFAULT '',
  "MgrFeeYear" real DEFAULT 0,
  "HoldFee" real DEFAULT 0,
  "SaleServiceFeeYear" real DEFAULT 0,
  PRIMARY KEY ("FundID")
);'''

gConn = sqlite3.connect('fund.db')
def QueryDB(sql:str):
    c = gConn.cursor()
    c.execute(sql)
    ret = True
    if sql.upper().find('SELECT') >=0:
        ret = c.fetchall()
        print(ret)
    c.close()
    gConn.commit()
    return ret
QueryDB(SQL_INIT_TABLE)
gMaxFundID = 0
SS = '6.55亿元'
def Str2Num(s:str):
    ret = ''
    for k in s:
        if k.isdigit() or k =='.':
            ret += k
        else:
            break
    num = 0
    if ret:
        num = float(ret)
        if s.find('万') == len(ret):
            num = num * 10000.0
        elif s.find('亿') == len(ret):
            num = num * 100000000.0 
        elif s.find('%') == len(ret):
            num = num / 100.0 
            num = round(num, 4)
    return num
def MergeDict(d:dict, v:dict):
    for k, v in v.items():
        if d.get(k) == None:
            d[k] = v[k]
    return d
def Str2Yi(s:str):
    num= Str2Num(s)
    num = num/100000000.0
    return num
def FmtDict(field2val:dict, name:str, func):
    field2val[name] = func(field2val.get(name, '0'))
gBrowser = None
def GetBrowser():
    global gBrowser
    if not gBrowser:
        gBrowser = webdriver.Chrome()
        gBrowser.implicitly_wait(5)
    return gBrowser
def AllGetFundBaseInfo2():
    sql = "SELECT FundID FROM FundBase WHERE Manager IS NULL or Manager is ''"
    ret = QueryDB(sql)
    for i in range(len(ret)):
        fundID= ret[i][0]
        field2val = GetFundBaseInfo2(fundID)
        print('%d/%d'%(i+1,len(ret)))
        time.sleep(1)
    return
def GetFundBaseInfo2(fundID):
    browser = GetBrowser()

    url= 'http://fundf10.eastmoney.com/jbgk_%s.html'%(fundID)
    browser.get(url)
    tableTag = browser.find_element_by_class_name('info')
    print(url)
    field2val = {}
    for tr in tableTag.find_elements(By.TAG_NAME, 'tr'):
        
        titles = []
        values = []
        for v in tr.find_elements(By.TAG_NAME, 'th'):
            titles.append(v.text)
        for v in tr.find_elements(By.TAG_NAME, 'td'):
            values.append(v.text)
        for i in range(min(len(titles), len(values))):
            field2val[titles[i]] = values[i]
    FmtDict(field2val, '资产规模', Str2Yi)
    FmtDict(field2val, '管理费率', Str2Num)
    FmtDict(field2val, '托管费率', Str2Num)
    FmtDict(field2val, '销售服务费率', Str2Num)
    args = field2val['基金经理人'].split('、')
    field2val['基金经理人'] = args[0]
    if len(args) >= 2 and args[1]:
        field2val['基金经理人2'] = args[1]
    if len(args) >= 3 and args[2]:
        field2val['基金经理人3'] = args[2]

    Title = [('FundType','基金类型'),('FundSize', '资产规模'), ('Manager', '基金经理人'), ('Manager2', '基金经理人2'), ('Manager3', '基金经理人3'), ('Company', '基金管理人'), ('MgrFeeYear','管理费率'), ('HoldFee', '托管费率'),('SaleServiceFeeYear', '销售服务费率')]
    sql = ""
    for k in Title:
        if not sql:
            sql = "update FundBase set "
        else:
            sql += ','
        sql += "%s = '%s'"%(k[0], field2val.get(k[1], ''))
    sql += " where FundID = '%s' "%(fundID)
    #print(sql)
    QueryDB(sql)
    return field2val
if __name__ == '__main__':
    try:
        #TestDB()
        DownLoadAllFundName()
        AllGetFundBaseInfo2()
        
        time.sleep(10)
        pass
    finally:
        gConn.close()
        if gBrowser:
            gBrowser.close()
        
from selenium import webdriver
from pyquery import PyQuery as pq
import pandas as pd
from time import sleep

year = []#"查詢年度","查詢年度"...
co_id = []#"股票代碼","股票代碼"...
df = pd.DataFrame(columns=["co_id","name","date","time","mine_idea"])
df1 = pd.DataFrame(columns=["time","story"])
driver = webdriver.Chrome()
driver.get("http://mops.twse.com.tw/mops/web/t05st01")

for i in range(0,len(year)):
    driver.find_element_by_id("year").clear()
    driver.find_element_by_id("year").send_keys(year[i])
    for i in range(0,len(co_id)):  
        driver.find_element_by_id("co_id").clear()
        driver.find_element_by_id("co_id").send_keys(co_id[i])
        sleep(2)
        clickElement = driver.find_element_by_css_selector("#search_bar1 div.search input[type=button]")                                                   
        clickElement.click()
        sleep(5)
        html = driver.page_source
        doc = pq(html)
        now_handle = driver.current_window_handle
        b = df.shape[0]
        i = 0
        for eachDoc in doc("#t05st01_fm > table > tbody > tr").items():
            i += 1
            if i == 1:
                continue
            co_ids = eachDoc("td:nth-child(1)").text()
            name = eachDoc("td:nth-child(2)").text()
            date = eachDoc("td:nth-child(3)").text()
            time = eachDoc("td:nth-child(4)").text()
            mine_idea = eachDoc("td:nth-child(5)").text()
            words = pd.Series([co_ids,name,date,time,mine_idea], index = ["co_id","name","date","time","mine_idea"])
            df = df.append(words,ignore_index=True)
            n = df.shape[0] - b
            N = n+2
        for i in range(2,N):
            a = str(i)
            try:
                driver.find_element_by_xpath('//*[@id="t05st01_fm"]/table/tbody/tr['+a+']/td[6]/input').click()
                sleep(5)
                all_handles = driver.window_handles
                for handle in all_handles:
                    if handle != now_handle:
                        driver.switch_to_window(driver.window_handles[1])
                        html1 = driver.page_source
                        doc = pq(html1)
                        story = doc("td.odd > pre").text()
                        time1 = doc("tr:nth-child(1) > td:nth-child(6)").text()
                        storys = pd.Series([time1,story], index = ["time","story"])
                        driver.close()
                        driver.switch_to_window(now_handle)
                        df1 = df1.append(storys,ignore_index=True)          
            except:
                break
df = pd.merge(df,df1,how = "left", on = "time")
df.to_csv("storys.csv",encoding="utf-8-sig",index=False)               
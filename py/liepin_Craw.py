from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.keys import Keys
import time
import re
import redis

def main(key,address):
    data = []
    driver = webdriver.Chrome("D:/Program Files/python/chromedriver.exe")
    driver2 = webdriver.Chrome("D:/Program Files/python/chromedriver.exe")
    pool = redis.ConnectionPool(host='127.0.0.1',password='') 
    r = redis.Redis(connection_pool=pool)

    try:
        driver.get("https://www.liepin.com/zhaopin")
        driver.implicitly_wait(3)
        # list down
        selector = driver.find_element_by_xpath('//*[@id="sojob"]/div[1]/form/div[1]/div/div/ul/li[1]/span/em')
        selector.click()
        cityPanel1 = driver.find_element_by_xpath('//*[@id="sojob"]/div[10]/div[2]')
        # city select 依旧不同场景选择城市
        citys = cityPanel1.find_elements_by_tag_name('a')
        for c in  citys:
            if c.text == address:
                c.click()
                driver.find_element_by_xpath('//*[@id="sojob"]/div[10]/div[3]/a[1]').click()
                break
            if c.text == '广东' and address == '佛山':
                c.click()
                cityPanel2 = driver.find_element_by_xpath('//*[@id="sojob"]/div[10]/div[2]')
                city2s = cityPanel2.find_elements_by_tag_name('a')
                for c2 in  city2s:
                    if c2.text == '佛山':
                        c2.click()
                        driver.find_element_by_xpath('//*[@id="sojob"]/div[10]/div[3]/a[1]').click()
                        break
                break

        # type1
        type1 = driver.find_element_by_xpath('//*[@id="sojob"]/div[1]/form/div[2]/div/div[1]/dl[6]/dd[2]/ul/li[3]/a')
        driver.execute_script("arguments[0].click();", type1)
        # type2
        type2 = driver.find_element_by_xpath('//*[@id="sojob"]/div[1]/form/div[2]/div/div[1]/dl[6]/dd[1]/ul/li[4]/a')
        driver.execute_script("arguments[0].click();", type2)
        # query
        keyInput = driver.find_element_by_xpath('//*[@id="sojob"]/div[1]/form/div[1]/div/div/div[1]/input')
        keyInput.send_keys(key)
        keyInput.send_keys(Keys.ENTER)

        #get list  
        elems = driver.find_elements_by_xpath('//*[@id="sojob"]/div[2]/div/div[1]/div[1]/ul/li')
        for i in elems:
            name = i.find_element_by_xpath('./div/div/h3/a')
            url = name.get_attribute('href')
            company = i.find_element_by_xpath('./div/div[2]/p[1]/a')
            salary = i.find_element_by_xpath('./div/div[1]/p[1]/span[1]')
            e = { 'type':'liepin' ,'key':key,'name':name.text,'url': url,'company':company.text,'salary':salary.text,'detail':'','address':''}
            driver2.get(url)
            driver2.implicitly_wait(2)
            try:
                e['detail'] = driver2.find_element_by_xpath('//*[@id="job-view-enterprise"]/div/div/div[1]/div[1]/div[3]/div').text
                e['address'] = driver2.find_element_by_xpath('//*[@id="job-view-enterprise"]/div/div/div[2]/div[2]/div/div[1]/div/ul[1]/li[3]').text
            except Exception as err:
                print(err)

            r.hset('liepin',e['company']+' '+e['name'],str(e))
            data.append(e)
        
        # next
        while True:
            elemNext = None

            try:
                pagebar = driver.find_element_by_xpath('//*[@id="sojob"]/div[2]/div/div[1]/div[1]/div/div')
                pagebtns = pagebar.find_elements_by_tag_name('a')
                for i in pagebtns:
                    if i.text == '下一页':
                        elemNext = i
                        break
            except Exception as err:
                print(err)
                continue
                
            if elemNext is None or elemNext.get_attribute('class') != '':
                break
                
            driver.execute_script("arguments[0].click();", elemNext)
            time.sleep(2)
            temp = driver.find_elements_by_xpath('//*[@id="sojob"]/div[2]/div/div[1]/div[1]/ul/li')
            for j in temp:
                name = j.find_element_by_xpath('./div/div/h3/a')
                url = name.get_attribute('href')
                company = j.find_element_by_xpath('./div/div[2]/p[1]/a')
                salary = j.find_element_by_xpath('./div/div[1]/p[1]/span[1]')
                e = { 'type':'liepin' ,'key':key,'name':name.text,'url': url,'company':company.text,'salary':salary.text,'detail':'','address':''}
                driver2.get(url)
                driver2.implicitly_wait(2)
                try:
                    e['detail'] = driver2.find_element_by_xpath('//*[@id="job-view-enterprise"]/div/div/div[1]/div[1]/div[3]/div').text
                    e['address'] = driver2.find_element_by_xpath('//*[@id="job-view-enterprise"]/div/div/div[2]/div[2]/div/div[1]/div/ul[1]/li[3]').text
                except Exception as err:
                    print(err)

                r.hset('liepin',e['company']+' '+e['name'],str(e))
                data.append(e)

    except Exception as err:
        print(err)
        return data
    finally:
        driver.quit()
        driver2.quit()
        pool.disconnect()
    
    return data

main('c#','广州')
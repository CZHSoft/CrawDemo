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
        driver.get("http://www.0757rc.com/search/offer_search_result.aspx")
        driver.implicitly_wait(3)

        #city
        citybtn = driver.find_element_by_xpath('//*[@id="SelCityBtn"]')
        driver.execute_script("arguments[0].click();", citybtn)
        city1 = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/dl[1]/dd/ul/li[1]/a')
        driver.execute_script("arguments[0].click();", city1)
        city2 = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div[4]/dl[2]/dd/ul/li[3]/a')
        driver.execute_script("arguments[0].click();", city2)
        city3 = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div[5]/dl[1]/dd/ul/li/a')
        driver.execute_script("arguments[0].click();", city3)
        city4 = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/a[1]')
        driver.execute_script("arguments[0].click();", city4)
        time.sleep(5)
        # one week  
        type1 = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_slDate"]/div/a[5]')
        driver.execute_script("arguments[0].click();", type1)

        # query 
        inputbox = driver.find_element_by_xpath('//*[@id="ctl00_keyword"]')
        inputbox.send_keys(key)
        inputbox.send_keys(Keys.ENTER)

        time.sleep(2)
        # get list 
        elems = driver.find_elements_by_xpath('//*[@id="ListView"]/div')
        for i in elems:
            name = i.find_element_by_xpath('./div[1]/a')  
            url = name.get_attribute('href')
            company = i.find_element_by_xpath('./div[2]/a')
            salary = i.find_element_by_xpath('./div[4]')
            e = { 'type':'0757rc' ,'key':key,'name':name.text,'url': url,'company':company.text,'salary':salary.text,'detail':'','address':''}
            driver2.get(url)
            try:
                e['detail'] = driver2.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_requirement"]').text
                e['address'] = driver2.find_element_by_xpath('//*[@id="aspnetForm"]/div[5]/div[2]/div[2]/div[2]/ul/li[3]/div[1]/ul/li[3]/p').text
            except Exception as err:
                print(err)

            r.hset('0757rc',e['company']+' '+e['name'],str(e))
            data.append(e)

        # next
        while True:
            elemNext = None

            try:
                pagebar = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_AspNetPager1"]')
                pagebtns = pagebar.find_elements_by_tag_name('a')
                for i in pagebtns:
                    if i.text == '后页':
                        elemNext = i
                        break
            except Exception as err:
                print(err)
                continue
                
            if elemNext is None or elemNext.get_attribute('disabled') != '':
                break

            driver.execute_script("arguments[0].click();", elemNext)

            temp = driver.find_elements_by_xpath('//*[@id="ListView"]/div')

            for j in temp:
                name = j.find_element_by_xpath('./div[1]/a')  
                url = name.get_attribute('href')
                company = j.find_element_by_xpath('./div[2]/a')
                salary = j.find_element_by_xpath('./div[4]')
                e = { 'type':'0757rc' ,'key':key,'name':name.text,'url': url,'company':company.text,'salary':salary.text,'detail':'','address':''}
                driver2.get(url)
                try:
                    e['detail'] = driver2.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_requirement"]').text
                    e['address'] = driver2.find_element_by_xpath('//*[@id="aspnetForm"]/div[5]/div[2]/div[2]/div[2]/ul/li[3]/div[1]/ul/li[3]/p').text
                except Exception as err:
                    print(err)

                r.hset('0757rc',e['company']+' '+e['name'],str(e))
                data.append(e)
        
  
    except Exception as err:
        print(err)
        return data
    finally:
        driver.quit()
        driver2.quit()
        pool.disconnect()
    
    return data

main('软件工程师','佛山')
# main('c#','广州')


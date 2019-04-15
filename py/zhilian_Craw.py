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
        driver.get("https://sou.zhaopin.com")
        driver.implicitly_wait(3)
        driver2.get("https://jobs.zhaopin.com/453045337250051.htm")
        driver2.implicitly_wait(3)
        # click
        driver.find_element_by_xpath('/html/body/div[2]/div/div/button').click()
        driver2.find_element_by_xpath('/html/body/div[2]/div/div/button').click() 
        # WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath("/html/body/div[2]/div/div/button").click())
        # WebDriverWait(driver2, 10).until(lambda x: x.find_element_by_xpath("/html/body/div[2]/div/div/button").click())
        # list down
        js = 'document.getElementsByClassName("current-city__down")[0].click();'
        driver.execute_script(js)
        # select city 
        elemCity = driver.find_element_by_xpath('//*[@id="queryCityBox"]/div/div/input')
        elemCity.send_keys(address)
        elemCity.send_keys(Keys.ENTER)
        time.sleep(3)
        # send key
        elemKey = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/input')
        elemKey.send_keys(key)
        # query 
        elemKey.send_keys(Keys.ENTER)
        time.sleep(3)

        # get list
        elems = WebDriverWait(driver, 10).until(lambda x: x.find_elements_by_xpath('//*[@id="listContent"]/div/div/a'))
        
        for i in elems:
            name = i.find_element_by_xpath('./div[1]/div[1]/span[1]').text
            company = i.find_element_by_xpath('./div[1]/div[2]/a').text
            url = i.get_attribute('href')
            e = { 'type':'zhilian' ,'key':key,'name':name,'url': url,'company':company,'salary':'','detail':'','address':''}
            driver2.get(url)
            driver2.implicitly_wait(2)
            try:
                e['salary'] = WebDriverWait(driver2, 10).until(lambda x: x.find_element_by_xpath('//*[@id="root"]/div[3]/div/div/div[2]/div[1]/span').text)
                e['address'] = WebDriverWait(driver2, 10).until(lambda x: x.find_element_by_xpath('//*[@id="root"]/div[4]/div[1]/div[1]/div[3]/div/span').text)
                e['detail'] = WebDriverWait(driver2, 10).until(lambda x: x.find_element_by_xpath('//*[@id="root"]/div[4]/div[1]/div[1]/div[2]/div').text)
            except Exception as err:
                print(err)

            r.hset('zhilian',e['company']+' '+e['name'],str(e))
            data.append(e)

        # next page 
        while True:
            elemNext = driver.find_element_by_xpath('//*[@id="pagination_content"]/div/button[2]')
            driver.execute_script("arguments[0].click();", elemNext)
            time.sleep(3)
            temp = WebDriverWait(driver, 10).until(lambda x: x.find_elements_by_xpath('//*[@id="listContent"]/div/div/a'))
            for j in temp:
                name = j.find_element_by_xpath('./div[1]/div[1]/span[1]').text
                company = j.find_element_by_xpath('./div[1]/div[2]/a').text
                url = j.get_attribute('href')
                e = { 'type':'zhilian' ,'key':key,'name':name,'url': url,'company':company,'salary':'','detail':'','address':''}
                driver2.get(url)
                driver2.implicitly_wait(2)
                try:
                    e['salary'] = WebDriverWait(driver2, 10).until(lambda x: x.find_element_by_xpath('//*[@id="root"]/div[3]/div/div/div[2]/div[1]/span').text)
                    e['address'] = WebDriverWait(driver2, 10).until(lambda x: x.find_element_by_xpath('//*[@id="root"]/div[4]/div[1]/div[1]/div[3]/div/span').text)
                    e['detail'] = WebDriverWait(driver2, 10).until(lambda x: x.find_element_by_xpath('//*[@id="root"]/div[4]/div[1]/div[1]/div[2]/div').text)
                except Exception as err:
                    print(err)

                r.hset('zhilian',e['company']+' '+e['name'],str(e))
                data.append(e)
            if elemNext.get_attribute('disabled') != '':
                break
  
    except Exception as err:
        print(err)
        return data
    finally:
        driver.quit()
        driver2.quit()
        pool.disconnect()
    
    return data

# main('c#','佛山')
# main('c#','广州')


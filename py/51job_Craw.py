from selenium import webdriver
import re
import redis

def main(key):

    data = []
    driver = webdriver.Chrome("D:/Program Files/python/chromedriver.exe")
    driver2 = webdriver.Chrome("D:/Program Files/python/chromedriver.exe")
    pool = redis.ConnectionPool(host='127.0.0.1',password='') 
    r = redis.Redis(connection_pool=pool)

    try:
        driver.get("https://search.51job.com")
        driver.implicitly_wait(3)
        # send key
        elemKey = driver.find_element_by_xpath('//*[@id="kwdselectid"]')
        elemKey.send_keys(key)
        # trun add
        js = 'document.getElementById("jobarea").value = "030200,030600"'
        driver.execute_script(js)
        # query 
        elemQuery = driver.find_element_by_xpath('/html/body/div[2]/form/div/div[1]/button')
        elemQuery.click()
        driver.implicitly_wait(1)
        # one week
        elemWeek = driver.find_element_by_xpath('//*[@id="filter_issuedate"]/ul/li[4]/a')
        elemWeek.click()
        # get list
        elems = driver.find_elements_by_xpath('//*[@id="resultList"]/div/p/span/a')
        for i in elems:
            url = i.get_attribute('href')
            e = { 'type':'51job' ,'key':key,'name':i.text,'url': url,'company':'','salary':'','detail':'','address':''}
            driver2.get(url)
            e['company'] = driver2.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]').text
            e['salary'] = driver2.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/strong').text
            e['address'] = driver2.find_element_by_xpath('/html/body/div[3]/div[2]/div[3]/div[2]/div/p').text
            e['detail'] = driver2.find_element_by_xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div').text
            
            # r.hset('51job '+ e['company']+' '+e['name'],e)
            r.hset('51job',e['company']+' '+e['name'],str(e))
            data.append(e)
        while True:
            elemNext = driver.find_element_by_xpath('//*[@id="rtNext"]')
            try:
                if elemNext.tag_name is 'a':
                    elemNext.click()
                    driver.implicitly_wait(1)
                    temp = driver.find_elements_by_xpath('//*[@id="resultList"]/div/p/span/a')
                    for j in temp:
                        url = j.get_attribute('href')
                        e = {'type':'51job' ,'key':key,'name':j.text,'url': url,'company':'','salary':'','detail':'','address':''}
                        driver2.get(url)
                        e['company'] = driver2.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]').text
                        e['salary'] = driver2.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/strong').text
                        e['address'] = driver2.find_element_by_xpath('/html/body/div[3]/div[2]/div[3]/div[2]/div/p').text
                        e['detail'] = driver2.find_element_by_xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div').text
                        # r.hmset('51job '+ e['company']+' '+e['name'],e)
                        r.hset('51job',e['company']+' '+e['name'],str(e))
                        data.append(e)
                else:
                    break
            except Exception as err:
                print(err)
 
    except Exception as err:
        return data
    finally:
        driver.quit()
        driver2.quit()
        pool.disconnect()
    
    return data


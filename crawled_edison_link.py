#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import re
import requests



# webdriver config
options=Options()
options.headless=True
options.add_argument('--proxy-server=socks5://127.0.0.1:1080')
options.add_argument('Connection=close')
#set proxy
proxies={'socks5': 'http://127.0.0.1:1080'}
headers={}
headers['User-Agent']='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
headers['Connection']='close'


#webdriver
browser = webdriver.Chrome(options=options)
target_url = 'https://www.edison.tech/'


selenium_url = [] #selenium crawled list
requests_url = [] #requests list


#get page by selenium 
def get_url_in_selenium(url, webdriver): 

    global selenium_url
    global requests_url
    
    if url in selenium_url: 
        return None
    #resource url append to request list
    if ('css' in url ) or ('js' in url) or ('png' in url) or ('pdf' in url) or ('jpg' in url) or ('zip' in url):
        requests_url.append(url)

    else:
        selenium_url.append(url)
        webdriver.get(url)
        return webdriver


#get url in the page
def get_url(webdriver):
    
    global requests_url

    if webdriver == None:
        return None
    else:    
        get_elem_img = webdriver.find_elements_by_tag_name('img')
        get_img = [get_url_img.get_attribute('src') for get_url_img in get_elem_img]
        
    
        get_elem_script = webdriver.find_elements_by_tag_name('script')
        get_src = [get_url_src.get_attribute('src') for get_url_src in get_elem_script]
        
    
        get_elem_link = webdriver.find_elements_by_tag_name('link')
        get_link = [get_link_src.get_attribute('href') for get_link_src in get_elem_link]
         

        get_elem_href = webdriver.find_elements_by_tag_name('a')
        get_href = [get_url_href.get_attribute('href') for get_url_href in get_elem_href]
         

        get_img.extend(get_link)  #resource
        get_src.extend(get_img)   #resource
        requests_url.extend(get_src) #resource
        
        return get_href


#get status code by requests
def get_status_code(url):
    response = requests.get(url,headers=headers)
    return response.status_code


#loop iterates
depth = 6 #depth
count = 0 #counter
def selenium_crawl(src,dep,count,driver):
    
    global requests_url
    if count >= dep:
        count -= 1
        return
    else:
        if src and ('edison.tech' in src or 'easilydo.com' in src) and src[:4] == 'http':
            if src not in selenium_url:
                selenium_driver = get_url_in_selenium(url=src,webdriver=driver)
                src_child = get_url(webdriver = selenium_driver)
                count += 1

                if not src_child: #has no child link
                    requests_url.append(src)
                    return
                else:
                    print('selenium:',src)
                    selenium_url.append(src) 
                    for i in src_child: #go through all the child links
                        selenium_crawl(i,dep,count,driver)  


if __name__ == '__main__':
    selenium_crawl(target_url,depth,count,browser)
    #print(set(requests_url))
    for src in set(requests_url):
        if src and ('edison.tech' in src or 'easilydo.com' in src) and src[:4]=='http':
            status_code = get_status_code(src)
            if status_code != 200:
                print('request:',src,':',status_code,'invalid link')
            else:
                print('request:',src)

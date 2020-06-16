from html.parser import HTMLParser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import re
import time
import os
import pickle
import getpass
import translit
import pandas as pd

def get_fb_page(url, driver):
    
    time.sleep(2)
    driver.get(url)

    #Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(7)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
    page = driver.page_source
    driver.quit()
    return page

def main():
    target_name = input("Enter the name of the target person: ")
    print("Enter", target_name, "Facebook id: ")
    uid = input()
    
    url = ''
    if uid.isnumeric():
        url = 'https://www.facebook.com/profile.php?id='+uid+'&sk=friends'
    else:
        url = 'https://www.facebook.com/'+uid+'/friends'

    print("Getting Chrome ready... Please wait...")
    time.sleep(3)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.quit()
    print("Done!")

    username = input("Enter your Facebook login: ")
    password = getpass.getpass('Enter your Facebook password: ')
    print("The data mining will start now. Please wait patiently until it finishes.")
    print("You can still use your PC and let the program run in background.")
    time.sleep(15)

    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('http://www.facebook.com/')
    # authenticate to facebook account
    elem = driver.find_element_by_id("email")
    elem.send_keys(username)
    elem = driver.find_element_by_id("pass")
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)
    time.sleep(5)
    print("Successfully logged in to Facebook!")

    page = get_fb_page(url, driver)
    print("The data was gathered succesfully! Calculating the amount of friends...")
    target_front = 'class="oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 q9uorilb mg4g778l btwxx1t3 pfnyh3mw p7hjln8o kvgmc6g5 wkznzc2l oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb lzcic4wl abiwlrkh p8dawk7l pioscnbf etr7akla" href="https://www.facebook.com/'
    page = page[page.find(target_front):]
    target_back = '<span id="ssrb_root_end" style="display:none"></span><!--/$--></div>'
    page = page[:page.find(target_back)]

    friends = {}
    while page.find('f="')!=-1:
        symbol = page.find('f="')+3
        page = page[symbol:]
        symbol = page.find('"')
        link = page[:symbol]
        if 'event' in link or 'friends_mutual' in link:
            continue
        if 'photos' in link:
            break
        symbol = page.find('dir="auto"')+11
        page = page[symbol:]
        name = page[:page.find('</span>')]
        if name in friends:
            pass
        else:
            friends[translit.downgrade(name, "latin-1")] = link

    print("Done!")
    print(target_name, 'has', len(friends), 'friends')
    friends = pd.DataFrame(friends.items(), columns=['Name', 'url'])
    if os.path.exists(target_name+'_friends.csv'):
          os.remove(target_name+'_friends.csv')
    friends.to_csv(target_name+'_friends.csv', encoding = 'utf-8')
    print("The data was saved to", target_name+'_friends.scv')

main()        

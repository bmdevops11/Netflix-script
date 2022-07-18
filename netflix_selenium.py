import os
import re
import pandas as pd
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

USERNAME = os.environ.get("NETFLIX_USER")
PASSWORD = os.environ.get("NETFLIX_PASS")
URL = "https://www.netflix.com/browse"
REGEX = r"https://www.netflix.com/watch/(.*?)\?tctx"

class NetflixLogin():
    def __init__(self):
        print("Creating a Netflix Instance")
        # create an instance of the Netflix class

    def login(self, browser):
        print(browser.current_url)
        try:
            username_field = browser.find_element_by_id('id_userLoginId')
            username_field.send_keys(USERNAME)
            password_field = browser.find_element_by_id("id_password")
            password_field.send_keys(PASSWORD)
        except:

            username_field = browser.find_element_by_id('email')
            username_field.send_keys(USERNAME)
            password_field = browser.find_element_by_id("password")
            password_field.send_keys(PASSWORD)
        login_button = browser.find_element_by_class_name('login-button')
        login_button.click()

    def profileselect(self, browser):
        print(browser.current_url)
        try:
            profile_button = browser.find_element_by_class_name('profile-icon')
            profile_button.click()
        except:
            print("Errorrr mf")
            pass

    def get_favorites(self, browser):
        items = []
        print(browser.find_elements_by_class_name('ptrack-content'))
        for elem in browser.find_elements_by_class_name('ptrack-content'):
            item = {
                'title': elem.find_element_by_class_name('slider-refocus').get_attribute('aria-label'),
                'viewlink': elem.find_element_by_class_name('slider-refocus').get_attribute('href')
            }
            item['id'] = re.search(REGEX, item['viewlink']).group(1)
            item['infolink'] = f"https://www.netflix.com/title/{item['id']}"
            items.append(item)
        pd.DataFrame(items).to_csv('output/items.csv', index=False)

    def set_favorites(self, browser):
        df = pd.read_csv('output/items.csv')
        for elem in df['infolink']:
            print(f"Adding {elem}")
            try:
                browser.get(elem)
                list_button = browser.find_elements_by_class_name('nf-icon-button')[-1]
                time.sleep(1)
                list_button.click()
            except:
                print("FAILED")
    
    def check_available(self, browser, movie, nr_checkings = 4):
        search_box = browser.find_element_by_class_name('searchTab')
        search_box.click()
        search_box = browser.find_element_by_css_selector("input[placeholder='Titles, people, genres']")
        search_box.send_keys(movie)
        time.sleep(1)
        names = browser.find_elements_by_class_name('slider-refocus')
        browser.get(URL)
        for i in range(nr_checkings):
            name = names[2 * i + 1].get_attribute('aria-label')
            print(name)
            if movie == name:
                return True
        return False

def main():
    browser = webdriver.Chrome(ChromeDriverManager().install())
    print("Running Netflix Selenium")
    browser.get(URL)
    netflix = NetflixLogin()

    netflix.login(browser)
    time.sleep(2)
    netflix.profileselect(browser)
    if netflix.check_available(browser, "Attack on Titan"):
        print("It is in Netflix :)")
    else:
        print("It isnt in Netflix :(")
    time.sleep(10)
    browser.quit()
    
if __name__ == "__main__":
    main()

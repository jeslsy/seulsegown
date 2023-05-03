from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import django
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seulsegown.settings")
django.setup()
from store.models import Category, Brand, Jumpo

def Crawling():
    '''
    서울특별시에 위치한 ministop 편의점 점포의 정보를 웹 크롤링한 함수입니다.
    
    '''
    '''0. 미니스톱 사이트 접속하기'''
    jumpos_info = []
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.ministop.co.kr/MiniStopHomePage/page/index.do")
    driver.implicitly_wait(0.5)


    ''' 1. 매장찾기로 마우스 이벤트 '''
    nav_menu = driver.find_element(By.XPATH, '//*[@id="header"]/div[3]/ul/li[1]/a')
    driver.execute_script("arguments[0].click();", nav_menu)


    '''2. 드롭다움 박스 선택하기'''
    dropdown = Select(driver.find_element(By.XPATH, '//*[@id="area1"]'))
    dropdown.select_by_value("1")
    driver.implicitly_wait(3)

    '''3. 검색 버튼 클릭'''
    btn = driver.find_element(By.XPATH, '//*[@id="section"]/div[3]/div/div[2]/div[2]/div[1]/a')
    driver.execute_script("arguments[0].click();", btn)


    '''3. 각 점포 정보 저장하기''' 
    for i in range(1, 261):
        li_element = driver.find_element(By.XPATH, f'//*[@id="section"]/div[3]/div/div[2]/div[2]/div[1]/ul/li[{i}]')
        li_lines = li_element.text.split('\n')
        name = li_lines[0]
        address = li_lines[1]
                            
                    
        jumpos_info.append({
            'jumpo_name': name, 
            'street_address' : address, 
            'latitude': 37.564214,
            'longitude': 127.001699,}
            )
        
    return jumpos_info


def Save_data(jumpos_info, category='편의점', brand='MINISTOP'):
    category = Category.objects.get_or_create(category_name=category)[0]
    brand = Brand.objects.get_or_create(category=category, brand_name=brand)[0]
    success = fail = 0

    for jumpo in jumpos_info:
        try:
            Jumpo.objects.create(brand=brand, **jumpo)
            success += 1
        except django.db.utils.IntegrityError:
            print(f'>>> 이미 저장된 데이터({jumpo["jumpo_name"]})가 있습니다.')
            fail += 1
            pass

    return success, fail, True

def main():
    Save_data(Crawling())

if __name__ == "__main__":
    main()
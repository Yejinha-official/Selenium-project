from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def getMelon(playlist_url): 

    driver = webdriver.Chrome('./chromedriver') # 경로가 아니라 파일명임. 확장자 없음

    driver.get(playlist_url) # 플레이리스트 화면 열기 
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser') 

    ## dj 플레이리스트와 기본 사용자 플레이스트 화면 구조 다르기에 분기 처리
    if(playlist_url.startswith('https://www.melon.com/mymusic/dj')) :  # dj 플레이리스트인 경우

        title = soup.select(
            '#frm > div > table > tbody > tr > td:nth-child(5) > div > div > div.ellipsis.rank01 > span > a'
        )

        print(title)

        singer = soup.select(
            '#frm > div > table > tbody > tr > td:nth-child(5) > div > div > div.ellipsis.rank02 > a'
        )

    else :  # 기본 사용자인 경우 
        title = soup.select(
            '#songList > div.section_playlist > #pageList > #frm > div.tb_list > table > tbody > tr > td.t_left > div.pd_none > div.ellipsis > a.btn_icon_detail > span'
        )
        
        singer = soup.select(
             '#songList > div.section_playlist > #pageList > #frm > div.tb_list > table > tbody > tr > td.t_left > div.wrapArtistName > #artistName'
        )


    playlist = []
    for item in zip(title, singer): # {'title' : 노래 제목, 'singer' : 가수} 로 리스트 만들기 
        
        playlist.append(
            {
            'title' : item[0].text,
            'singer'    : item[1].text
            }
        )
        
    driver.quit() # 멜론 리스트 읽은 드라이버 종료 

    print(playlist)

    return playlist

# 유투브 플레이리스트 저장 
def toYtube(id, passwd, playlist): 
    driver = webdriver.Chrome('./chromedriver')  # 새 드라이버 시작 


    driver.get('https://www.youtube.com/');   	# 유튜브 접속
    time.sleep(15)					#  로그인 동작 시작 
    lg_menu = WebDriverWait(driver,timeout=100).until(EC.presence_of_element_located((By.XPATH,"/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-button-renderer/a/paper-button/yt-formatted-string")))				# 실행합니다.
    lg_menu.click()
    idd = WebDriverWait(driver,timeout=100).until(EC.presence_of_element_located((By.NAME,'identifier') ))  
    idd.send_keys(id)
    sb_btn =  WebDriverWait(driver,timeout=100).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button")))
    sb_btn.send_keys(Keys.ENTER)
    time.sleep(10)
    pwd =  WebDriverWait(driver,timeout=100).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input')))   # element name이 q인 곳을 찾아
    pwd.send_keys(passwd)
    sbp_btn=  WebDriverWait(driver,timeout=100).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button')))
    sbp_btn.send_keys(Keys.ENTER)
    time.sleep(10)

    # 로그인 완료 

    # 루프 돌면서  검색 -> 플레이리스트 저장 반복
    for idx in playlist:
        search_box=WebDriverWait(driver,timeout=100).until(EC.element_to_be_clickable((By.NAME, "search_query")))
        search_box.clear()
        search_box.send_keys(idx['title']+ ' ' + idx['singer'])		# 곡명 가수 로 검색하여 첫번째 검색 결과 플레이리스트 저장 
        time.sleep(10)
        click_menu =WebDriverWait(driver,timeout=100).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="search-icon-legacy"]')))
        click_menu.click()				# 검색
        time.sleep(10)
        sub_menu = WebDriverWait(driver,timeout=100).until(EC.element_to_be_clickable((By.XPATH,"/html/body/ytd-app/ytd-popup-container/iron-dropdown/div/ytd-menu-popup-renderer/paper-listbox/ytd-menu-service-item-renderer[3]/paper-item/yt-formatted-string")))
        sub_menu.click()				# 첫번째 결과의  서브메뉴 클릭
        time.sleep(10)
        playList_btn = WebDriverWait(driver,timeout=100).until(EC.element_to_be_clickable((By.XPATH,"/html/body/ytd-app/ytd-popup-container/paper-dialog/ytd-add-to-playlist-renderer/div[2]/ytd-playlist-add-to-option-renderer[2]/tp-yt-paper-checkbox/div[1]")))   
        playList_btn.click()				# 가장 최근에 생성한 플레이리스트로 저장
        time.sleep(10)
        chk_btn = WebDriverWait(driver,timeout=100).until(EC.element_to_be_clickable((By.XPATH,"/html/body/ytd-app/ytd-popup-container/paper-dialog/ytd-add-to-playlist-renderer/div[1]/yt-icon-button/button/yt-icon")))
        chk_btn.click()				


    driver.quit()



## 실행 코드 

playlist_final = getMelon('플레이리스트 주소')

toYtube('구글 아이디' ,'구글 아이디 비밀번호' ,playlist_final)
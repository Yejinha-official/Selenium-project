# step1.프로젝트에 필요한 패키지 불러오기
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# step2.로그인 정보 및 검색할 회사 미리 정의, 해당 회사의 리뷰 끝 페이지도 정의
usr = "ahwlrhal@naver.com"
pwd = "ks090909!"
query = "그린랩스"
page = 11


# step3.크롬드라이버 실행 및 잡플래닛 로그인

driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")

driver.get("https://www.jobplanet.co.kr/users/sign_in?_nav=gb")
time.sleep(5)

login_id = driver.find_element_by_css_selector("input#user_email")
login_id.send_keys(usr)

login_pwd = driver.find_element_by_css_selector("input#user_password")
login_pwd.send_keys(pwd)

login_id.send_keys(Keys.RETURN)
time.sleep(5)


# step4.원하는 회사의 리뷰 페이지까지 이동
query_vieworks = driver.find_element_by_css_selector("input#search_bar_search_query")
query_vieworks.send_keys(query)
query_vieworks.send_keys(Keys.RETURN)
time.sleep(3)

driver.find_element_by_css_selector("a.tit").click()
time.sleep(15)

driver.find_element_by_css_selector("button.btn_close_x_ty1 ").click()
time.sleep(3)



# step6.크롤링한 정보를 담을 리스트명 정의
list_div = []
list_cur = []
list_date =[]
list_stars = []
list_summery = []
list_merit = []
list_disadvantages = []
list_managers =[]
#하예진 수정
list_detailedStar=[]  #세부 별점 저장 
list_detailedStarChunked=[] # 리뷰 1개당 세부 별점 5개 이기에  NX5  행렬로 자름 

# step7.원하는 회사의 직무/근속여부/일시/요약/평점/장점/단점/경영진에게 바라는 점 크롤링 (for문으로 반복)
for i in range(page): 

    #직무, 근속여부, 일시
    user_info = driver.find_elements_by_css_selector("span.txt1")

    count = int(len(user_info)/4)
    print(count)

    list_user_info = []

    for j in user_info:
        list_user_info.append(j.text)

    for j in range(count):            #한 페이지에 정보 5set씩 나옴. 마지막 페이지는 5개 미만일 수 있으므로 count 변수를 반복횟수로 넣어줌.
        a = list_user_info[4*j]
        list_div.append(a)
        
        b = list_user_info[4*j+1]
        list_cur.append(b)

        c = list_user_info[4*j+3]
        list_date.append(c)

    #별점
    stars = driver.find_elements_by_css_selector("div.star_score")
    for j in stars:
        a = j.get_attribute('style')
        if a[7:9] == '20':
            list_stars.append("1점")
        elif a[7:9] == '40':
            list_stars.append("2점")
        elif a[7:9] == '60':
            list_stars.append("3점")
        elif a[7:9] == '80':
            list_stars.append("4점")
        else:
            list_stars.append("5점")

    #하예진 수정  개별 항목 별점을 모두 읽어와 5개씩 나눈다. (리뷰 1개당 개별 항목 5개)
    detailed_stars = driver.find_elements_by_css_selector("div.bl_score")
    for j in detailed_stars:
        a = j.get_attribute('style')
        if a[7:9] == '20':
            list_detailedStar.append("1점")
        elif a[7:9] == '40':
            list_detailedStar.append("2점")
        elif a[7:9] == '60':
            list_detailedStar.append("3점")
        elif a[7:9] == '80':
            list_detailedStar.append("4점")
        else:
            list_detailedStar.append("5점")
 
    list_detailedStarChunked = [ list_detailedStar[i:i+5] for i in range (0, len(list_detailedStar) ,5 )]  #5개씩 나누어 NX5 행렬 만든다. 
        
        
    #요약 정보
    summery = driver.find_elements_by_css_selector("h2.us_label")

    for j in summery:
        list_summery.append(j.text)
    
    #장점, 단점, 경영진에게 바라는 점
    list_review = []

    review = driver.find_elements_by_css_selector("dd.df1")

    for j in review:
        list_review.append(j.text)

    for j in range(count):            #한 페이지에 정보 5set씩 나옴. 마지막 페이지는 5개 미만일 수 있으므로 count 변수를 반복횟수로 넣어줌.
        a = list_review[3*j]
        list_merit.append(a)
        
        b = list_review[3*j+1]
        list_disadvantages.append(b)

        c = list_review[3*j+2]
        list_managers.append(c)

    # 다음 페이지 클릭 후 for문 진행, 끝 페이지에서 다음 페이지 클릭 안되는 것 대비해서 예외처리 구문 추가
    try:
        driver.find_element_by_css_selector("a.btn_pgnext").click()
        time.sleep(15)
    except:
        pass


# step8.pandas 라이브러리로 표 만들기
total_data = pd.DataFrame()
total_data['날짜'] = pd.Series(list_date)
total_data['직무'] = pd.Series(list_div)
total_data['재직여부'] = pd.Series(list_cur)
total_data['별점'] = pd.Series(list_stars)
#하예진 수정 개별 항목 추가
total_data['승진 기회 및 가능성'] = pd.DataFrame(list_detailedStarChunked)[0]
total_data['복지 및 급여'] = pd.DataFrame(list_detailedStarChunked)[1]
total_data['업무와 삶의 균형'] = pd.DataFrame(list_detailedStarChunked)[2]
total_data['사내 문화'] = pd.DataFrame(list_detailedStarChunked)[3]
total_data['경영진'] = pd.DataFrame(list_detailedStarChunked)[4]

total_data['요약'] = pd.Series(list_summery)
total_data['장점'] = pd.Series(list_merit)
total_data['단점'] = pd.Series(list_disadvantages)
total_data['경영진에게 바라는 점'] = pd.Series(list_managers)

# step9.엑셀 형태로 저장하기
total_data.to_excel("Jobplanet.xls" ,index=True)

# step10.크롬 드라이버 종료
driver.close()

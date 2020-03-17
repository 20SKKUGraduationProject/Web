
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from time import sleep




#<<GLS 크롤링>>

driver = webdriver.Chrome("C:\\Users\\hyurs\\Downloads\\chromedriver_win32\\chromedriver.exe")

driver.maximize_window()

driver.get('https://eportal.skku.edu/wps/portal/!ut/p/z1/04_Sj9CPykssy0xPLMnMz0vMAfIjo8zijQIsnD2c3Q38LcxNnQwC_YNMvPy9gwyCnc30w8EKDFCAo4FTkJGTsYGBe7CBfhSGNLJCqH5ToOkeRkAL3E1DTA0CLUL8g51DwwyBSgjrj8KiBOECfyOsClDMgCjA5QZ_Q_1An_z09NQU_9IS_YLc0AiDzIB0ALi2J0A!/')
sleep(5)

#login
driver.find_element_by_name('userid').send_keys('######')
sleep(1)
driver.find_element_by_name('userpwd').send_keys('######')
sleep(1)
driver.find_element_by_xpath('//*[@id="LoginForm"]/div/button').click()
sleep(10)

#gls
driver.find_element_by_xpath('//*[@id="mypage"]/form[1]/div/div[1]/div[2]/div/ul/li[2]/a/span[1]/img').click()
sleep(1)

#gls창전환
driver.switch_to.window(window_name=driver.window_handles[-1])
sleep(1)

#수업영역
mainmenu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@id, "btnM532030000")]/div')))
ActionChains(driver).move_to_element(mainmenu).click().perform()
sleep(1)

#학사과정-전공
submenu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[contains(@id, "btnMenuM000011088")]/div')))
submenu.click()
sleep(5)


#학사과정-기타/교양
#driver.find_element_by_xpath('//*[@id="mainframe.TopFrame.form.divFrame.form.divTop.form.divPopupMenuM532030000.form.divMain.form.divMenuM532030500.form.btnMenuM000011089"]').click()


#년도학기 클릭
mainmenu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@id, "cboYearTerm.dropbutton")]')))
mainmenu.click()
sleep(1)
submenu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[contains(@id, "cboYearTerm.combolist.item_1")]')))
submenu.click()
sleep(1)


#<반복구간>
#학부(대학)선택
mainmenu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[contains(@id, "cboTongHakbu.dropbutton")]')))
mainmenu.click()
sleep(1)

scroll_num=4
faculties = driver.find_elements_by_xpath('//*[contains(@id, "cboTongHakbu.combolist.item") and contains(@class, "nexacontentsbox")]')

f_num = len(faculties)

Schools=[] #School에 저장할 데이터 (course.models)
Courses=[] #Course에 저장할 데이터 (course.models)

for f in range(0, f_num):   #조정하면서 db 저장  
    #scroll 내리기
    if f>=(f_num-scroll_num): 
        for i in range(0, scroll_num+1):
            scroll = driver.find_element_by_xpath('//*[contains(@id, "cboTongHakbu.combolist.vscrollbar.incbutton") and contains(@class, "ButtonControl incbutton")]')
            scroll.click()
        sleep(5)
    
    fec = f
    if f>(f_num-scroll_num):
        fec-=4
    
    faculties=driver.find_elements_by_xpath('//*[contains(@id, "cboTongHakbu.combolist.item") and contains(@class, "nexacontentsbox")]')
    sleep(1)

    Hakbu = faculties[fec].text

    faculties[fec].click()
    sleep(1)

    
    #전공선택
    mainmenu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[contains(@id, "cboHakgwa.dropbutton")]')))   
    mainmenu.click()
    sleep(1)

    majors = driver.find_elements_by_xpath('//*[contains(@id, "cboHakgwa.combolist.item") and contains(@id, ":text")]')
    
    m_num=len(majors)
            
    for m in range(0, m_num):  #조정하면서 db저장
        maj = m
        #scroll내리기
        if f==4:
                if m>=(m_num-2):
                    for i in range(0, scroll_num+1):
                            scroll = driver.find_element_by_xpath('//*[contains(@id, "cboHakgwa.combolist.vscrollbar.incbutton") and contains(@class, "ButtonControl incbutton")]')
                            scroll.click()
                sleep(5)

                    if m>(m_num-2):
                    maj-=2


        majors = driver.find_elements_by_xpath('//*[contains(@id, "cboHakgwa.combolist.item") and contains(@id, ":text")]')

        Hakgwa=majors[maj].text

        majors[maj].click()
        sleep(1)

        #학부, 학과 리스트
        Schools.append(Hakbu)
        Schools.append(Hakgwa)

        #캠퍼스마다
        #인문사회
        mainmenu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[contains(@id, "rdoCampusGb.radioitem0")]')))   
        mainmenu.click()
        sleep(1)
        #조회클릭
        mainmenu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[contains(@id, "btnSearch")]')))   
        mainmenu.click()  
        sleep(5)
    
        #정보 저장 - 영역구분1/2(학번에 따라 다르게), 캠퍼스, 학수번호, 학점(시수), 교과목명, 수업요시및강의실, 담당교수
        courses = driver.find_elements_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@class, "GridRowControl")]')
        pre_len = len(courses)-1
        order = []
        idx=[]
        for i in range(0,pre_len):
            order.append(i)
            idx.append(i)
        
        if len(courses)>1:
                num = driver.find_elements_by_xpath('//*[contains(@id, "staGridTotal:text")]')
                num_text = num[0].text
                n = int(num_text[10:]) 

                while n>0:  

                    courses = driver.find_elements_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@class, "GridRowControl")]')

                    length = len(courses)-1
                    if n-length<=0:
                            length = n
                    n-=length


                    c = 0
                    while c < length:
    
                        while True:
                            try:
                                courses = driver.find_elements_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@class, "GridRowControl")]')
                                courses[order[c]].click()
                                sleep(1)

                                break
                            except ElementNotInteractableException:
                                sc = driver.find_element_by_xpath('//*[contains(@id, "grdMain.vscrollbar.incbutton")]')
                                for s in range(0,3):
                                        sc.click()
                                sleep(5)

                                courses = driver.find_elements_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@class, "GridRowControl")]')

                    
                                if pre_len < (len(courses)-1):
                                    for j in range(c, c-1+(len(courses)-pre_len)):
                                            order.insert(j, pre_len+j-c)
                                            idx.insert(j, int(num_text[10:])-n-length+j)

                                    if length < (len(courses)-1):
                                            length = len(courses)-1
                                            if n-length<=0:
                                                length = n
                                            n=n+pre_len-length
                                    

                                    pre_len = len(courses)-1
                        
                                        
                        
                        Course=[]
                        Course.append(Hakbu)
                        Course.append(Hakgwa)                        
                        campus = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_8") and contains(@id, ":text")]')
                        Course.append(campus.text)
                        courseid = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_3") and contains(@id, ":text")]')
                        Course.append(courseid.text)
                        coursename = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_4") and contains(@id, ":text")]')
                        Course.append(coursename.text)
                        credit1 = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_2") and contains(@id, ":text")]')
                        Course.append(credit1.text)
                        credit2 = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_9") and contains(@id, ":text")]')
                        Course.append(credit2.text)
                        try:
                                year = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_5") and contains(@id, ":text")]')
                                Course.append(year.text)
                        except NoSuchElementException:
                                Course.append('')
                        coursedate = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_11") and contains(@id, ":text")]')
                        Course.append(coursedate.text)
                        coursetype = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_12") and contains(@id, ":text")]')
                        Course.append(coursetype.text)
                        profname = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_6") and contains(@id, ":text")]')
                        Course.append(profname.text)
                        time = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_10") and contains(@id, ":text")]')
                        Course.append(time.text)
                        etc = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_7") and contains(@id, ":text")]')
                        Course.append(etc.text)

                        Courses.append(Course)

                        c+=1


                        



        #자연과학
        mainmenu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[contains(@id, "rdoCampusGb.radioitem1")]')))   
        mainmenu.click()  
        sleep(1)
        #조회클릭
        mainmenu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[contains(@id, "btnSearch")]')))   
        mainmenu.click()  
        sleep(5)


        #정보 저장 - 영역구분1/2(학번에 따라 다르게), 캠퍼스, 학수번호, 학점(시수), 교과목명, 수업요시및강의실, 담당교수
            
        courses = driver.find_elements_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@class, "GridRowControl")]')
        pre_len = len(courses)-1

        order = []
        idx=[]
        for i in range(0,pre_len):
            order.append(i)
            idx.append(i)
        
        if len(courses)>1:
            num = driver.find_elements_by_xpath('//*[contains(@id, "staGridTotal:text")]')
            num_text = num[0].text
            n = int(num_text[10:]) 

            while n>0:  

                courses = driver.find_elements_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@class, "GridRowControl")]')

                length = len(courses)-1
                if n-length<=0:
                        length = n
                n-=length

                c = 0
                while c < length:
                        
                    while True:
                        try:
                            courses = driver.find_elements_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@class, "GridRowControl")]')
                            courses[order[c]].click()
                            sleep(1)

                            break
                        except ElementNotInteractableException:
                            sc = driver.find_element_by_xpath('//*[contains(@id, "grdMain.vscrollbar.incbutton")]')
                            for s in range(0,3):
                                sc.click()
                            sleep(5)

                            courses = driver.find_elements_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@class, "GridRowControl")]')

                
                            if pre_len < (len(courses)-1):
                                for j in range(c, c-1+(len(courses)-pre_len)):
                                    order.insert(j, pre_len+j-c)
                                    idx.insert(j, int(num_text[10:])-n-length+j)
                                
                                if length < (len(courses)-1):
                                    length = len(courses)-1
                                    if n-length<=0:
                                        length = n
                                    n=n+pre_len-length
                                
                                pre_len = len(courses)-1
                
                    Course=[]
                    Course.append(Hakbu)
                    Course.append(Hakgwa)
                    campus = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_8") and contains(@id, ":text")]')
                    Course.append(campus.text)
                    courseid = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_3") and contains(@id, ":text")]')
                    Course.append(courseid.text)
                    coursename = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_4") and contains(@id, ":text")]')
                    Course.append(coursename.text)
                    credit1 = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_2") and contains(@id, ":text")]')
                    Course.append(credit1.text)
                    credit2 = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_9") and contains(@id, ":text")]')
                    Course.append(credit2.text)
                    try:
                        year = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_5") and contains(@id, ":text")]')
                        Course.append(year.text)
                    except NoSuchElementException:
                        Course.append('')
                    coursedate = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_11") and contains(@id, ":text")]')
                    Course.append(coursedate.text)
                    coursetype = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_12") and contains(@id, ":text")]')
                    Course.append(coursetype.text)
                    profname = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_6") and contains(@id, ":text")]')
                    Course.append(profname.text)
                    time = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_10") and contains(@id, ":text")]')
                    Course.append(time.text)
                    etc = driver.find_element_by_xpath('//*[contains(@id, "grdMain.body.gridrow") and contains(@id, "cell_'+str(idx[c])+'_7") and contains(@id, ":text")]')
                    Course.append(etc.text)

                    Courses.append(Course)
                    
                    c+=1
    

        
        if m<(m_num-1):
            mainmenu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[contains(@id, "cboHakgwa.dropbutton")]')))   
            mainmenu.click()
            sleep(5)

            


    mainmenu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[contains(@id, "cboTongHakbu.dropbutton")]')))
    mainmenu.click()
    sleep(5)
      


driver.quit()  
      


#<<에브리타임 크롤링>>
driver = webdriver.Chrome("C:\\Users\\hyurs\\Downloads\\chromedriver_win32\\chromedriver.exe")

driver.maximize_window()

driver.get('https://everytime.kr/login?redirect=%2Flecture')

sleep(5)
driver.find_element_by_name('userid').send_keys('######')
sleep(1)
driver.find_element_by_name('password').send_keys('######')

sleep(1)
driver.find_element_by_xpath('//*[@id="container"]/form/p[3]').click()
sleep(5)

for course in Courses:
    name = course[4].split('\n')

    #교수명, 수업명 검색 -> 평점 저장
    courseName = name[0]
    profName = course[10]


    ###교수님 평점###
    driver.get('https://everytime.kr/lecture/search/'+profName)

    sleep(2)

    lectures = driver.find_elements_by_xpath('//*[@class="lecture"]')

    prof_rating=-1
    total=0.0
    cnt=0
    for i in range(0, len(lectures)):
        lectures[i].click()
        sleep(2)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        if float(soup.find(class_='value').get_text())!=0:
            total+=float(soup.find(class_='value').get_text())
            cnt+=1

        driver.get('https://everytime.kr/lecture/search/'+profName)
        sleep(2)

        lectures = driver.find_elements_by_xpath('//*[@class="lecture"]')

    if cnt!=0:
        prof_rating = total/cnt

    course.append(round(prof_rating,2))

    ###과목 평점###
    driver.get('https://everytime.kr/lecture/search/'+courseName)

    sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    lecs = soup.find_all('a', class_='lecture')
    lectures = driver.find_elements_by_xpath('//*[@class="lecture"]')

    class_rating=-1
    for i in range(0, len(lectures)):
        try:
            professors = lecs[i].find(class_='professor').get_text()
        except AttributeError:
            professors=''
        try:
            names = lecs[i].find(class_='name').get_text()
        except AttributeError:
            names=''

        if (professors==profName)&(names==courseName):
            lectures[i].click()
            sleep(2)

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            if float(soup.find(class_='value').get_text())!=0:
                class_rating = float(soup.find(class_='value').get_text())

            driver.get('https://everytime.kr/lecture/search/'+profName)
            sleep(2)

            break
    
    course.append(round(class_rating,2))


driver.quit()




###저장###

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grad_project.settings")
import django
django.setup()

from course.models import School, Course



if __name__=='__main__':
      
    School(Hakbu=Schools[0], Hakgwa=Schools[1]).save()

    for course in Courses:
        c = School.objects.get(Hakbu=Schools[0], Hakgwa=Schools[1])
        Course(school=c, Campus=course[2], courseID=course[3],
        courseName=course[4], Credit1=course[5], Credit2=course[6], year=course[7],
        class_day=course[8], class_type=course[9], profName=course[10], credit_time=course[11], etc=course[12],
        prof_rating=course[13], class_rating=course[14]).save()

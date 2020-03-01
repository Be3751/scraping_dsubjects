# 学部選択のプルダウンメニューにズレあり注意。valueや要素の順番が一部ズレている。
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import time

target_url='https://syllabus.doshisha.ac.jp'

# 1:神学部 2:文学部 3:社会学部 4:法学部 5:経済学部 6:商学部 7:理工学部 8:政策学部 9:文化情報学部 10:生命医科学部 11:スポーツ健康科学部 12:心理学部 13:グローバルコミュニケーション学部 14:グローバル地域文化学部
target_course_value = 14
target_year = '2018'

driver = webdriver.Safari()

driver.get(target_url)

# 学部課程1を指定
courseid = driver.find_element_by_name('courseid')
Select(courseid).select_by_value('1')
school_year = driver.find_element_by_name('select_bussinessyear')
Select(school_year).select_by_value(target_year)
subjectcd = driver.find_element_by_name('subjectcd')
# グローバル地域文化学部の場合
if(target_course_value == 14):
    Select(subjectcd).select_by_value(str(19))
    coursename = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td/form/table[1]/tbody/tr[5]/td/select/option['+str(target_course_value*2)+']').text
# 理工学部の場合
elif(target_course_value == 7):
    Select(subjectcd).select_by_value(str(target_course_value))
    coursename = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td/form/table[1]/tbody/tr[5]/td/select/option['+str(18)+']').text
# 政策学部の場合
elif(target_course_value == 8):
    Select(subjectcd).select_by_value(str(target_course_value))
    coursename = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td/form/table[1]/tbody/tr[5]/td/select/option['+str(14)+']').text
# 文化情報学部の場合
elif(target_course_value == 9):
    Select(subjectcd).select_by_value(str(target_course_value))
    coursename = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td/form/table[1]/tbody/tr[5]/td/select/option['+str(16)+']').text
# その他の学部の場合
else:
    Select(subjectcd).select_by_value(str(target_course_value))
    coursename = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td/form/table[1]/tbody/tr[5]/td/select/option['+str(target_course_value*2)+']').text

print(coursename)

maxdisplaynumber = driver.find_element_by_name('maxdisplaynumber')
maxdisplaynumber.send_keys(1000)

search_button = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td/form/center/input[1]')
search_button.send_keys(Keys.ENTER)

# 読み込み待機3秒
sleep(3)
# 検索件数
hitsnumber = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td/dl/dd').text
hitsnumber = int(hitsnumber[:-1])
print(hitsnumber)
subjectnums = []
gap = hitsnumber - 1000

try:
    for i in range(1, hitsnumber+1):
        tmpstr = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td/table/tbody/tr['+str(i)+']/td[1]').text
        subjectnums.append(tmpstr[:-1])
        # 検索結果が1000以上ある場合、次ページに進み取得
        if(i == 1000):
            nextPage = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td/form[2]/input[1]')
            nextPage.send_keys(Keys.ENTER)
            #　読み込み待機3秒
            sleep(3)
            print('Moved to next page.')
            for i in range(1, gap+1):
                tmpstr = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td/table/tbody/tr['+str(i)+']/td[1]').text
                subjectnums.append(tmpstr[:-1])
            break
            print(subjectnums)
except NoSuchElementException:
    print("No such element.")
finally:
    f = open('Desktop/DoshishaSubject/SubjectCode/'+target_year+'/'+coursename+target_year+'.txt', 'w', encoding='utf-8')

    for subjectnum in subjectnums:
        f.write(subjectnum+"\n")

    print('Got subject codes.')
    f.close()
    driver.quit()
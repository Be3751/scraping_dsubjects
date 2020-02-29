# CSV書き込み部分のコード修正, a~fの評価データを配列じゃなくする
# SQL書き込み部分のコード追加
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import time
import csv
import os

target_url='https://duet.doshisha.ac.jp/kokai/html/fi/fi020/FI02001G.html'
# 対象年度の指定
target_year = '2018'
value_to_name = {'01':'神学部', '02':'文学部', '03':'法学部', '04':'経済学部', '05':'商学部', '07':'政策学部', '08':'文化情報学部', '09':'社会学部', '14':'生命医科学部', '15':'スポーツ健康科学部', '16':'理工学部', '17':'心理学部', '19':'グローバルコミュニケーション学部', '22':'グローバル地域文化学部', '60':'一般教養科目', '61':'保健体育科目', '65':'外国語科目'}
target_course_value = '01'
subject_codes = []
# テーブル名を手動で変更する必要がある. 神学部ならtheologyに.
table = 'INSERT INTO `LAA1138458-subjectsdata`.`theology`'
column = '(`code`, `semester`, `name`, `teacher`, `registers`, `a`, `b`, `c`, `d`, `f`) VALUES '

driver = webdriver.Safari()

try:
    driver.get(target_url)
    Select(driver.find_element_by_name('form1:_id86')).select_by_value('110'+target_course_value)
    Select(driver.find_element_by_id('form1:kaikoNendolist')).select_by_value(target_year)
    driver.find_element_by_id('form1:enterDodoZikko').send_keys(Keys.ENTER)
    sleep(1)
    # 該当科目数を取得し、50で割った商と余りを算出
    hitsnum = int(driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[2]/tbody/tr/th/div[1]').text.replace(' ','').replace('\n','').replace('1件目から50件目までを表示','').replace('全','').replace('件','').replace(',',''))
    page_limit = hitsnum // 50
    mod = hitsnum % 50
    margin = hitsnum - mod
    print(str(hitsnum)+' subjects.')
    # 最初のページから最後の手前のページまでのデータ取得
    page =1
    while page <= page_limit:
        # trタグの奇数番目のみデータ取得
        for i in range(1,100,2):
            subject_code = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[1]').text
            semester = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[2]').text
            subject_name = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[3]').text
            subject_teacher = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[4]').text.replace(' ','').replace('\n','')
            subject_registers = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[5]').text
            subject_a = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[6]').text
            subject_b = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[7]').text
            subject_c = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[8]').text
            subject_d = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[9]').text
            subject_f = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[10]').text
            subject_other = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[11]').text
            subject_recave = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[12]').text
            # 取得したデータをcsvファイルに書き込み
            if not os.path.isfile('Desktop/DoshishaSubject/SubjectData/CSV/'+target_year+'/'+value_to_name[target_course_value]+target_year+'.csv'):
                # ファイルがなければ新規書き込み
                print('New CSV file.')
                with open('Desktop/DoshishaSubject/SubjectData/CSV/'+target_year+'/'+value_to_name[target_course_value]+target_year+'.csv', 'w') as f:
                    writer = csv.writer(f)
                    writer.writerow([subject_code, semester, subject_name, subject_teacher, subject_registers, subject_a, subject_b, subject_c, subject_d, subject_f, subject_other, subject_recave])
            else:
                # ファイルがあれば追記
                with open('Desktop/DoshishaSubject/SubjectData/CSV/'+target_year+'/'+value_to_name[target_course_value]+target_year+'.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([subject_code, semester, subject_name, subject_teacher, subject_registers, subject_a, subject_b, subject_c, subject_d, subject_f, subject_other, subject_recave])
            # 取得したデータを用いてSQL書き込み
            if not os.path.isfile('Desktop/DoshishaSubject/SubjectData/SQL/'+target_year+'/'+value_to_name[target_course_value]+target_year+'.txt'):
                # ファイルがなければ新規書き込み
                print('New SQL file.')
                with open('Desktop/DoshishaSubject/SubjectData/SQL/'+target_year+'/'+value_to_name[target_course_value]+target_year+'.txt', 'w') as f:
                    values = "('"+subject_code+"','"+semester+"','"+subject_name+"','"+subject_teacher+"','"+subject_registers+"','"+subject_a+"','"+subject_b+"','"+subject_c+"','"+subject_d+"','"+subject_f+"');"
                    f.write(table+ column + values + '\n')
            else:
                # ファイルがあれば追記
                with open('Desktop/DoshishaSubject/SubjectData/SQL/'+target_year+'/'+value_to_name[target_course_value]+target_year+'.txt', 'a') as f:
                    values = "('"+subject_code+"','"+semester+"','"+subject_name+"','"+subject_teacher+"','"+subject_registers+"','"+subject_a+"','"+subject_b+"','"+subject_c+"','"+subject_d+"','"+subject_f+"');"
                    f.write(table+ column + values + '\n')
        # 次ページへ移る
        # 最初のページの場合
        if page == 1:
            nextPage = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[2]/tbody/tr/th/div[2]/a[1]')
            nextPage.send_keys(Keys.ENTER)
            sleep(1)
        else:
            nextPage = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[2]/tbody/tr/th/div[2]/a[3]')
            nextPage.send_keys(Keys.ENTER)
            sleep(1)
        print('Page '+str(page)+'.')
        page += 1
    # 最後のページのデータ取得
    if mod != 0:
        print('The last page.')
        for i in range(1,margin*2,2):
            subject_code = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[1]').text
            semester = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[2]').text
            subject_name = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[3]').text
            subject_teacher = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[4]').text.replace(' ','').replace('\n','')
            subject_registers = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[5]').text
            subject_a = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[6]').text
            subject_b = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[7]').text
            subject_c = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[8]').text
            subject_d = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[9]').text
            subject_f = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[10]').text
            subject_other = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[11]').text
            subject_recave = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[12]').text
            # 取得したデータをcsvファイルに書き込み
            with open('Desktop/DoshishaSubject/SubjectData/CSV/'+target_year+'/'+value_to_name[target_course_value]+target_year+'.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([subject_code, semester, subject_name, subject_teacher, subject_registers, subject_a, subject_b, subject_c, subject_d, subject_f, subject_other, subject_recave])
            # 取得したデータを用いてSQL書き込み
            with open('Desktop/DoshishaSubject/SubjectData/SQL/'+target_year+'/'+value_to_name[target_course_value]+target_year+'.txt', 'a') as f:
                    values = "('"+subject_code+"','"+semester+"','"+subject_name+"','"+subject_teacher+"','"+subject_registers+"','"+subject_a+"','"+subject_b+"','"+subject_c+"','"+subject_d+"','"+subject_f+"');"
                    f.write(table+ column + values + '\n')
except NoSuchElementException:
    print('No such element.')
finally:
    print('Got all subject records.')
    driver.quit()
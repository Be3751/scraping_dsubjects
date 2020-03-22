# -*- coding: utf-8 -*-
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
print('Please type which year, such as 2018, 2017 or something like that.')
string = input()
target_year = string
value_to_name = {'01':'theology', '02':'literature', '03':'law', '04':'economics', '05':'commerce', '07':'policy', '08':'culture_info', '09':'social', '14':'biology', '15':'sport', '16':'engineering', '17':'psychology', '19':'glo_com', '22':'glo_region', '60':'general', '61':'health', '65':'language'}
print('Here is a list of combinations of a value and a faculty name.')
for value in value_to_name:
    print(value+':'+value_to_name[value])
print('Please type a value of a faculty.')
string = input()
target_course_value = string
subject_codes = []
# SQL生成用の文字列
table = 'INSERT INTO `LAA1138458-subjectsdata`.'
faculty = '`'+ value_to_name[target_course_value] + target_year + '`'
column = '(`code`, `semester`, `name`, `registers`, `a`, `b`, `c`, `d`, `f`, `get_point`) VALUES '

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
            subject_registers = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[5]').text
            subject_a = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[6]').text
            subject_b = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[7]').text
            subject_c = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[8]').text
            subject_d = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[9]').text
            subject_f = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[10]').text
            subject_other = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[11]').text
            subject_recave = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[12]').text

            if subject_a == '' :
                subject_a = '0'
            if subject_b == '' :
                subject_b = '0'
            if subject_c == '' :
                subject_c = '0'
            if subject_d == '' :
                subject_d = '0'
            if subject_f == '' :
                subject_f = '0'

            subject_get_point = float(subject_a) + float(subject_b) + float(subject_c) + float(subject_d)
            subject_get_point = str(subject_get_point)
            # 取得したデータをcsvファイルに書き込み
            if not os.path.isfile(os.path.dirname(__file__)+'/CSV/'+target_year+'/'+value_to_name[target_course_value]+target_year+'.csv'):
                # ファイルがなければ新規書き込み
                print('New CSV file.')
                with open(os.path.dirname(__file__)+'/CSV/'+target_year+'/'+value_to_name[target_course_value]+target_year+'.csv', 'w') as f:
                    writer = csv.writer(f)
                    writer.writerow([subject_code, semester, subject_name, subject_registers, subject_a, subject_b, subject_c, subject_d, subject_f, subject_other, subject_recave])
            else:
                # ファイルがあれば追記
                with open(os.path.dirname(__file__)+'/CSV/'+target_year+'/'+value_to_name[target_course_value]+target_year+'.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([subject_code, semester, subject_name, subject_registers, subject_a, subject_b, subject_c, subject_d, subject_f, subject_other, subject_recave])
            # 取得したデータを用いてSQL書き込み
            if not os.path.isfile(os.path.dirname(__file__)+'/SQL/'+target_year+'/'+value_to_name[target_course_value]+target_year+'.txt'):
                # ファイルがなければ新規書き込み
                print('New SQL file.')
                with open(os.path.dirname(__file__)+'/SQL/'+target_year+'/'+value_to_name[target_course_value]+target_year+'.txt', 'w') as f:
                    values = "('"+subject_code+"','"+semester+"','"+subject_name+"','"+subject_registers+"','"+subject_a+"','"+subject_b+"','"+subject_c+"','"+subject_d+"','"+subject_f+"','"+subject_get_point+"');"
                    f.write(table + faculty + column + values + '\n')
            else:
                # ファイルがあれば追記
                with open(os.path.dirname(__file__)+'/SQL/'+target_year+'/'+value_to_name[target_course_value]+target_year+'.txt', 'a') as f:
                    values = "('"+subject_code+"','"+semester+"','"+subject_name+"','"+subject_registers+"','"+subject_a+"','"+subject_b+"','"+subject_c+"','"+subject_d+"','"+subject_f+"','"+subject_get_point+"');"
                    f.write(table + faculty + column + values + '\n')
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
            subject_registers = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[5]').text
            subject_a = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[6]').text
            subject_b = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[7]').text
            subject_c = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[8]').text
            subject_d = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[9]').text
            subject_f = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[10]').text
            subject_other = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[11]').text
            subject_recave = driver.find_element_by_xpath('//*[@id="form1"]/span/div/div/table[1]/tbody/tr['+str(i)+']/td[12]').text
            subject_get_point = subject_a + subject_b + subject_c + subject_d
            # 取得したデータをcsvファイルに書き込み
            with open(os.path.dirname(__file__)+'/CSV/'+target_year+'/'+value_to_name[target_course_value]+target_year+'.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([subject_code, semester, subject_name, subject_registers, subject_a, subject_b, subject_c, subject_d, subject_f, subject_other, subject_recave])
            # 取得したデータを用いてSQL書き込み
            with open(os.path.dirname(__file__)+'/SQL/'+target_year+'/'+value_to_name[target_course_value]+target_year+'.txt', 'a') as f:
                    values = "('"+subject_code+"','"+semester+"','"+subject_name+"','"+subject_registers+"','"+subject_a+"','"+subject_b+"','"+subject_c+"','"+subject_d+"','"+subject_f+"','"+subject_get_point+"');"
                    f.write(table + faculty + column + values + '\n')
except NoSuchElementException:
    print('No such element.')
finally:
    print('Got all subject records.')
    driver.quit()
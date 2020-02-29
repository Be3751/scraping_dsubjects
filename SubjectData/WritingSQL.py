import csv

target_year = '2018'
value_to_name = {'01':'神学部', '02':'文学部', '03':'法学部', '04':'経済学部', '05':'商学部', '07':'政策学部', '08':'文化情報学部', '09':'社会学部', '14':'生命医科学部', '15':'スポーツ健康科学部', '16':'理工学部', '17':'心理学部', '19':'グローバルコミュニケーション学部', '22':'グローバル地域文化学部', '60':'一般教養科目', '61':'保健体育科目', '65':'外国語科目'}
target_course_value = '01'
rows = []

with open('Desktop/DoshishaSubject/SubjectData/'+target_year+'/'+value_to_name[target_course_value]+target_year+'.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        rows.append(row)



# mysqlデータ追加の例
# INSERT INTO `LAA1138458-subjectsdata`.`theology` (`code`, `semester`, `name`, `teacher`, `registers`, `a`, `b`, `c`, `d`, `f`) VALUES ('123', '春', 'そのえ', 'はじゃ', '123', '0', '0', '0', '0', '0'), ('132', '春', 'ふひあ', 'うん', '34', '9', '9', '9', '9', '9');
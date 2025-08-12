

#f=open('file.txt', "r")
#print(f.read())
#f.close()

#f=open('file.txt', "a")
#f.write('apple\nfifth\t string\n') #добавление новых строк и слов
#print(f.read())

#print(f.read())

#f=open('file.txt','r+b', encoding='utf-8')
#print(f.read(7))
#f.close()

#w-перезапись
#a-запись
#r+-и чтение и запись
#b-бинарная запись (для картинок)
#r+b-читать и записывать и работать с картинками

#f=open('file.txt','r', encoding='utf-8')
#print(f.readline())
#f.close()

#f=open('file.txt','r', encoding='utf-8')
#print(f.readlines()) выводит списком
#f.close()

#f=open('file.txt', "r", encoding='utf-8')
#f.seek(10, 2)
# 0-начало
# 1-от текущего значения
# 2-от конца
#print(f.read())
#f.close()


#try:
    #f=open('filent.txt')
    #f.read()
    #f.close()
#except FileNotFoundError:
    #print('файл не существует')
#finally:
    #f.close()      

# with open('file.txt', 'r', encoding='utf-8') as file:
#     print(file.read())

def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as file: # чтение файла
        lines = file.readlines() #в переменную бедет записан массив из наших строчек
    return [line.split(',') for line in lines] # получили двумерный массив

def write_csv(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        for row in data:
            file.write(';'.join(row))

def filter_students(filename):
    students = read_csv(filename)            
    header = students[0]
    data_rows = students[1:]
    # print(header) проверка работы
    # print(data_rows)
    expulsion= [header]
    grand= [header]


    for student in data_rows:
        gpa = float(student[4])
        if gpa < 3.0:
            expulsion.append(student)
        elif gpa > 4.6:
            grand.append(student)  

    #print(expulsion)

    write_csv('expulsion.txt', expulsion)
    write_csv('grand.txt', grand)


filter_students('file1.txt')    


#print(read_csv('file1.txt')) 



















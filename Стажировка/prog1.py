lis=[1, 10, 1.14, False, True, 100, 15, 32] #список

print(lis[4]) #вывод по индексу, индекс с 0
print(lis[-3]) #вывод в обратном порядке
print(lis[1:4])#вывод с по
print(lis[1:-2])
print(lis[1:-2:2]) #вывод от 10 до 15 c шагом 2

#lis[2] = 'frog' # замена элемента списка
print(lis)

lis.append(512)# добавление элемента в конец списка
print(lis)

#lis.insert(4, "insert") # добавление в нужное место по индексу
print(lis)

lis.extend([2, 3, 4])# добавление списка в конец
print(lis)

lis2 = [10, 20]
lis.extend(lis2) # добавление списка в конец
print(lis)


lis.sort() # сортировка
print(lis)

lis.remove(1) # удаление значения, не индекса
print(lis)

lis.reverse() # обратная сортировка
print(lis)

lis.remove(32)
print(lis)

c=lis.pop(2) # извлечение элемента с индексом 2
print(lis)
print(c)     # выведение извлеченного из списка элемента
 
print(lis.count(10)) # количество элементов 10

string='bmstu, aided, intelligence'
print(string)
print(string.count('i')) # подсчет буквы i в строке

print(string.find('ai'))

print(string.split(',')) # разделение строки в виде списка

print(string.split('i'))

splited_string=string.split(',') # разделители
 
joined_string=";del;".join(splited_string)
print(joined_string)

# кортеж - список который мы не можем изменить

tup1 = (1, 4, 7, 10)
print(tup1.index(7)) # выводит индекс числа 7

# словари  именованный список, имеющий ключи

dictionary = {'name':'Ivan',            
            'group':5123, 
            'average':2.8} 

print(dictionary['name'])
#print(dictionary.clear()) # очистится список

print(dictionary.items())

print(dictionary.keys())

print(dictionary.values())

print(dictionary.get('name'))

#dictionary1=dict(name='Ivan',group: 5123, average: 2.8)

dictionary['group']=6123 # поменяли номер группы
print(dictionary.values())


human = {
    'user1':{
        'firstname': 'Ivan',
        'lastname': 'Ivanov',
        'age': 23,
        'address':('Москва', 'Бригадирский пер-к', '13'),
        'grades':{'math': 4.4, 'physics': 3.5}
    },
    'user2':{

    }
}

print(human['user1']) # вывод словаря user1

print(human['user1']['address']) # вывод адреса

print(human['user1']['address'][2]) # вывод номера дома


# множества 

a=set([1,2,3,4,5,5]) # вывод разных чисел, выводит только одну 5
print(a) # множество можно изменять

b=frozenset([1,2,3,4,5,5]) # множество frozenset нельзя изменить, замороженное множество




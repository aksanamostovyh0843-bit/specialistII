try:

    a=int(input("Введите число: "))
    a +=5
    print(a)
except ValueError:
    print("Число я сказал!")
else:
    print("else")
finally:
    print("finally")    

print('много кода')





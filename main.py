from math import log
from time import time
from random import randint
from crpt import Cryptor

# атака Брамли−Боне
def Bramli_Bone_attack(g, l, s, R, j, delta, cryptor, n):
    #print('Подбираю {}-ый бит'.format(j + 1))
    print('Guessing {}-th bit'.format(j + 1))
    t_1_list = []
    t_2_list = []
    g_ = g | (1 << (511 - j)) #(1) ставим бит 1 на позицию(управляется циклом) и пропускаем побитовой дизъюнк,чтобы получить новый g'
    for i in range(0, l): #(2)
        u_g = ((g + i) * pow(R, -1, n)) % n # преобразование в форму монтгомери с ближайшими соседями
        u_g_ = ((g_ + i) * pow(R, -1, n)) % n
        t_1 = t_2 = 0
        for i in range(0, s):
            message, time = cryptor.interact(u_g)
            t_1 += time
            message, time = cryptor.interact(u_g_)
            t_2 += time
        t_1_list.append(t_1 / s) # mean from 5.2, среднеарифметическое
        t_2_list.append(t_2 / s)
    T_g = sum(t_1_list)
    T_g_ = sum(t_2_list)
    d = abs(T_g - T_g_)
    print('delta =', d, end=', ')
    if d < delta: # если разница маленькая , то бит i равен 1; t(g)<t(g_) время дешифрования g оказалось меньше g_
        print('on {}-th bit we setting 1'.format(j + 1))
        return g_, d
    else: # если дельта "большая", то бит от q это нуль; g>g_ время дешифрования g оказалось больше g_
        print('on {}-th bit we setting 0'.format(j + 1))
        return g, d


# выполняет атаку по времени на некорректную реализацию RSA
def program1(n, e, l, s, delta):
    cryptor = Cryptor('C:\\Users\\Elvin\\Downloads\\cryptor_v4.exe')
    cryptor.run()

    # вычисляем начальное приближение g для множителя q = (2 ** (log(n, 2) // 2))
    # при помощи этого приближения вычисляем R - степень двойки > приближение
    R = int(2 ** ((log(n, 2) // 2) + 1)) #правая граница для g

    # первые 3 бита (всего 512) необходимо подобрать так,
    # чтобы время расширования было было минимальным.
    minimum_time = 10 ** 10
    for number in range(4, 8):
        g = number << 509 # создаём на конце нули, а начало такое же - 3 бита  --  подбор g относительно q
        message, time = cryptor.interact(g)
        if time < minimum_time:
            minimum_time, minimum_time_g = time, g
    g = minimum_time_g
    print('g =', g)

    # далее в ход вступает алгоритм Брамли−Боне,
    # который подбирает остальные биты числа.

    # первые три бита подобраны. далее
    # с 3 по 511 позицию подбираем остальные 
    for i in range(3, 512):
        g, delta_ = Bramli_Bone_attack(g, l, s, R, i, delta, cryptor, n)

    cryptor.close()

    # найти закрытый ключ RSA
    q = g
    p = n // q
    print('p = {}\nq = {}\nn = {}\np * q = {}'.format(p, q, n, p * q))
    return pow(e, -1, (p - 1) * (q - 1)) # выражаем d


n = 0xbdca61f2bdc1b76bda3b7811df28052e0501ad5aad2d206e6b8eb5e578939692d2a7f679fb194104ef79bb90c71f9b1f66c02f830b0b9afad9a527a0ae8fedfb78a178e3fad6a98c9cf95cceafda851eb24fd881c45ec3bd4429a8364f993c4ba1f69020442d00c018b72f8b56edd00dc586f5a485859b752e56cc853361457f
e = 0x010001
#params
l = 6 # neighborhood size
s = 1 # sample size
delta = 500000 # для шага 4 из дока

timer = time()
d = program1(n, e, l, s, delta)
print('d =', d)
timer = time() - timer
message = randint(10 ** 10, 10 ** 11)
cipher = pow(message, e, n)
decipher = pow(cipher, d, n)
if message == decipher:
    #print('Атака прошла успешно, затрачено {} секунд'.format(timer))
    print('Success,we spent {} seconds'.format(timer))
else:
    #print('Атака прошла неуспешно')
    print('No success')
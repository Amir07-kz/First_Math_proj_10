import numpy
from pandas import *
import math
from scipy.stats import chi2
import statistics
import matplotlib.pyplot as plt

from Таблица_значений import t

data = read_csv('workers_info.csv')

data = data['стоимость_акций'].tolist()
numbers = data

count = len(numbers)

print(f"\nКоличество чисел: {count}")
print('\nlg(', + count, ') =', math.log10(count))
intervalValue = math.floor(1 + 3.322 * math.log10(count))
print("\nКоличеcтво интервалов: ", intervalValue)
print("\nX min: ", min(numbers))
print("\nX max: ", max(numbers))
l = math.ceil((max(numbers) - min(numbers)) / math.floor(intervalValue))
print("\nДлина интервала =", l)

xmin = math.floor(min(numbers))
# [)
ni = [[0 for x in range(2)] for y in range(intervalValue)]
for i in range(0, intervalValue):
    ni[i][0] = xmin
    ni[i][1] = xmin + l
    xmin = xmin + l
print(ni)

countList = [[] for y in range(intervalValue)]
for i in range(0, intervalValue):
    x = 0
    for j in range(0, count):
        if ni[i][1] > numbers[j] >= ni[i][0]:
            x = x + 1
    countList[i].append(x)
print(countList)

middle = [[] for y in range(0, intervalValue)]
mid = 0
for i in range(0, intervalValue):
    mid = (ni[i][0] + ni[i][1]) / 2
    middle[i].append(mid)
print(middle)

xMiddle = 0
for i in range(0, intervalValue):
    xMiddle = xMiddle + (middle[i][0] * countList[i][0])
xMiddle = xMiddle / count
print("")
print("Выборочная средняя =", xMiddle)

z = [[] for y in range(0, intervalValue)]
for i in range(0, intervalValue):
    zmid = (middle[i][0] - xMiddle) ** 2
    z[i].append(zmid)
print(z)

sigma = 0.0
for i in range(0, intervalValue):
    sigma = sigma + (z[i][0] * countList[i][0])
sigma = sigma / count
print("\nВыборочная дисперсия =", sigma)

y = 0
if count <= 20:
    y = count
elif 20 < count <= 50:
    if count % 10 == 0:
        y = count
    elif count % 5 == 0:
        y = count
    else:
        y = count - (count % 5)
elif 50 < count <= 100:
    if count % 10 == 0:
        y = count
    else:
        y = count - (count % 10)
elif 120 >= count > 100:
    y = 120
else:
    y = 0
j = 0
for i in range(0, 29):
    if y == t[i][0]:
        j = i
print("\n1      2      3")
gamma = int(input(f"0.95   0,99   0.999\nВыберите гамму из таблицы значений: "))
xIntervalMin = xMiddle - (t[j][gamma] * math.sqrt(sigma)) / math.sqrt(count)
xIntervalMax = xMiddle + (t[j][gamma] * math.sqrt(sigma)) / math.sqrt(count)
gamma = 0
if gamma == 1:
    gamma = 0.95
elif gamma == 2:
    gamma = 0.99
else:
    gamma = 0.999

d = [0 for i in range(intervalValue)]
for i in range(intervalValue):
    d[i] = middle[i][0] - xMiddle

a = 0

for i in range(intervalValue):
    a = a + (d[i] * d[i] * d[i] * countList[i][0] / count)
a = a / math.pow(math.sqrt(sigma), 3)

df = count - 1
alfa1 = (1 - gamma) / 2
alfa2 = (1 + gamma) / 2
p1 = 1 - alfa1
p2 = 1 - alfa2

intervalSigma1 = (df * sigma) / chi2.ppf(p1, df)
intervalSigma2 = (df * sigma) / chi2.ppf(p2, df)

median = statistics.median(numbers)
mode = statistics.mode(numbers)
print("\nМедиана = ", median)
print("\nМода = ", mode)

plt.hist(numbers, edgecolor='black', bins=intervalValue)
plt.title('\nГистограмма для ' + str(count) + ' элементов')
plt.xlabel('Значения')
plt.ylabel('Частоты')
plt.plot(median, "ro", label = 'Медиана')
plt.plot(median, "ro")
plt.plot(mode, "o", label = 'Мода')
plt.plot(mode, "o")
plt.legend()
plt.show()

z4 = [0 for y in range(0, intervalValue)]
x = 0
for i in range(0, intervalValue):
    z4[i] = (z[i][0]) ** 2

m4 = 0

for i in range(0, intervalValue):
    m4 = m4 + z4[i] * countList[i][0]

m4 = m4 / count

ek = m4 / (sigma ** 2) - 3

print("\nКоэффициент эксцесса Ek = ", ek)

z3 = [0 for y in range(0, intervalValue)]
x = 0
for i in range(0, intervalValue):
    z3[i] = (z[i][0]) ** 1.5

m3 = 0

for i in range(0, intervalValue):
    m3 = m3 + z3[i] * countList[i][0]
m3 = m3 / count
a3 = m3 / (sigma ** 1.5)

print("\nКоэффициент ассиметри A3 = ", a3)
print("\nd1=", xIntervalMin)
print("\nd2=", xIntervalMax)
print("")
print(xIntervalMin, "< x <", xIntervalMax)
print("")
print(intervalSigma1, "< sigma <", intervalSigma2)
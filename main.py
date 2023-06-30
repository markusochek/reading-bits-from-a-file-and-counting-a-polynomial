# polynomTest1BE.dat содержит коэффициенты многочлена
# в порядке возрастания показателя степени и аргумент
# (порядок следования байтов - big-endian, формат IEEE-754 binary64).
# Найти значение данного многочлена на заданном аргументе методом Горнера
# и оценки абсолютной погрешности (априорную и апостериорную).
import struct


def binToFloat(bf):
    return struct.unpack('>d', bytes(list(bf)))[0]


def apriori(x, bits, u):
    e = bits[-1]
    n = len(bits)
    for i in range(1, n):
        e = e * abs(x) + abs(bits[i])
    e = 2 * (n-1) * u / (1 - 2 * (n-1) * u) * e  # 2 * n * u * e
    return e


def aposteriori(x, bits, u):
    p = bits[-1]
    n = len(bits)
    M = abs(bits[-1]) / 2
    for i in range(n):
        p = p * x + bits[i]
        M = M * abs(x) + abs(p)
    M = u * (2 * M - abs(p))
    return M


def gorner(x, bits):
    p = 0
    for i in range(len(bits)):
        p = p * x + bits[i]
    return p


file = open("polynomTest1BE.dat", "rb")
symbols = file.read()
bits = []
for i in range(len(symbols) // 8):
    bts = symbols[i * 8:8 + 8 * i]
    bits.append(binToFloat(bts))
u = pow(2, -53)  # u = ulp(1) / 2

print(gorner(bits[-1], (bits[:-1])[::-1]))
print(apriori(bits[-1], (bits[:-1])[::-1], u))
print(aposteriori(bits[-1], (bits[:-1])[::-1], u))
print()

# polynomTest2LE.dat содержит коэффициенты многочлена
# в порядке возрастания показателя степени и три аргумента
# (порядок следования байтов - little-endian, формат IEEE-754 binary64).
# Какой из представленных аргументов может быть нулём данного многочлена, почему?

file = open("polynomTest2LE.dat", "rb")
symbols = file.read()
bits = []
for i in range(len(symbols) // 8):
    bts = (symbols[i * 8:8 + 8 * i])[::-1]
    bits.append(binToFloat(bts))

u = pow(2, -53)  # u = ulp(1) / 2

for i in range(1, 4):
    print("аргумент №" + str(i))
    gorn = gorner(bits[-i], (bits[:-3])[::-1])
    print(gorn)
    print(apriori(bits[-i], (bits[:-3])[::-1], u))
    apost = aposteriori(bits[-i], (bits[:-3])[::-1], u)
    print(apost)
    if (abs(gorn) < apost):
        print("Аргумент может быть нулем данного многочлена")
    else:
        print("Аргумент НЕ может быть нулем данного многочлена")
    print()

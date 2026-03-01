import sys

x = 6000
y = 6000
a = 0
b = 0

for i in range(x):
    for j in range(y):
        z = abs((i+1) - (j+1))
        if z <= 1500:
            a += 1
        else:
            b += 1

    c = a/(x*y)
    d = b/(x*y)

    print(f'\rSucceed Rate: {c:.6f} | Failed Rate: {d:.6f}', end='')
    sys.stdout.flush()

print()
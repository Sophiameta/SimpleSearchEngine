__author__ = 's0540017'

# python 3.4

print("hello world")

x = 10

print(x)

squares = [1, 4, 5, 8, 17]

print(squares)

squares2 = [1, "hallo", 5, 8, 17]

print(squares2)

squares[1:3]

squares[:20]

squares[2:]

# lezte Beide
squares[-2:]


# wichtige Einrueckungen! Bsp. if-Bedingung
if x < 5:
    print("kleiner 5")

else:
    print("größer gleich 5")
    print("bla")

# Bsp. Schleife (alle Elemente einer Liste)
for i in squares:
    print(i)

# Bsp. Schleife (alle Zahlen von 0-4)
for i in range 5:
    print(i)


# Unveränderbare Tupel (im Gegensatz zu Listen)
t = ("xxx", 5)

# Syntaxgesteuerte Zerlegung von Tupeln
t = [("a", 1), ("b", 2), ("c", 3)]

# c= character v= value
for c, v in t:
    print(c,v)


# List Comprehension:
# Liste aller Squares < 5
[v for v in squares if v < 5]

# Liste aller Buchstaben in t
[c for c,v in t]



# Funktion definieren:
def f(n):
    return n + 1

# Funktion ausführen (Positionsbasierte Parameter)
f(2)

# Keywordbasiete Parameter
f(n=2)

# Funktion auf Liste anwenden
[f(n) for n in squares]

# Funktion mit default-Wert definieren (wenn ohne Parameter ausgeführt)
def f(n=1):
    return n + 1

#Keywordbasiete Parameter
f(n=2)

# Funktionen höherer Ordnung:
pairs = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]

# Listenfunktion sort() z.B. lexikografisch sortieren (Lambda wegen Lamba-Kalkül)
pairs.sort(key=lambda pair: pair[1])



# Klassen noch angucken!
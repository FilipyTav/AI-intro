# Mini sistema fuzzy para controlar ventilador baseado na temperatura


# Funções de pertinência (triangulares)
def triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b <= x < c:
        return (c - x) / (c - b)
    return 0


# Conjuntos fuzzy da temperatura
def none(day):
    return triangular(day, 0, 2.5, 4.5)


def few(day):
    return triangular(day, 3.5, 4.5, 5.5)


def lots(day):
    return triangular(day, 4.5, 6.5, 8)


# Regras fuzzy → devolvem intensidade da regra:
def fuzzy_inferencia(day):
    regras = {}
    regras["none"] = none(day)
    regras["few"] = few(day)
    regras["lots"] = lots(day)
    return regras


# Defuzzificação simples (média ponderada)
def defuzzificar(regras):
    valores = {"none": 0, "few": 2, "lots": 4}
    num = 0
    den = 0
    for regra, litters in regras.items():
        num += litters * valores[regra]
        den += litters
    return num / den if den != 0 else 0


days_of_week = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

for i in range(len(days_of_week)):
    amount = fuzzy_inferencia(i + 1)
    saida = defuzzificar(amount)
    print(f"Suggested amount for {days_of_week[i]}: {saida} litters")

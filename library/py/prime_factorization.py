# Разложение на простые множители (Prime Factorization)
# Ключевые слова: факторизация, простые множители, делители, prime factorization, trial division
# Сложность: O(√n) для факторизации одного числа
# Описание: Находит разложение числа n на простые множители и их степени

from collections import defaultdict

# ============ НАЧАЛО КОПИРУЕМОГО БЛОКА ============

def factorize(n):
    factors = defaultdict(int)
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] += 1
            n //= d
        d += 1
    if n > 1:
        factors[n] += 1
    return dict(factors)

def get_prime_divisors(n):
    primes = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            primes.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        primes.append(n)
    return primes

def count_divisors(n):
    factors = factorize(n)
    result = 1
    for power in factors.values():
        result *= (power + 1)
    return result

# ============ КОНЕЦ КОПИРУЕМОГО БЛОКА ============

# ============ РЕАЛИЗАЦИЯ С КОММЕНТАРИЯМИ ============

def factorize(n):
    """
    Факторизация числа n методом пробного деления
    Возвращает dict: простой делитель -> степень
    Пример: 360 = 2³ × 3² × 5 → {2: 3, 3: 2, 5: 1}
    """
    factors = defaultdict(int)
    d = 2

    # Перебираем делители от 2 до √n
    while d * d <= n:
        while n % d == 0:
            factors[d] += 1
            n //= d
        d += 1

    # Если n > 1, это простой делитель больше √n
    if n > 1:
        factors[n] += 1

    return dict(factors)

def get_prime_divisors(n):
    """
    Получить все простые делители (без степеней)
    Пример: 360 → [2, 3, 5]
    """
    primes = []
    d = 2

    while d * d <= n:
        if n % d == 0:
            primes.append(d)
            while n % d == 0:
                n //= d
        d += 1

    if n > 1:
        primes.append(n)

    return primes

def count_divisors(n):
    """
    Количество делителей числа n
    Формула: если n = p₁^a₁ × p₂^a₂ × ... × pₖ^aₖ
    то количество делителей = (a₁ + 1) × (a₂ + 1) × ... × (aₖ + 1)
    """
    factors = factorize(n)
    result = 1
    for power in factors.values():
        result *= (power + 1)
    return result

# ============ КОНЕЦ КОММЕНТИРОВАННОЙ ВЕРСИИ ============

# Примеры использования:

def example1():
    """Пример 1: Факторизация числа"""
    n = 360
    factors = factorize(n)

    print(f"{n} = ", end="")
    parts = []
    for prime, power in sorted(factors.items()):
        if power > 1:
            parts.append(f"{prime}^{power}")
        else:
            parts.append(str(prime))
    print(" × ".join(parts))
    # Вывод: 360 = 2^3 × 3^2 × 5

def example2():
    """Пример 2: Только простые делители"""
    n = 100
    primes = get_prime_divisors(n)

    print(f"Простые делители {n}: {primes}")
    # Вывод: Простые делители 100: [2, 5]

def example3():
    """Пример 3: Количество делителей"""
    n = 12  # 12 = 2² × 3
    count = count_divisors(n)

    print(f"Количество делителей {n}: {count}")
    # Вывод: Количество делителей 12: 6
    # Делители: 1, 2, 3, 4, 6, 12

def example4():
    """Пример 4: Задача "сломать делимость" """
    # Найти максимальный делитель p, не делящийся на q
    p, q = 100, 10

    if p % q != 0:
        print(p)
        return

    ans = 0
    q_primes = get_prime_divisors(q)

    for d in q_primes:
        temp = p
        while temp % q == 0:
            temp //= d
        ans = max(ans, temp)

    print(f"Максимальный делитель {p} не делящийся на {q}: {ans}")
    # Вывод: Максимальный делитель 100 не делящийся на 10: 25

if __name__ == "__main__":
    example1()
    example2()
    example3()
    example4()

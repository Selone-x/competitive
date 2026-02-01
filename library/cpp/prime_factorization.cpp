// Разложение на простые множители (Prime Factorization)
// Ключевые слова: факторизация, простые множители, делители, prime factorization, trial division
// Сложность: O(√n) для факторизации одного числа
// Описание: Находит разложение числа n на простые множители и их степени

#include <map>
using namespace std;

// ============ НАЧАЛО КОПИРУЕМОГО БЛОКА ============

map<long long, int> factorize(long long n) {
    map<long long, int> factors;
    for (long long d = 2; d * d <= n; d++) {
        while (n % d == 0) {
            factors[d]++;
            n /= d;
        }
    }
    if (n > 1) {
        factors[n]++;
    }
    return factors;
}

vector<long long> get_prime_divisors(long long n) {
    vector<long long> primes;
    for (long long d = 2; d * d <= n; d++) {
        if (n % d == 0) {
            primes.push_back(d);
            while (n % d == 0) {
                n /= d;
            }
        }
    }
    if (n > 1) {
        primes.push_back(n);
    }
    return primes;
}

long long count_divisors(long long n) {
    auto factors = factorize(n);
    long long result = 1;
    for (auto [prime, power] : factors) {
        result *= (power + 1);
    }
    return result;
}

// ============ КОНЕЦ КОПИРУЕМОГО БЛОКА ============

// ============ РЕАЛИЗАЦИЯ С КОММЕНТАРИЯМИ ============

// Факторизация числа n методом пробного деления
// Возвращает map: простой делитель -> степень
// Пример: 360 = 2³ × 3² × 5 → {2: 3, 3: 2, 5: 1}
map<long long, int> factorize(long long n) {
    map<long long, int> factors;

    // Перебираем делители от 2 до √n
    for (long long d = 2; d * d <= n; d++) {
        while (n % d == 0) {
            factors[d]++;
            n /= d;
        }
    }

    // Если n > 1, это простой делитель больше √n
    if (n > 1) {
        factors[n]++;
    }

    return factors;
}

// Получить все простые делители (без степеней)
// Пример: 360 → [2, 3, 5]
vector<long long> get_prime_divisors(long long n) {
    vector<long long> primes;

    for (long long d = 2; d * d <= n; d++) {
        if (n % d == 0) {
            primes.push_back(d);
            while (n % d == 0) {
                n /= d;
            }
        }
    }

    if (n > 1) {
        primes.push_back(n);
    }

    return primes;
}

// Количество делителей числа n
// Формула: если n = p₁^a₁ × p₂^a₂ × ... × pₖ^aₖ
// то количество делителей = (a₁ + 1) × (a₂ + 1) × ... × (aₖ + 1)
long long count_divisors(long long n) {
    auto factors = factorize(n);
    long long result = 1;
    for (auto [prime, power] : factors) {
        result *= (power + 1);
    }
    return result;
}

// ============ КОНЕЦ КОММЕНТИРОВАННОЙ ВЕРСИИ ============

// Примеры использования:

#include <iostream>
using namespace std;

void example1() {
    // Пример 1: Факторизация числа
    long long n = 360;
    auto factors = factorize(n);

    cout << n << " = ";
    bool first = true;
    for (auto [prime, power] : factors) {
        if (!first) cout << " × ";
        cout << prime;
        if (power > 1) cout << "^" << power;
        first = false;
    }
    cout << "\n"; // Вывод: 360 = 2^3 × 3^2 × 5
}

void example2() {
    // Пример 2: Только простые делители
    long long n = 100;
    auto primes = get_prime_divisors(n);

    cout << "Простые делители " << n << ": ";
    for (long long p : primes) {
        cout << p << " ";
    }
    cout << "\n"; // Вывод: Простые делители 100: 2 5
}

void example3() {
    // Пример 3: Количество делителей
    long long n = 12; // 12 = 2² × 3
    cout << "Количество делителей " << n << ": " << count_divisors(n) << "\n";
    // Вывод: Количество делителей 12: 6
    // Делители: 1, 2, 3, 4, 6, 12
}

void example4() {
    // Пример 4: Задача "сломать делимость"
    // Найти максимальный делитель p, не делящийся на q
    long long p = 100, q = 10;

    if (p % q != 0) {
        cout << p << "\n";
        return;
    }

    long long ans = 0;
    auto q_primes = get_prime_divisors(q);

    for (long long d : q_primes) {
        long long temp = p;
        while (temp % q == 0) {
            temp /= d;
        }
        ans = max(ans, temp);
    }

    cout << "Максимальный делитель " << p << " не делящийся на " << q << ": " << ans << "\n";
    // Вывод: Максимальный делитель 100 не делящийся на 10: 25
}

int main() {
    example1();
    example2();
    example3();
    example4();
    return 0;
}

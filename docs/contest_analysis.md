# Анализ контеста после участия

**Проблема:** После контеста нет структурированного анализа стратегии и распределения времени — есть только поточечный разбор задач (режим практики), но анализа контеста как целого нет.

**Дата:** 2026-02-05
**Статус:** 🔲 Спланировано

---

## Сценарий использования

Пользователь участвовал в контесте на Codeforces. После окончания он хочет понять не просто "какую задачу решил / не решил", а: была ли стратегия выбора задач оптимальна, где потратил время впустую, какие паттерны ошибок проявились на уровне всего контеста.

### Пошаговый сценарий

```
$ /coach contest 1234
```

1. Claude запускает расширенный `codeforces_api.py` с аргументом `--contest`:
   ```
   python3 codeforces_api.py --contest myhandle 1234
   ```
   Фетчит `user.status` (фильтр по `contestId=1234`) и `contest.standings` (список задач контеста с рейтингом и тегами).

2. Claude показывает загруженные данные в табличном виде:
   ```
   Контест 1234 — результаты myhandle
   ─────────────────────────────────────────────────
   Задача │ Попытки │ Verdict │ Время (мин) │ Теги
   ─────────────────────────────────────────────────
   A      │ 1       │ OK      │ 5           │ greedy
   B      │ 2       │ OK      │ 15          │ dp
   C      │ 3       │ OK      │ 30          │ graphs
   D      │ 1       │ WA      │ —           │ dp, trees
   E      │ 0       │ —       │ —           │ flows
   F      │ 0       │ —       │ —           │ geometry
   ─────────────────────────────────────────────────
   Итого: 3 решено, 1 попытка без AC, 2 не брали
   ```

3. Для каждой **нерешённой** задачи (D, E, F) Claude задаёт вопрос:
   ```
   D (dp, trees) — почему не решил? Где застрял?
   > Не видел как сделать DP по дереву, пробовал жадно — не сошёлся

   E (flows) — почему не решил?
   > Пропустил, слишком сложно для моего уровня

   F (geometry) — почему не решил?
   > Не брался вообще, не хватило времени
   ```
   Каждый ответ опционален — можно просто Enter для пропуска.

4. Один общий вопрос:
   ```
   Как выбирал задачи? В каком порядке решал? Был ли план?
   > Начал с A, потом B, C по порядку. После C попытался D но не пошёл,
     оставшуюся часть времени потратил на D.
   ```

5. Claude генерирует анализ (см. раздел "Дизайн" ниже).

6. Анализ сохраняется в `editorials/contests/1234_analysis.md`.

7. `stats.json` обновляется: новая запись в `contest_history`.

---

## Дизайн

### Структура генерируемого анализа

Пример output для контеста 1234:

```markdown
# Анализ контеста 1234

**Дата:** 2026-02-05
**Результат:** 3/6 задач решено

---

## Стратегия выбора задач

Порядок решения: A → B → C → D (не решено).
Стратегия: последовательная по индексу (A, B, C, ...).

**Оценка:** Оптимально для первых трёх задач — A, B, C набирают очки быстро.
Однако после C (30 мин на решение) было потрачено остаток времени на D,
хотя D была явно сложнее текущего уровня (dp по деревьям).
Альтернатива: попробовать E или пропустить D быстрее и вернуться к ней позже.

## Распределение времени

| Задача | Время (мин) | Оценка |
|--------|-------------|--------|
| A      | 5           | ✅ Быстро |
| B      | 15          | ✅ Нормально |
| C      | 30          | ⚠️ На грани — больше 20 мин |
| D      | >20 (не решена) | ❌ Потеря времени — застрял |

**Суммарное время на решённые:** 50 мин.
**Время на нерешённые попытки:** остаток контеста (~70 мин на D).
**Вывод:** Слишком много времени на D после того как стало понятно что не решается.

## Паттерны ошибок

Нерешённые задачи по тегам:
- **dp** — D (попытка была, не решил)
- **trees** — D (не видел как DP на дереве)
- **flows** — E (пропущено по уровню)
- **geometry** — F (не брался)

**Слабые места по контесту:** dp на деревьях — нужна практика.

## Ключевые моменты

- ✅ Быстро решил A и B — базовые задачи не тормозят
- ⚠️ C заняла 30 минут — рисковая граница, но решена
- ❌ D: застрял на DP по дереву, потратил много времени без прогресса
- 💡 Рекомендация: установить личный лимит ~20 мин на задачу.
  Если нет прогресса — пропуск и возврат.
```

### Правило "потери времени"

Если на задачу потрачено больше 20 минут без AC — это потенциальная потеря. Анализ выделяет такие задачи явно.

---

## Расширения системы

### Новые функции в `codeforces_api.py`

Существующий класс `CodeforcesAPI` использует `_make_request` с rate limiting (2 сек между запросами). Новые методы добавляются как методы класса, не меняя существующие:

```python
def get_contest_submissions(self, handle, contest_id):
    """Фильтр user.status по contestId → per-problem статистика"""
    submissions = self._make_request("user.status", {"handle": handle})

    contest_subs = [s for s in submissions if s.get("problem", {}).get("contestId") == contest_id]

    # Группировка по задаче (индексу)
    problems = {}
    for sub in contest_subs:
        index = sub["problem"]["index"]
        if index not in problems:
            problems[index] = {"attempts": 0, "verdict": None, "time_min": None, "tags": sub["problem"].get("tags", [])}
        problems[index]["attempts"] += 1
        if sub["verdict"] == "OK" and problems[index]["verdict"] != "OK":
            problems[index]["verdict"] = "OK"
            # creationTimeSeconds — время с начала контеста в секундах
            problems[index]["time_min"] = sub.get("creationTimeSeconds", 0) // 60
        elif problems[index]["verdict"] != "OK":
            problems[index]["verdict"] = sub["verdict"]

    return problems

def get_contest_problems(self, contest_id):
    """contest.standings → список задач контеста с рейтингом и тегами"""
    result = self._make_request("contest.standings", {"contestId": contest_id, "showUnused": "true"})
    problems = result.get("problems", [])
    return [{"index": p["index"], "name": p["name"], "rating": p.get("rating"), "tags": p.get("tags", [])} for p in problems]
```

Новый режим запуска в `main()`:
```python
# python3 codeforces_api.py --contest <handle> <contest_id>
if sys.argv[1] == "--contest":
    handle, contest_id = sys.argv[2], int(sys.argv[3])
    api = CodeforcesAPI()
    subs = api.get_contest_submissions(handle, contest_id)
    problems = api.get_contest_problems(contest_id)
    print(json.dumps({"submissions": subs, "problems": problems}, indent=2))
```

### Новые поля в `stats.json`

```json
"contest_history": [
  {
    "date": "2026-02-05",
    "contest_id": 1234,
    "contest_name": "Codeforces Round 1234",
    "problems_attempted": ["A", "B", "C", "D"],
    "problems_solved": ["A", "B", "C"],
    "time_per_problem_min": {"A": 5, "B": 15, "C": 30, "D": null},
    "strategy_notes": "Последовательный порядок A→B→C→D. Слишком долго на D.",
    "weak_topics_detected": ["dp", "trees"],
    "analysis_file": "editorials/contests/1234_analysis.md"
  }
]
```

Поле `contest_history` — новый массив, не конфликтует с существующими полями (`topics_history`, `total_stats`, `monthly_summaries`, `codeforces_sync`).

---

## Интеграция с существующей системой

| Компонент | Что меняется | Как |
|-----------|--------------|-----|
| `codeforces_api.py` | +2 метода в `CodeforcesAPI`, +новый режим в `main()` | Не трогаем существующие методы (`get_user_info`, `get_solved_problems`, `analyze_user_stats`) |
| `stats.json` | +поле `contest_history` | Новый массив, не конфликтует с существующими полями |
| `SKILL.md` | +секция "Режим контеста" | Аргумент `contest {contest_id}` к команде `/coach` |
| `core.json` | не меняется | Контест — это history, не текущее состояние |
| `editorials/` | +директория `contests/` | Файлы `{contest_id}_analysis.md` |

---

## План реализации

### Этап 1: Расширение API
- [ ] Добавить метод `get_contest_submissions(handle, contest_id)` в `CodeforcesAPI`
- [ ] Добавить метод `get_contest_problems(contest_id)` в `CodeforcesAPI`
- [ ] Добавить режим `--contest` в `main()`
- [ ] Протестировать на реальном контесте

### Этап 2: Логика анализа в SKILL.md
- [ ] Описать сценарий команды `/coach contest {contest_id}`
- [ ] Логика табличного вывода данных из API
- [ ] Логика диалога: вопросы про нерешённые задачи + общий вопрос про стратегию
- [ ] Логика генерации анализа (стратегия, время, паттерны, ключевые моменты)

### Этап 3: Сохранение результатов
- [ ] Создать директорию `editorials/contests/`
- [ ] Генерация файла `{contest_id}_analysis.md`
- [ ] Обновление `stats.json`: добавление записи в `contest_history`

### Этап 4: Тестирование
- [ ] Тест на реальном контесте с известными результатами
- [ ] Проверить корректность парсинга времени из `creationTimeSeconds`
- [ ] Проверить работу при пропущенных задачах (0 попыток)
- [ ] Проверить пропуск ответов на вопросы (Enter без текста)

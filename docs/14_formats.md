# Форматы файлов и шаблоны

## Обзор

Документ описывает форматы всех файлов в системе Claude Coach.

## solution/PROBLEM.md

### Формат

```markdown
# Ссылка на задачу
[URL задачи на Codeforces/AtCoder/etc.]

---

# Разбор
[Текст разбора или пусто]
```

### Режимы

**Режим помощи** - "Разбор" пустой:
- Claude консультирует при решении
- Не даёт подсказок проактивно

**Режим объяснения** - "Разбор" заполнен:
- Claude объясняет готовое решение
- Выделяет ключевые идеи

### Пример

```markdown
# Ссылка на задачу
https://codeforces.com/problemset/problem/1234/D

---

# Разбор

```

## solution/CONTEST.md

### Формат

```markdown
# Ссылка на контест
[URL контеста на Codeforces]

---

# Тип контеста
solo

---

# Команда

## Ваш handle
[Ваш handle]

## Участники команды (только для team)
[Handle участника 1]
[Handle участника 2]
```

### Типы

- `solo` - индивидуальный контест
- `team` - командный контест (2-3 человека)

### Примеры

**Solo:**
```markdown
# Ссылка на контест
https://codeforces.com/contest/2062

---

# Тип контеста
solo

---

# Команда

## Ваш handle
tourist

## Участники команды (только для team)

```

**Team:**
```markdown
# Ссылка на контест
https://codeforces.com/contest/1234

---

# Тип контеста
team

---

# Команда

## Ваш handle
tourist

## Участники команды (только для team)
Petr
vepifanov
```

## coach/core.json

### Структура

```json
{
  "version": "2.0",
  "initialized_at": "2026-02-08T10:30:00Z",
  "last_updated": "2026-02-08T11:45:00Z",
  "user_info": {
    "codeforces_handle": "tourist",
    "has_existing_library": true,
    "preferred_language": "cpp",
    "worked_with_claude": true
  },
  "knowledge_assessment": {
    "topic_confidence": {
      "binary_search": 9,
      "two_pointers": 8,
      "sorting": 7,
      "dynamic_programming": 4,
      "graphs_dfs_bfs": 5,
      "greedy": 3,
      "number_theory": 2,
      "data_structures": 6,
      "strings": 3,
      "geometry": 1
    },
    "weak_topics": ["greedy", "number_theory", "dp", "strings", "geometry"],
    "strong_topics": ["binary_search", "two_pointers"]
  },
  "codeforces_analysis": {
    "rating": 1456,
    "rank": "specialist",
    "solved_count": 247,
    "frequent_tags": ["implementation", "greedy", "dp"],
    "rare_tags": ["geometry", "strings", "flows"],
    "last_sync": "2026-02-08T11:30:00Z"
  },
  "training_plan": {
    "current_phase": "intermediate",
    "target_rating": 1600,
    "focus_areas": ["greedy", "number_theory", "dp"],
    "weekly_goals": {
      "problems_per_week": 12,
      "learning_sessions_per_week": 2
    },
    "strategy": "focus_weak"
  },
  "recent_summary": [
    {
      "date": "2026-02-05",
      "type": "learning",
      "topic": "greedy",
      "result": "4/5 quiz"
    }
  ]
}
```

## coach/stats.json

### Структура

```json
{
  "version": "2.0",
  "topics_history": {
    "greedy": {
      "attempts": 15,
      "solved": 6,
      "last_practice": "2026-02-05T10:30:00Z",
      "avg_difficulty": 1400
    }
  },
  "total_stats": {
    "problems_solved": 247,
    "problems_attempted": 485,
    "ac_rate": 51,
    "learning_sessions": 12,
    "drill_sessions": 25,
    "contests_analyzed": 5
  },
  "codeforces_sync": {
    "last_sync": "2026-02-08T11:30:00Z",
    "rating_history": [
      {"date": "2026-02-01", "rating": 1456},
      {"date": "2026-02-08", "rating": 1472}
    ]
  },
  "session_history": [],
  "drill_history": [],
  "contest_history": [],
  "team_contest_history": []
}
```

## editorials/{task}_editorial.md

### Формат

```markdown
# Ссылка
[URL]

---

# Теги
#topic1 #topic2

---

# Что я понял правильно

- Пункт 1
- Пункт 2

---

# Пропущенный шаг

### Ложное предположение
[Описание]

### Ошибка в мышлении
[Описание]

Критический вопрос:
> _«[Вопрос]»_

---

# Правильное решение

1. Шаг 1
2. Шаг 2

Ключевая мысль:
> **[Идея]**

Признаки задачи:
- Признак 1

➡️ **[Вывод]**

---

# Что подтянуть

- Тема 1
```

## editorials/{topic}/index.md

### Формат (Карта знаний)

```markdown
# Тема - Карта знаний

## Обзор темы
[Описание]

## Карта концепций
```
[ASCII граф связей]
```

## Навигация по заметкам

### Базовые концепции
1. [[01_concept]] - описание

### Продвинутые техники
2. [[02_concept]] - описание

## Быстрый старт

Новичок? Начни с [[01_concept]]

## Типичные задачи

- Задача 1
- Задача 2
```

## editorials/{topic}/{N}_concept.md

### Формат (Атомарная заметка)

```markdown
# Название концепции

## Какую задачу решает
[Описание проблемы]

## Суть
[Интуитивное объяснение]

## Пример
[Конкретный пример с разбором]

## Реализация
[Простой код или ссылка на library/]

## Сложность
Время: O(...)
Память: O(...)

## Связи
- [[другая_заметка]] - описание связи
```

## library/{lang}/{algorithm}.cpp

### Формат

```cpp
// [Название]
// Ключевые слова: keyword1, keyword2
// Сложность: O(...)
// Описание: [краткое описание]

// ============ НАЧАЛО КОПИРУЕМОГО БЛОКА ============
[Чистый код БЕЗ комментариев]
// ============ КОНЕЦ КОПИРУЕМОГО БЛОКА ============

// ============ РЕАЛИЗАЦИЯ С КОММЕНТАРИЯМИ ============
[Тот же код С комментариями]
// ============ КОНЕЦ КОММЕНТИРОВАННОЙ ВЕРСИИ ============

// Примеры использования
[Примеры]
```

## editorials/{contest_id}_analysis.md (solo)

### Формат

```markdown
# Анализ контеста {id}: {название}

**Дата:** [дата]
**Результат:** [X/Y задач]

---

## Стратегия выбора задач
[Порядок, оценка]

---

## Распределение времени
[Таблица]

---

## Паттерны ошибок
### Нерешённые задачи
[Анализ каждой]

---

## Ключевые моменты
[Выводы]

---

## Связь с профилем
[Слабые темы]

---

## Действия
[Checklist]
```

## editorials/{contest_id}_team_analysis.md (team)

### Формат

```markdown
# Анализ командного контеста {id}

**Дата:** [дата]
**Команда:** [handles]
**Результат:** [X/Y]

---

## Результаты команды
[Таблица с вкладом]

---

## Эффективность команды
[Оценка, дублирование]

---

## Слабые темы команды
[Анализ по участникам]

---

## Рекомендации
### По координации
### По подготовке
### Действия
```

## Шаблоны кода

### solution/cpp/task.cpp

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    // Код решения

    return 0;
}
```

### solution/py/main.py

```python
import sys
input = sys.stdin.readline

def solve():
    # Код решения
    pass

if __name__ == "__main__":
    solve()
```

---

**Все форматы стандартизированы для удобства работы!**

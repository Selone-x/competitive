#!/usr/bin/env python3
"""
Миграция профиля тренера: profile.json (v1) → core.json + stats.json (v2)

Использование:
    python3 scripts/migrate_profile.py [путь_к_profile.json] [директория_вывода]

По умолчанию:
    - Вход:  coach/profile.json
    - Выход: coach/core.json + coach/stats.json

Если профиль v1 не найден — выводит ошибку и завершается.
Если core.json или stats.json уже существуют — создаёт backup перед перезаписью.
"""

import json
import sys
import shutil
from pathlib import Path
from datetime import datetime


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def backup_if_exists(path: Path):
    """Создаёт backup файла с суффиксом .backup если файл существует."""
    if path.exists():
        backup_path = path.with_suffix(".backup.json")
        shutil.copy2(path, backup_path)
        print(f"  Backup создан: {backup_path}")


def migrate(profile_path: Path, output_dir: Path):
    """Миграция profile.json v1 → core.json + stats.json v2."""

    # --- Загрузка исходного профиля ---
    if not profile_path.exists():
        print(f"Ошибка: файл профиля не найден: {profile_path}")
        sys.exit(1)

    profile = load_json(profile_path)

    if profile.get("version") != "1.0":
        print(f"Предупреждение: версия профиля '{profile.get('version')}', "
              f"ожидалась '1.0'. Продолжаем миграцию...")

    # --- Строим core.json ---
    # recent_summary: последние 10 сессий в кратком виде
    session_history = profile.get("session_history", [])
    recent_sessions = session_history[-10:]  # последние 10

    recent_summary = []
    for session in recent_sessions:
        summary_entry = {
            "date": session.get("date", ""),
            "mode": session.get("mode", ""),
        }

        if session.get("mode") == "practice":
            summary_entry["outcome"] = session.get("outcome", "")
            summary_entry["topics"] = session.get("topics_practiced", [])

            # confidence_delta: вычисляем из before/after если есть
            # для practice обычно не хранится явно, оставляем пустым
            summary_entry["confidence_delta"] = {}

        elif session.get("mode") == "learning":
            summary_entry["outcome"] = "completed"
            summary_entry["topics"] = [session.get("topic", "")]

            # confidence_delta из before/after
            topic = session.get("topic", "")
            before = session.get("confidence_before")
            after = session.get("confidence_after")
            if topic and before is not None and after is not None:
                summary_entry["confidence_delta"] = {topic: after - before}
            else:
                summary_entry["confidence_delta"] = {}

        recent_summary.append(summary_entry)

    core = {
        "version": "2.0",
        "initialized_at": profile.get("initialized_at", ""),
        "user_info": {
            "codeforces_handle": profile.get("user_info", {}).get("codeforces_handle", ""),
            "preferred_language": profile.get("user_info", {}).get("preferred_language", "cpp"),
            "worked_with_claude": profile.get("user_info", {}).get("worked_with_claude", False),
        },
        "knowledge_assessment": {
            "topic_confidence": profile.get("knowledge_assessment", {}).get("topic_confidence", {}),
            "weak_topics": profile.get("knowledge_assessment", {}).get("weak_topics", []),
            "strong_topics": profile.get("knowledge_assessment", {}).get("strong_topics", []),
        },
        "training_plan": profile.get("training_plan", {
            "current_phase": "fundamentals",
            "target_rating": 1600,
            "focus_areas": [],
            "weekly_goals": {
                "problems_per_week": 10,
                "learning_sessions_per_week": 2
            },
            "strategy": "balanced"
        }),
        "recent_summary": recent_summary,
        "last_updated": datetime.now().isoformat(),
    }

    # --- Строим stats.json ---
    topics_history = profile.get("topics_history", {})

    # Считаем агрегирующую статистику из session_history
    total_sessions = len(session_history)
    learning_sessions = sum(1 for s in session_history if s.get("mode") == "learning")
    practice_sessions = sum(1 for s in session_history if s.get("mode") == "practice")
    total_solved = sum(1 for s in session_history
                       if s.get("mode") == "practice" and s.get("outcome") == "solved")
    success_rate = (total_solved / practice_sessions * 100) if practice_sessions > 0 else 0

    # Среднее время решения из practice сессий
    practice_times = [s.get("time_spent_minutes", 0) for s in session_history
                      if s.get("mode") == "practice" and s.get("time_spent_minutes")]
    avg_solve_time = sum(practice_times) / len(practice_times) if practice_times else 0

    stats = {
        "version": "2.0",
        "topics_history": topics_history,
        "total_stats": {
            "total_sessions": total_sessions,
            "learning_sessions": learning_sessions,
            "practice_sessions": practice_sessions,
            "total_solved": total_solved,
            "success_rate": round(success_rate, 1),
            "avg_solve_time_min": round(avg_solve_time, 1),
            "current_streak_days": 0,   # нельзя точно вычислить из history
            "longest_streak_days": 0,   # нельзя точно вычислить из history
        },
        "monthly_summaries": [],        # заполняется при архивации
        "codeforces_sync": profile.get("codeforces_analysis", {
            "rating": 0,
            "solved_count": 0,
            "tags_distribution": {},
            "frequent_tags": [],
            "rare_tags": [],
            "last_sync": "",
        }),
        "session_history": session_history,  # полная история переносится в stats
    }

    # --- Сохранение ---
    output_dir.mkdir(parents=True, exist_ok=True)

    core_path = output_dir / "core.json"
    stats_path = output_dir / "stats.json"

    backup_if_exists(core_path)
    backup_if_exists(stats_path)

    save_json(core_path, core)
    save_json(stats_path, stats)

    print(f"\n✅ Миграция завершена!")
    print(f"   core.json  → {core_path}")
    print(f"   stats.json → {stats_path}")
    print(f"\n   recent_summary: {len(recent_summary)} записей (из {total_sessions} сессий)")
    print(f"   topics_history: {len(topics_history)} тем")
    print(f"   session_history: {total_sessions} сессий (в stats.json)")
    print(f"\n💡 Старый profile.json остаётся на месте как backup.")
    print(f"   Удалите его вручную после проверки: {profile_path}")


def main():
    # Парсинг аргументов
    profile_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("coach/profile.json")
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("coach")

    print(f"Миграция профиля тренера v1 → v2")
    print(f"  Вход:  {profile_path}")
    print(f"  Выход: {output_dir}/core.json + {output_dir}/stats.json\n")

    migrate(profile_path, output_dir)


if __name__ == "__main__":
    main()

"""Install the synthetic demonstration profile without replacing existing data."""

import json
from datetime import datetime, timedelta
from pathlib import Path

from data.migration.schema_manager import initialize_schema
from data.persistence.factory import get_backend


def main() -> None:
    """Load a portable synthetic profile through the application's persistence API."""
    root = Path(__file__).resolve().parent
    db_path = root / "profiles" / "burndown.db"
    if not initialize_schema(db_path):
        raise RuntimeError("Не удалось создать базу демонстрационного проекта")
    backend = get_backend(db_path=str(db_path))
    payload = json.loads(
        (root / "examples" / "demo-freelance.json").read_text(encoding="utf-8")
    )
    profile = payload["profile_data"]
    profile_id = profile["id"]
    query_id = "demo-delivery"
    if backend.get_profile(profile_id):
        print("Демонстрационный профиль уже существует; данные сохранены.")
        return

    now = datetime.now().isoformat()
    profile["created_at"] = now
    profile["last_used"] = now
    backend.save_profile(profile)
    query_data = payload["query_data"]["demo"]
    backend.save_query(
        profile_id,
        {
            "id": query_id,
            "name": "ДЕМО — полная история разработки",
            "jql": "project = DEMO",
            "created_at": now,
            "last_used": now,
        },
    )
    backend.save_statistics_batch(profile_id, query_id, query_data["statistics"])
    backend.save_scope(profile_id, query_id, query_data["project_scope"])
    backend.save_issues_batch(
        profile_id,
        query_id,
        "synthetic-demo",
        query_data["jira_cache"]["issues"],
        datetime.now() + timedelta(days=365),
    )
    backend.set_app_state("active_profile_id", profile_id)
    backend.set_app_state("active_query_id", query_id)
    print("Создан демонстрационный проект: 150 задач, 12 недель истории.")


if __name__ == "__main__":
    main()

"""Russian presentation strings for labels supplied dynamically by data modules.

Only serialized component captions are translated. Store payloads, component IDs,
option values, graph series and all calculation inputs retain their original form.
"""

import json
import re
from typing import Any

from flask import Response, request

_LABELS = {
    "Items Per Week": "Задач в неделю",
    "Points Per Week": "Баллов в неделю",
    "Items Completed": "Выполнено задач",
    "Points Completed": "Выполнено баллов",
    "items/week": "задач/нед.",
    "points/week": "баллов/нед.",
    "points/item": "баллов/задачу",
    "items": "задач",
    "points": "баллов",
    "50% Confidence": "Вероятность 50%",
    "95% Confidence": "Вероятность 95%",
    "Expand Settings": "Открыть настройки",
    "Expand Parameters": "Открыть параметры",
    "Expand Data": "Открыть данные",
    "Close Settings": "Закрыть настройки",
    "Close Parameters": "Закрыть параметры",
    "Close Data": "Закрыть данные",
    "Create or import a profile first.": "Создайте или импортируйте профиль.",
    "Declining throughput": "Темп выполнения снижается",
    "Снижается throughput": "Темп выполнения снижается",
    "Shrinking размер задачи": "Средний размер задачи снижается",
    "Shrinking item size": "Средний размер задачи снижается",
    "Growing item size": "Средний размер задачи растёт",
    "Stable throughput": "Стабильный темп выполнения",
    "Growing throughput": "Темп выполнения растёт",
    "AT RISK": "ПОД РИСКОМ",
    "HEALTHY": "В НОРМЕ",
    "ON TRACK": "ПО ПЛАНУ",
    "BEHIND PACE": "ОТСТАВАНИЕ",
    (
        "Tracks new items added vs completed • Monitors backlog growth over "
        "project lifecycle"
    ): "Сравнение новых и выполненных задач • Контроль роста бэклога",
}

_PHRASES = {
    "Backlog Burn-Down Accelerating - ": "Бэклог сокращается — ",
    "Completing items faster than new additions for ": "Темп опережает прирост: ",
    "Completing items ": "Задачи выполняются ",
    "No data available. Please load project data first.": "Сначала загрузите данные.",
    "Consistency + stability metrics": "Стабильность темпа и тренда",
    "High values (80%+) enable reliable forecasting": "Надёжность выше при 80%+",
    "faster than new additions for ": "быстрее появления новых уже ",
    "High Scope Growth over ": "Рост объёма за ",
    "weeks - For every completed item, ": "нед. — на каждую выполненную задачу ",
    "new items are being created (": "новых задач создаётся (",
    "Using actual data (": "Фактические данные (",
    "Monday": "понедельник",
    "Tuesday": "вторник",
    "Wednesday": "среда",
    "Thursday": "четверг",
    "Friday": "пятница",
    "Saturday": "суббота",
    "Sunday": "воскресенье",
    "(Last 4 Weeks)": "(последние 4 недели)",
    "Trend (last ": "Динамика за ",
    "of historical data used for forecasting": "истории для прогноза",
    " recently (": " за последнее время (",
    " vs ": " против ",
    " of ": " из ",
    " items/week": " задач/нед.",
    " points/week": " баллов/нед.",
    " items": " задач",
    " points": " баллов",
    " weeks": " нед.",
    " AT RISK": " ПОД РИСКОМ",
    "прогноз завершения: завершение через ": "завершение ожидается через ",
}


def translate_caption(text: str) -> str:
    """Translate a display caption without interpreting markup or code."""
    if text in _LABELS:
        return _LABELS[text]
    for source, target in _PHRASES.items():
        text = text.replace(source, target)
    text = text.replace("нед.):", "нед.:")
    return re.sub(r"\b(\d+)w\b", r"\1 нед.", text)


def _translate_children(value: Any) -> Any:
    """Translate nested child lists without entering component property dicts."""
    if isinstance(value, str):
        return translate_caption(value)
    if isinstance(value, list):
        return [_translate_children(item) for item in value]
    return value


def localize_components(value: Any) -> Any:
    """Copy a Dash JSON tree, changing component presentation properties only."""
    if isinstance(value, list):
        return [localize_components(item) for item in value]
    if not isinstance(value, dict):
        return value
    if (
        value.get("namespace") == "dash_core_components"
        and value.get("type") == "Store"
    ):
        return value
    result = {key: localize_components(item) for key, item in value.items()}
    if "namespace" not in value or not isinstance(value.get("props"), dict):
        return result
    props = result["props"]
    for key in ("children", "title", "placeholder", "aria-label"):
        caption = props.get(key)
        if isinstance(caption, str):
            props[key] = translate_caption(caption)
        elif key == "children" and isinstance(caption, list):
            props[key] = _translate_children(caption)
    for option in props.get("options") or []:
        if isinstance(option, dict) and isinstance(option.get("label"), str):
            option["label"] = translate_caption(option["label"])
    return result


def localize_dash_response(response: Response) -> Response:
    """Localize Dash component responses, leaving exports and APIs unchanged."""
    if request.path not in {"/_dash-layout", "/_dash-update-component"}:
        return response
    if not response.is_json:
        return response
    payload = response.get_json(silent=True)
    if payload is not None:
        response.set_data(json.dumps(localize_components(payload), ensure_ascii=False))
    return response

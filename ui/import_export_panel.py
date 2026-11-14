"""
Import/Export Panel Component

Dedicated component for data import/export functionality.
Separated from main JIRA integration for cleaner UI organization.
"""

import dash_bootstrap_components as dbc
from dash import dcc, html

from ui.button_utils import create_panel_collapse_button


def create_import_export_panel():
    """Create the import/export panel component (content only, no card wrapper)."""
    return html.Div(
        [
            # Import Section
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label(
                                "Импорт данных",
                                className="form-label small text-muted mb-1",
                            ),
                            dcc.Upload(
                                id="upload-data",
                                children=html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.I(
                                                    className=(
                                                        "fas fa-cloud-upload-alt "
                                                        "fa-lg mb-1 text-primary"
                                                    )
                                                ),
                                                html.P(
                                                    "Перетащите файл или нажмите",
                                                    className="mb-0 small",
                                                ),
                                                html.Small(
                                                    "JSON/CSV",
                                                    className="text-muted",
                                                    style={"fontSize": "0.75rem"},
                                                ),
                                            ],
                                            className="text-center py-2",
                                        )
                                    ],
                                ),
                                style={
                                    "position": "relative",
                                    "width": "100%",
                                    "borderWidth": "2px",
                                    "borderStyle": "dashed",
                                    "borderRadius": "8px",
                                    "borderColor": "#dee2e6",
                                    "backgroundColor": "#f8f9fa",
                                    "cursor": "pointer",
                                },
                                multiple=False,
                                accept="application/json,.json,.csv",
                            ),
                        ],
                        md=6,
                    ),
                    dbc.Col(
                        [
                            html.Label(
                                "Экспорт данных",
                                className="form-label small text-muted mb-1",
                            ),
                            dbc.Button(
                                [
                                    html.I(className="fas fa-download me-2"),
                                    "Экспорт данных",
                                ],
                                id="export-project-data-button",
                                color="secondary",
                                className="w-100",
                                size="md",
                            ),
                            dcc.Download(id="export-project-data-download"),
                        ],
                        md=6,
                    ),
                ],
                className="g-3",
            ),
        ]
    )


def _create_import_export_tab():
    """Create simplified Import/Export tab with JSON data and metrics."""
    return html.Div(
        [
            # Import Section
            html.Div(
                [
                    html.I(className="fas fa-file-import me-2 text-primary"),
                    html.Span("Импорт данных проекта", className="fw-bold"),
                ],
                className="d-flex align-items-center mb-2",
            ),
            html.P(
                "Загрузите JSON проекта со статистикой и метриками",
                className="text-muted small mb-2",
                style={"fontSize": "0.8rem"},
            ),
            dcc.Upload(
                id="upload-data",
                children=html.Div(
                    [
                        html.I(
                            className="fas fa-cloud-upload-alt fa-lg mb-1 text-primary"
                        ),
                        html.P(
                            "Перетащите JSON-файл или нажмите для выбора",
                            className="mb-1 fw-medium",
                            style={"fontSize": "0.85rem"},
                        ),
                        html.Small(
                            html.Span(".json", className="badge bg-primary"),
                            className="text-muted",
                        ),
                    ],
                    className="text-center py-2",
                ),
                style={
                    "width": "100%",
                    "borderWidth": "2px",
                    "borderStyle": "dashed",
                    "borderRadius": "8px",
                    "borderColor": "#dee2e6",
                    "backgroundColor": "#f8f9fa",
                    "cursor": "pointer",
                    "transition": "all 0.2s ease",
                },
                multiple=False,
                accept=".json,application/json",
            ),
            # Divider
            html.Hr(className="my-3"),
            # Export Section
            html.Div(
                [
                    html.I(className="fas fa-file-export me-2 text-primary"),
                    html.Span("Экспорт данных проекта", className="fw-bold"),
                ],
                className="d-flex align-items-center mb-2",
            ),
            html.P(
                "Скачайте статистику проекта и рассчитанные метрики в JSON",
                className="text-muted small mb-2",
                style={"fontSize": "0.8rem"},
            ),
            # T013: Export mode selection
            html.Div(
                [
                    html.Label(
                        "Режим экспорта", className="form-label small fw-bold mb-1"
                    ),
                    dbc.RadioItems(
                        id="export-mode-radio",
                        options=[
                            {
                                "label": ("Только настройки и запросы, без данных"),
                                "value": "CONFIG_ONLY",
                            },
                            {
                                "label": ("Полный профиль с данными, включая кэш Jira"),
                                "value": "FULL_DATA",
                            },
                        ],
                        value="CONFIG_ONLY",
                        labelStyle={"display": "block", "marginBottom": "0.35rem"},
                        style={"fontSize": "0.875rem"},
                    ),
                ],
                className="mb-2",
            ),
            # T013: Token inclusion checkbox
            html.Div(
                [
                    dbc.Checkbox(
                        id="include-token-checkbox",
                        label="Включить токен Jira (ВНИМАНИЕ: риск раскрытия доступа)",
                        value=False,  # Default unchecked
                        style={"fontSize": "0.875rem"},
                    ),
                ],
                className="mb-2",
            ),
            # Budget data inclusion checkbox
            html.Div(
                [
                    dbc.Checkbox(
                        id="include-budget-checkbox",
                        label="Включить бюджет",
                        value=False,  # Default unchecked
                        style={"fontSize": "0.875rem"},
                    ),
                ],
                className="mb-2",
            ),
            # Changelog inclusion checkbox
            html.Div(
                [
                    dbc.Checkbox(
                        id="include-changelog-checkbox",
                        label="Включить историю изменений",
                        value=False,  # Default unchecked
                        style={"fontSize": "0.875rem"},
                    ),
                ],
                className="mb-2",
            ),
            html.Div(
                [
                    dbc.Button(
                        [
                            html.I(className="fas fa-download me-2"),
                            html.Span("Экспорт данных"),
                        ],
                        id="export-profile-button",
                        color="primary",
                        className="action-button",
                    ),
                ],
                style={"marginBottom": "1rem"},
            ),
            dcc.Download(id="export-profile-download"),
            # Import status alert
            dbc.Alert(
                id="import-status-alert",
                is_open=False,
                dismissable=True,
                duration=8000,
            ),
            # T013: Token warning modal
            dbc.Modal(
                [
                    dbc.ModalHeader("Предупреждение безопасности"),
                    dbc.ModalBody(
                        [
                            html.P("Including your JIRA token in the export will:"),
                            html.Ul(
                                [
                                    html.Li(
                                        "Allow anyone with the file "
                                        "to access your JIRA instance"
                                    ),
                                    html.Li(
                                        "Expose your credentials if file "
                                        "is shared or leaked"
                                    ),
                                    html.Li(
                                        "Grant full API access until token is revoked"
                                    ),
                                ]
                            ),
                            html.P("Only proceed if:", className="fw-bold mt-3"),
                            html.Ul(
                                [
                                    html.Li(
                                        "This is a personal backup on a secure device"
                                    ),
                                    html.Li("You will not share this file with others"),
                                    html.Li(
                                        "You understand how to revoke "
                                        "the token if needed"
                                    ),
                                ]
                            ),
                        ]
                    ),
                    dbc.ModalFooter(
                        [
                            dbc.Button(
                                "Отмена", id="token-warning-cancel", color="secondary"
                            ),
                            dbc.Button(
                                "Понятно, продолжить",
                                id="token-warning-proceed",
                                color="danger",
                            ),
                        ]
                    ),
                ],
                id="token-warning-modal",
                is_open=False,
            ),
            # T050: Profile conflict resolution modal
            dbc.Modal(
                [
                    dbc.ModalHeader("Профиль уже существует"),
                    dbc.ModalBody(
                        [
                            html.P(
                                [
                                    "A profile with this name already exists: ",
                                    html.Strong(id="conflict-profile-name"),
                                ],
                                className="mb-3",
                            ),
                            html.P("Как продолжить?", className="fw-bold"),
                            dbc.RadioItems(
                                id="conflict-resolution-strategy",
                                options=[
                                    {
                                        "label": [
                                            html.Strong("Объединить: "),
                                            "Combine configurations and "
                                            "preserve local JIRA credentials",
                                        ],
                                        "value": "merge",
                                    },
                                    {
                                        "label": [
                                            html.Strong("Заменить: "),
                                            "Replace existing profile completely "
                                            "(WARNING: local credentials will be lost)",
                                        ],
                                        "value": "overwrite",
                                    },
                                    {
                                        "label": [
                                            html.Strong("Переименовать: "),
                                            "Import as a new profile with custom name",
                                        ],
                                        "value": "rename",
                                    },
                                ],
                                value="merge",  # Smart default: preserve credentials
                                className="mb-3",
                            ),
                            # New name input field
                            # shown only when "Rename" is selected
                            html.Div(
                                [
                                    dbc.Label(
                                        "Название нового профиля:",
                                        className="fw-bold mb-2",
                                    ),
                                    dbc.Input(
                                        id="conflict-rename-input",
                                        type="text",
                                        placeholder="Название нового профиля",
                                        className="mb-2",
                                    ),
                                    html.Small(
                                        "Leave empty to auto-generate name "
                                        "with timestamp",
                                        className="text-muted",
                                    ),
                                ],
                                id="conflict-rename-section",
                                style={"display": "none"},  # Hidden by default
                                className="mb-3 p-3 bg-light rounded",
                            ),
                            html.Div(
                                [
                                    html.I(
                                        className="fas fa-info-circle me-2 text-info"
                                    ),
                                    html.Small(
                                        "Merge is recommended for config imports "
                                        "to preserve your JIRA token",
                                        className="text-muted",
                                    ),
                                ],
                                className="alert alert-info py-2",
                            ),
                        ]
                    ),
                    dbc.ModalFooter(
                        [
                            dbc.Button(
                                "Отменить импорт",
                                id="conflict-cancel",
                                color="secondary",
                            ),
                            dbc.Button(
                                "Продолжить",
                                id="conflict-proceed",
                                color="primary",
                            ),
                        ]
                    ),
                ],
                id="conflict-resolution-modal",
                is_open=False,
            ),
            # Store for import data between callbacks (T050)
            dcc.Store(id="import-data-store"),
        ],
        className="settings-tab-content",
    )


def _create_reports_tab():
    """Create simplified Reports tab using Data Points slider value."""
    return html.Div(
        [
            # Report Section Header
            html.Div(
                [
                    html.I(className="fas fa-file-alt me-2"),
                    html.Span("Создать HTML-отчёт", className="fw-bold"),
                ],
                className="d-flex align-items-center mb-2",
            ),
            html.P(
                (
                    "Создайте автономный HTML-файл со всеми метриками для "
                    "передачи заказчику"
                ),
                className="text-muted small mb-2",
                style={"fontSize": "0.8rem"},
            ),
            # Info about time period
            html.Div(
                [
                    html.I(className="fas fa-chart-line me-2 text-white"),
                    html.Span(
                        [
                            "В отчёт войдут данные за ",
                            html.Strong(id="report-weeks-display", children="12"),
                            " нед. shown in your current История данных view",
                        ],
                        style={"fontSize": "0.85rem"},
                    ),
                ],
                className="alert alert-info py-2 mb-3",
                style={"fontSize": "0.8rem"},
            ),
            # Generate button
            html.Div(
                [
                    dbc.Button(
                        [
                            html.I(className="fas fa-download"),
                            html.Span("Создать отчёт"),
                        ],
                        id="generate-report-button",
                        color="primary",
                        className="action-button",
                    ),
                ],
                id="generate-report-button-container",
                style={"marginBottom": "1rem"},
            ),
            dcc.Download(id="report-download"),
            # Hidden elements (kept for backward compatibility with callbacks)
            html.Div(
                [
                    dbc.Checklist(
                        id="report-sections-checklist",
                        options=[],
                        value=["burndown", "dora", "flow", "budget"],
                        style={"display": "none"},
                    ),
                    dbc.RadioItems(
                        id="report-time-period-radio",
                        options=[],
                        value=12,
                        style={"display": "none"},
                    ),
                    html.Div(id="report-size-estimate", style={"display": "none"}),
                ],
                style={"display": "none"},
            ),
        ],
        className="settings-tab-content",
    )


def _create_ai_prompt_tab():
    """Create AI Prompt Generator tab."""
    return html.Div(
        [
            # Header
            html.Div(
                [
                    html.I(className="fas fa-robot me-2 text-primary"),
                    html.Span("Подготовка запроса для анализа ИИ", className="fw-bold"),
                ],
                className="d-flex align-items-center mb-2",
            ),
            html.P(
                "Подготовьте обезличенный запрос для анализа любым ИИ-агентом",
                className="text-muted small mb-2",
                style={"fontSize": "0.8rem"},
            ),
            # Info about time period (mirrors Reports tab)
            html.Div(
                [
                    html.I(className="fas fa-magic me-2 text-white"),
                    html.Span(
                        [
                            "В анализ ИИ войдут данные за ",
                            html.Strong(id="ai-prompt-weeks-display", children="12"),
                            " нед. shown in your current История данных view",
                        ],
                        style={"fontSize": "0.85rem"},
                    ),
                ],
                className="alert alert-info py-2 mb-3",
                style={"fontSize": "0.8rem"},
            ),
            # Privacy notice
            html.Div(
                [
                    html.I(className="fas fa-shield-alt me-2"),
                    html.Span(
                        "All customer-identifying data is automatically "
                        "sanitized before prompt generation.",
                        style={"fontSize": "0.85rem"},
                    ),
                ],
                className="alert alert-secondary py-2 mb-3",
                style={"fontSize": "0.8rem"},
            ),
            # Generate button (matches other action buttons)
            html.Div(
                [
                    dbc.Button(
                        [
                            html.I(className="fas fa-robot"),
                            html.Span("Подготовить запрос для ИИ"),
                        ],
                        id="generate-ai-prompt-button",
                        color="primary",
                        className="action-button",
                    ),
                ],
                style={"marginBottom": "1rem"},
            ),
        ],
        className="settings-tab-content",
    )


def create_import_export_flyout(is_open: bool = False):
    """
    Create a flyout panel for import/export functionality.

    This creates a separate collapsible panel similar to the settings panel
    for data management operations.

    Args:
        is_open: Whether panel should start in expanded state

    Returns:
        html.Div: Complete import/export flyout panel
    """
    return html.Div(
        [
            # Collapsible import/export panel content (drops down from button)
            dbc.Collapse(
                html.Div(
                    [
                        # Tabs row with collapse button
                        html.Div(
                            [
                                # Collapse button (positioned absolutely,
                                # so order does not depend on order here)
                                create_panel_collapse_button("import-export-collapse"),
                                # Tabbed interface matching Settings panel
                                dbc.Tabs(
                                    [
                                        dbc.Tab(
                                            label="Отчёты",
                                            tab_id="reports-tab",
                                            children=_create_reports_tab(),
                                        ),
                                        dbc.Tab(
                                            label="Импорт/экспорт",
                                            tab_id="import-export-tab",
                                            children=_create_import_export_tab(),
                                        ),
                                        dbc.Tab(
                                            label="Запрос для ИИ",
                                            tab_id="ai-prompt-tab",
                                            children=_create_ai_prompt_tab(),
                                        ),
                                    ],
                                    id="data-tabs",
                                    active_tab="reports-tab",
                                    className="settings-tabs",
                                ),
                            ],
                            className="panel-tabs-container",
                        ),
                    ],
                    className="tabbed-settings-panel blue-accent-panel",
                ),
                id="import-export-collapse",
                is_open=is_open,
            ),
        ],
        id="import-export-panel",
        className="import-export-panel-container",
    )

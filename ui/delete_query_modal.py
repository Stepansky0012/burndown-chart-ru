"""
Delete Query Confirmation Modal

Confirms query deletion with clear warnings about data loss.
Shows what will be permanently deleted.
"""

import dash_bootstrap_components as dbc
from dash import html


def create_delete_query_modal() -> dbc.Modal:
    """
    Create modal for confirming query deletion.

    Shows:
    - Query name and JQL being deleted
    - Explicit warning about data loss
    - Cannot undo message

    Returns:
        dbc.Modal component
    """
    return dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.ModalTitle(
                    [
                        html.I(className="fas fa-trash text-danger me-2"),
                        "Удалить запрос",
                    ]
                ),
                close_button=True,
            ),
            dbc.ModalBody(
                [
                    html.P(
                        "Удалить этот запрос?",
                        className="mb-3",
                    ),
                    # Query Details
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Strong("Запрос: "),
                                    html.Span(
                                        id="delete-query-name",
                                        className="text-primary",
                                    ),
                                ],
                                className="mb-2",
                            ),
                        ],
                        className="p-3 bg-light border rounded mb-3",
                    ),
                    # Data Loss Warning
                    dbc.Alert(
                        [
                            html.Div(
                                [
                                    html.I(
                                        className="fas fa-exclamation-triangle me-2"
                                    ),
                                    html.Strong("Будут безвозвратно удалены:"),
                                ],
                                className="mb-2",
                            ),
                            html.Ul(
                                [
                                    html.Li("Кэш данных Jira"),
                                    html.Li("Рассчитанные метрики"),
                                    html.Li("Статистика выгорания"),
                                    html.Li("Все файлы этого запроса"),
                                ],
                                className="mb-2",
                            ),
                            html.Div(
                                [
                                    html.I(className="fas fa-ban me-2"),
                                    html.Strong("Это действие нельзя отменить."),
                                ],
                                className="text-danger",
                            ),
                        ],
                        color="danger",
                        className="mb-0",
                    ),
                ]
            ),
            dbc.ModalFooter(
                [
                    dbc.Button(
                        "Отмена",
                        id="cancel-delete-query-button",
                        color="secondary",
                        outline=True,
                        className="me-auto",
                    ),
                    dbc.Button(
                        [html.I(className="fas fa-trash me-2"), "Удалить запрос"],
                        id="confirm-delete-query-button",
                        color="danger",
                    ),
                ]
            ),
        ],
        id="delete-jql-query-modal",
        size="md",
        is_open=False,
        backdrop="static",
        centered=True,
    )

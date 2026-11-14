"""JIRA issue link helper compatibility shim.

This module preserves the original UI-layer API while delegating shared
implementation paths to utils.jira_link_utils.
"""

from __future__ import annotations

import logging

from dash import html

from utils import jira_link_utils as _shared

logger = logging.getLogger(__name__)


def get_jira_base_url() -> str | None:
    """Get JIRA base URL from configuration if connection is verified."""
    return _shared.get_jira_base_url()


def construct_jira_issue_url(issue_key: str, base_url: str) -> str:
    """Construct full JIRA issue URL."""
    return _shared.construct_jira_issue_url(issue_key, base_url)


def is_jira_connection_verified() -> bool:
    """Check if JIRA connection has been successfully verified."""
    return get_jira_base_url() is not None


def create_jira_issue_link(
    issue_key: str,
    text: str | None = None,
    className: str | None = None,
    style: dict | None = None,
) -> html.A | html.Span:
    """Create Dash html.A component linking to JIRA issue."""
    display_text = text or issue_key

    base_url = get_jira_base_url()
    if not base_url:
        return html.Span(display_text, className=className, style=style)

    issue_url = construct_jira_issue_url(issue_key, base_url)

    return html.A(
        display_text,
        href=issue_url,
        target="_blank",
        rel="noopener noreferrer",
        className=className,
        style=style,
        title=f"Open {issue_key} in JIRA",
    )


def create_jira_issue_link_html(issue_key: str, text: str | None = None) -> str:
    """Create HTML string for JIRA issue link."""
    display_text = text or issue_key

    base_url = get_jira_base_url()
    if not base_url:
        return display_text

    issue_url = construct_jira_issue_url(issue_key, base_url)

    return (
        f'<a href="{issue_url}" target="_blank"'
        f' rel="noopener noreferrer" title="Open {issue_key} in JIRA">'
        f"{display_text}</a>"
    )


def batch_create_jira_issue_links(
    issue_keys: list[str],
    className: str | None = None,
    style: dict | None = None,
) -> list[html.A | html.Span]:
    """Create multiple JIRA issue links at once."""
    return [
        create_jira_issue_link(issue_key, className=className, style=style)
        for issue_key in issue_keys
    ]

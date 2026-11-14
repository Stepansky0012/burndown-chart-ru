"""Check localization boundaries: captions change, machine data does not."""

from flask import Flask, jsonify

from ui.localization import localize_components, localize_dash_response


def test_dynamic_caption_preserves_internal_properties():
    component = {
        "namespace": "dash_html_components",
        "type": "Span",
        "props": {"id": "items", "children": "Items Per Week", "value": "items"},
    }
    localized = localize_components(component)
    assert localized["props"]["children"] == "Задач в неделю"
    assert localized["props"]["id"] == "items"
    assert localized["props"]["value"] == "items"
    assert component["props"]["children"] == "Items Per Week"


def test_store_and_graph_data_are_preserved():
    store = {
        "namespace": "dash_core_components",
        "type": "Store",
        "props": {"data": {"status": "AT RISK", "items": 47}},
    }
    graph = {
        "namespace": "dash_core_components",
        "type": "Graph",
        "props": {"figure": {"data": [{"name": "items", "y": [103, 47]}]}},
    }
    assert localize_components(store) == store
    assert localize_components(graph) == graph


def test_dropdown_values_remain_english():
    dropdown = {
        "namespace": "dash_core_components",
        "type": "Dropdown",
        "props": {"options": [{"label": "Items Completed", "value": "items"}]},
    }
    option = localize_components(dropdown)["props"]["options"][0]
    assert option == {"label": "Выполнено задач", "value": "items"}


def test_nested_child_lists_translate_status_captions():
    component = {
        "namespace": "dash_html_components",
        "type": "Div",
        "props": {"children": [["AT RISK", 47]]},
    }
    result = localize_components(component)
    assert result["props"]["children"] == [["ПОД РИСКОМ", 47]]


def test_flask_hook_does_not_translate_exports_or_api_data():
    server = Flask(__name__)
    with server.test_request_context("/api/example"):
        response = jsonify({"status": "AT RISK"})
        assert localize_dash_response(response).get_json() == {"status": "AT RISK"}


def test_callback_numeric_values_and_component_id_survive():
    server = Flask(__name__)
    payload = {
        "response": {
            "summary": {
                "children": {
                    "namespace": "dash_html_components",
                    "type": "Span",
                    "props": {
                        "id": "remaining",
                        "children": "47 items",
                        "data-total": 150,
                    },
                }
            }
        },
    }
    with server.test_request_context("/_dash-update-component"):
        translated = localize_dash_response(jsonify(payload)).get_json()
    props = translated["response"]["summary"]["children"]["props"]
    assert props == {"id": "remaining", "children": "47 задач", "data-total": 150}

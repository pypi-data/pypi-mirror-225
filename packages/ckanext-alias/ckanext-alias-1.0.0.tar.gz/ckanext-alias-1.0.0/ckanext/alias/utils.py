from __future__ import annotations

import json
from typing import Any

import ckan.plugins.toolkit as tk

import ckanext.alias.config as alias_config


def extension_is_configured() -> None:
    for dataset_type in alias_config.get_supported_dataset_types():
        if is_schema_has_alias_field(dataset_type):
            continue

        assert None, tk._(
            "Alias extension is enabled, but schema field is not configured. "
            "Please, check ckanext-alias documentation"
        )


def is_schema_has_alias_field(dataset_type: str) -> bool:
    schema: dict[str, Any] | None = tk.h.scheming_get_dataset_schema(dataset_type)

    if not schema:
        return False

    field: dict[str, Any] | None = tk.h.scheming_field_by_name(
        schema["dataset_fields"], alias_config.get_alias_fieldname()
    )

    return field is not None


def parse_alias_field(value: str | list | None) -> list[str]:
    if not value:
        return []

    if isinstance(value, list):
        return value

    try:
        alias_list = json.loads(value)
    except ValueError:
        return [value]

    return alias_list


def get_package_by_alias(alias: str, all_fields: bool = False) -> dict[str, str] | None:
    result = tk.get_action("package_search")(
        {"ignore_auth": True},
        {
            "fq": f'vocab_{alias_config.get_alias_fieldname()}:"{alias}"',
            "fl": "id,name" if not all_fields else "",
            "include_private": True,
        },
    )

    if not result["count"]:
        return

    assert result["count"] == 1, "Multiple datasets with the same alias"

    return result["results"][0]

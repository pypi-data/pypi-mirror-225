from __future__ import annotations

import ckan.plugins.toolkit as tk

CONFIG_AUTO_SAVE_ALIAS = "ckanext.alias.autosave_alias"
DEFAULT_AUTO_SAVE_ALIAS = False

CONFIG_ALIAS_FIELDNAME = "ckanext.alias.alias_fieldname"
DEFAULT_ALIAS_FIELDNAME = "alias"

CONFIG_DATASET_TYPES = "ckanext.alias.dataset_types"
DEFAULT_DATASET_TYPES = "dataset"


def save_alias_automatically() -> bool:
    return tk.asbool(tk.config.get(CONFIG_AUTO_SAVE_ALIAS, DEFAULT_AUTO_SAVE_ALIAS))


def get_alias_fieldname() -> str:
    return tk.config.get(CONFIG_ALIAS_FIELDNAME, DEFAULT_ALIAS_FIELDNAME)


def get_supported_dataset_types() -> list[str]:
    return tk.aslist(tk.config.get(CONFIG_DATASET_TYPES, DEFAULT_DATASET_TYPES))

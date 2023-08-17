from __future__ import annotations

from typing import Any

import ckan.plugins as plugins
import ckan.plugins.toolkit as tk
import ckan.types as types

import ckanext.alias.config as alias_config
import ckanext.alias.utils as alias_utils


@tk.blanket.actions
@tk.blanket.blueprints
@tk.blanket.validators
class AliasPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")
        tk.add_public_directory(config_, "public")
        tk.add_resource("assets", "alias")

    # IConfigurable
    def configure(self, config: types.Config) -> None:
        for dataset_type in alias_config.get_supported_dataset_types():
            if alias_utils.is_schema_has_alias_field(dataset_type):
                continue

            assert None, tk._(
                "Alias extension is enabled, but schema field is not configured. "
                "Please, check ckanext-alias documentation"
            )

    # IPackageController

    def before_dataset_index(self, pkg_dict: dict[str, Any]) -> dict[str, Any]:
        alias_fieldname = alias_config.get_alias_fieldname()

        if not pkg_dict.get(alias_fieldname):
            return pkg_dict

        pkg_dict[f"vocab_{alias_fieldname}"] = alias_utils.parse_alias_field(
            pkg_dict[alias_fieldname]
        )

        return pkg_dict

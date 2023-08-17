from __future__ import annotations

from typing import Any

import ckan.plugins.toolkit as tk
import ckan.tests.factories as factories
import pytest
from ckan.tests.helpers import call_action

import ckanext.alias.config as alias_config
import ckanext.alias.utils as alias_utils


@pytest.mark.usefixtures("with_plugins")
class TestAliasConfiguration:
    @pytest.mark.ckan_config("ckanext.alias.dataset_types", "package")
    def test_extension_is_misconfigured(self):
        with pytest.raises(AssertionError):
            alias_utils.extension_is_configured()

    @pytest.mark.ckan_config("ckanext.alias.dataset_types", "dataset")
    def test_extension_is_configured_properly(self):
        alias_utils.extension_is_configured()


@pytest.mark.usefixtures("reset_db_once", "with_plugins")
class TestAutomaticAlias:
    @pytest.mark.ckan_config("ckanext.alias.autosave_alias", "true")
    def test_automatic_alias_is_enabled(self):
        dataset: dict[str, Any] = factories.Dataset()  # type: ignore
        old_name = dataset["name"]

        dataset = call_action("package_patch", id=dataset["id"], name="name-1")
        assert dataset[alias_config.get_alias_fieldname()] == [old_name]

        dataset = call_action("package_patch", id=dataset["id"], name="name-2")
        assert len(dataset[alias_config.get_alias_fieldname()]) == 2
        assert old_name in dataset[alias_config.get_alias_fieldname()]
        assert "name-1" in dataset[alias_config.get_alias_fieldname()]

    def test_automatic_alias_is_disabled_by_default(self):
        dataset: dict[str, Any] = factories.Dataset()  # type: ignore

        dataset = call_action("package_patch", id=dataset["id"], name="new_name")

        assert alias_config.get_alias_fieldname() not in dataset


@pytest.mark.usefixtures("reset_db_once", "clean_index", "with_plugins")
class TestAliasRedirect:
    def test_without_alias(self, app):
        dataset: dict[str, Any] = factories.Dataset()  # type: ignore

        response = app.get(tk.url_for("dataset.read", id=dataset["name"]))
        assert response.status_code == 200

        response = app.get(tk.url_for("dataset.read", id="xxx"))
        assert response.status_code == 404

    def test_with_alias(self, app):
        dataset: dict[str, Any] = factories.Dataset(alias="xxx")  # type: ignore

        response = app.get(tk.url_for("dataset.read", id=dataset["name"]))
        assert response.status_code == 200

        response = app.get(tk.url_for("dataset.read", id="xxx"))
        assert response.status_code == 200

    def test_with_multiple_aliases(self, app):
        test_aliases = ["alias1", "alias2"]
        dataset: dict[str, Any] = factories.Dataset(alias=test_aliases)  # type: ignore

        response = app.get(tk.url_for("dataset.read", id=dataset["name"]))
        assert response.status_code == 200

        for alias in test_aliases:
            response = app.get(tk.url_for("dataset.read", id=alias))
            assert response.status_code == 200


@pytest.mark.usefixtures("reset_db_once", "clean_index", "with_plugins")
class TestAliasValidators:
    def test_alias_is_not_unique(self):
        with pytest.raises(
            tk.ValidationError, match="Alias must be unique. Remove duplicates"
        ):
            factories.Dataset(alias=["alias", "alias"])

    def test_alias_is_occupied(self):
        factories.Dataset(alias=["alias"])

        with pytest.raises(
            tk.ValidationError, match="Alias 'alias' is already occupied"
        ):
            factories.Dataset(alias=["alias"])

    def test_name_is_occupied_by_alias(self):
        factories.Dataset(alias=["alias"])

        with pytest.raises(
            tk.ValidationError, match="Name 'alias' is already occupied by an alias"
        ):
            factories.Dataset(name="alias")

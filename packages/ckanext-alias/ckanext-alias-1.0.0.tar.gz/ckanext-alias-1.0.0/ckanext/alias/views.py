# encoding: utf-8
from __future__ import annotations

import logging
from typing import Union

from ckan import model
from ckan.common import session as flask_session
from ckan.plugins import toolkit as tk
from ckan.types import Response
from ckan.views import dataset as dataset_view
from flask import Blueprint

import ckanext.alias.utils as alias_utils

log = logging.getLogger(__name__)

dataset = Blueprint(
    "alias_dataset",
    __name__,
    url_prefix="/dataset",
    url_defaults={"package_type": "dataset"},
)


def read(package_type: str, name_or_id: str) -> Union[Response, str]:
    """A custom dataset.read view to handle URL aliases"""
    if flask_session.pop("from_alias", None):
        return dataset_view.read(package_type, name_or_id)

    package = model.Package.get(name_or_id)

    if not package:
        package = alias_utils.get_package_by_alias(name_or_id)
        name_or_id = package["name"] if package else name_or_id
    else:
        return dataset_view.read(package_type, name_or_id)

    flask_session["from_alias"] = True

    return tk.redirect_to("{}.read".format(package_type), id=name_or_id)


dataset.add_url_rule("/<name_or_id>", view_func=read)

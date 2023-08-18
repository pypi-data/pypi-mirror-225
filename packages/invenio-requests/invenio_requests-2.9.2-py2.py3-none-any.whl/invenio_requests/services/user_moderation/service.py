# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""User moderation service."""
from flask import current_app
from invenio_accounts.models import Role
from invenio_i18n import gettext as _
from invenio_records_resources.services.uow import unit_of_work

from invenio_requests.customizations.user_moderation.user_moderation import (
    UserModeration,
)
from invenio_requests.proxies import current_request_type_registry


class UserModerationRequestService:
    """Service for User Moderation requests."""

    def __init__(self, requests_service):
        """Service initialisation as a sub-service of requests."""
        self.requests_service = requests_service

    @property
    def request_type_cls(self):
        """User moderation request type."""
        return current_request_type_registry.lookup(UserModeration.type_id)

    @unit_of_work()
    def request_moderation(self, identity, user_id, data=None, uow=None, **kwargs):
        """Creates a UserModeration request and submits it."""
        REQUESTS_MODERATION_ROLE = current_app.config.get("REQUESTS_MODERATION_ROLE")
        role = Role.query.filter(Role.name == REQUESTS_MODERATION_ROLE).one_or_none()
        assert role, _("Moderation role must exist to enable user moderation requests.")

        data = data or {}

        # For user moderation, topic is the user to be moderated
        topic = {"user": str(user_id)}

        # Receiver can be configured, by default send the request to users with moderation role
        receiver = {"group": role.name}  # TODO to be changed to role id
        creator = {"group": role.name}  # TODO to be changed to role id

        request_item = self.requests_service.create(
            identity,
            data,
            self.request_type_cls,
            receiver,
            creator,
            topic=topic,
            uow=uow,
        )

        # Permission for identity might be denied on 'submit'
        return self.requests_service.execute_action(
            identity=identity, id_=request_item.id, action="submit", data=data, uow=uow
        )

# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.
"""User moderation requests."""

from invenio_i18n import lazy_gettext as _
from invenio_users_resources.proxies import current_users_service

from invenio_requests.customizations import RequestType, actions


class DeclineUserAction(actions.DeclineAction):
    """Represents a decline action used to block an user."""

    def execute(self, identity, uow):
        """Executes block action."""
        user = self.request.topic.resolve()
        current_users_service.block(identity, user.id, uow=uow)
        super().execute(identity, uow)


class AcceptUserAction(actions.AcceptAction):
    """Represents an accept action used to aprove an user."""

    def execute(self, identity, uow):
        """Executes aprove action."""
        user = self.request.topic.resolve()
        current_users_service.approve(identity, user.id, uow=uow)
        super().execute(identity, uow)


class UserModeration(RequestType):
    """Request to moderate an user."""

    type_id = "user-moderation"
    name = _("User moderation")

    creator_can_be_none = False
    topic_can_be_none = False
    allowed_creator_ref_types = ["group"]
    allowed_receiver_ref_types = ["group"]
    allowed_topic_ref_types = ["user"]

    available_actions = {
        "delete": actions.DeleteAction,
        "submit": actions.SubmitAction,
        "create": actions.CreateAction,
        "cancel": actions.CancelAction,
        # Custom implemented actions
        "accept": AcceptUserAction,
        "decline": DeclineUserAction,
    }

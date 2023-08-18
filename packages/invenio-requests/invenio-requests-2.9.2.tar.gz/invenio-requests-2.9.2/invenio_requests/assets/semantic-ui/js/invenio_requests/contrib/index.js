import {
  LabelStatusAccept,
  LabelStatusCancel,
  LabelStatusDecline,
  LabelStatusDelete,
  LabelStatusExpire,
  LabelStatusSubmit,
  LabelTypeCommunityInclusion,
  LabelTypeCommunityInvitation,
  LabelTypeCommunitySubmission,
  LabelTypeGuestAccess,
  LabelTypeUserAccess,
} from "@js/invenio_requests/contrib";
import {
  RequestAcceptButton,
  RequestCancelButton,
  RequestDeclineButton,
} from "@js/invenio_requests/components/Buttons";
import {
  RequestAcceptModalTrigger,
  RequestDeclineModalTrigger,
  RequestCancelModalTrigger,
} from "@js/invenio_requests/components/ModalTriggers";

export const defaultContribComponents = {
  [`RequestTypeLabel.layout.community-submission`]: LabelTypeCommunitySubmission,
  [`RequestTypeLabel.layout.community-inclusion`]: LabelTypeCommunityInclusion,
  [`RequestTypeLabel.layout.community-invitation`]: LabelTypeCommunityInvitation,
  [`RequestTypeLabel.layout.guest-access-request`]: LabelTypeGuestAccess,
  [`RequestTypeLabel.layout.user-access-request`]: LabelTypeUserAccess,
  [`RequestStatusLabel.layout.submitted`]: LabelStatusSubmit,
  [`RequestStatusLabel.layout.deleted`]: LabelStatusDelete,
  [`RequestStatusLabel.layout.accepted`]: LabelStatusAccept,
  [`RequestStatusLabel.layout.declined`]: LabelStatusDecline,
  [`RequestStatusLabel.layout.cancelled`]: LabelStatusCancel,
  [`RequestStatusLabel.layout.expired`]: LabelStatusExpire,
  [`RequestActionButton.cancel`]: RequestCancelButton,
  [`RequestActionButton.decline`]: RequestDeclineButton,
  [`RequestActionButton.accept`]: RequestAcceptButton,
  [`RequestActionModalTrigger.accept`]: RequestAcceptModalTrigger,
  [`RequestActionModalTrigger.decline`]: RequestDeclineModalTrigger,
  [`RequestActionModalTrigger.cancel`]: RequestCancelModalTrigger,
};

export * from "./labels";

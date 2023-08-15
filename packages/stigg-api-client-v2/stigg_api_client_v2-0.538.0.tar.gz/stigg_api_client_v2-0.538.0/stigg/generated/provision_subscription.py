# Generated by ariadne-codegen on 2023-08-14 17:19
# Source: operations.graphql

from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import ProvisionSubscriptionStatus
from .fragments import SlimSubscriptionFragment


class ProvisionSubscription(BaseModel):
    provision_subscription: "ProvisionSubscriptionProvisionSubscription" = Field(
        alias="provisionSubscription"
    )


class ProvisionSubscriptionProvisionSubscription(BaseModel):
    checkout_url: Optional[str] = Field(alias="checkoutUrl")
    status: ProvisionSubscriptionStatus
    subscription: Optional["ProvisionSubscriptionProvisionSubscriptionSubscription"]


class ProvisionSubscriptionProvisionSubscriptionSubscription(SlimSubscriptionFragment):
    pass


ProvisionSubscription.update_forward_refs()
ProvisionSubscriptionProvisionSubscription.update_forward_refs()
ProvisionSubscriptionProvisionSubscriptionSubscription.update_forward_refs()

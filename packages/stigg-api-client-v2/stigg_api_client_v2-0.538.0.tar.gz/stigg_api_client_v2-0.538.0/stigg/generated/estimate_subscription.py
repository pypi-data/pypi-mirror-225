# Generated by ariadne-codegen on 2023-08-14 17:19
# Source: operations.graphql

from pydantic import Field

from .base_model import BaseModel
from .fragments import SubscriptionPreviewFragment


class EstimateSubscription(BaseModel):
    estimate_subscription: "EstimateSubscriptionEstimateSubscription" = Field(
        alias="estimateSubscription"
    )


class EstimateSubscriptionEstimateSubscription(SubscriptionPreviewFragment):
    pass


EstimateSubscription.update_forward_refs()
EstimateSubscriptionEstimateSubscription.update_forward_refs()

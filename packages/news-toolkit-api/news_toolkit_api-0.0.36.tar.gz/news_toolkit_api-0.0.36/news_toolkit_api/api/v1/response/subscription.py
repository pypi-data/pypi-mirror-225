from dataclasses import dataclass

from news_toolkit_api.db.subscription import SubscriptionPlan


@dataclass(frozen=True)
class SubscriptionCost:
    monthly: int
    annual: int


@dataclass(frozen=True)
class SubscriptionResponse:
    id: str
    name: SubscriptionPlan
    benefits: list[str]
    cost: SubscriptionCost


@dataclass(frozen=True)
class SubscriptionsResponse:
    subscriptions: list[SubscriptionResponse]

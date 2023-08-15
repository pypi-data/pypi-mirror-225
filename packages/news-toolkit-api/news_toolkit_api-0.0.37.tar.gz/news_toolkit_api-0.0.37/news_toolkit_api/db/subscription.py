from enum import Enum

from google.cloud import ndb


class SubscriptionPlan(Enum):
    NONE = "none"
    BASIC = "basic"
    PLUS = "plus"
    PREMIUM = "premium"


class SubscriptionCost(ndb.Model):
    monthly = ndb.IntegerProperty(required=True)
    annual = ndb.IntegerProperty(required=True)


class Subscription(ndb.Model):
    name = ndb.StringProperty(
        required=True, choices=[plan.value for plan in SubscriptionPlan]
    )
    benefits = ndb.StringProperty(repeated=True)
    cost = ndb.StructuredProperty(SubscriptionCost, required=True)

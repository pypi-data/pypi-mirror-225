from dataclasses import dataclass
from enum import Enum


class BannerAdSize(Enum):
    normal = "normal"
    large = "large"
    extraLarge = "extraLarge"
    anchoredAdaptive = "anchoredAdaptive"


@dataclass(frozen=True)
class BannerAdContent:
    size: BannerAdSize
    type: str = "__banner_ad__"

from dataclasses import dataclass


@dataclass(frozen=True)
class SectionHeaderBlock:
    title: str
    type: str = "__section_header__"

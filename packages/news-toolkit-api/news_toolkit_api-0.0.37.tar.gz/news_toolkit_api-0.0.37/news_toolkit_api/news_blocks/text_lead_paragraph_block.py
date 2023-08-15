from dataclasses import dataclass


@dataclass(frozen=True)
class TextLeadParagraphBlock:
    text: str
    type: str = "__text_lead_paragraph__"

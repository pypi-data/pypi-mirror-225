from dataclasses import dataclass
from typing import List, Optional

import pandas as pd
from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GeneratedResponse:
    prompt: str
    response: str
    raw_prompt: Optional[str] = None
    sample_index: Optional[int] = None
    sample_data: Optional[str] = None
    context: Optional[str] = None
    model_name: Optional[str] = None
    finish_reason: Optional[str] = None
    generated_tokens: Optional[int] = None

    @staticmethod
    def to_responses(df: pd.DataFrame) -> List["GeneratedResponse"]:
        return [GeneratedResponse(**row.to_dict()) for _, row in df.iterrows()]

from typing import Dict, List, Optional

from pydantic import UUID4, BaseModel, Field


class GetRowsRequest(BaseModel):
    project_id: UUID4
    run_id: UUID4


class PromptRow(BaseModel):
    index: int
    prompt: Optional[str] = None
    response: Optional[str] = None
    target: Optional[str] = None
    inputs: Dict[str, Optional[str]] = Field(default_factory=dict)
    hallucination: Optional[float] = None
    bleu: Optional[float] = None
    rouge: Optional[float] = None
    cost: Optional[float] = None
    like_dislike: Optional[bool] = None


class PromptRows(BaseModel):
    rows: List[PromptRow]

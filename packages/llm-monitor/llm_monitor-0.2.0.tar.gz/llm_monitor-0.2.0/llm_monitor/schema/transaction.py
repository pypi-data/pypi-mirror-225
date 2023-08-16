from typing import Dict, List, Optional

from pydantic import BaseModel


class TransactionRecord(BaseModel):
    latency_ms: Optional[int]
    status_code: Optional[int]
    input_text: str
    output_text: Optional[str]
    model: str
    num_input_tokens: Optional[int]
    num_output_tokens: Optional[int]
    output_logprobs: Optional[Dict]
    created_at: str


class TransactionRecordBatch(BaseModel):
    records: List[TransactionRecord]

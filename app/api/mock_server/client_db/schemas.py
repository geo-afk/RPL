from pydantic import BaseModel
from typing import Dict, Any

class RowUpdate(BaseModel):
    field: str
    value: Any

class RowPatch(BaseModel):
    updates: Dict[str, Any]

class TableRow(BaseModel):
    id: int
    class Config:
        from_attributes = True
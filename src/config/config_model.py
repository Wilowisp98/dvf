from dataclasses import dataclass
from typing import Optional, Dict, List, Any

@dataclass
class Config:
    schema: Optional[Dict[str, List[Any]]] = None  # e.g. {'column_name': ['data_type', True/False]}
    primary_keys: Optional[List[str]] = None # e.g. ['column_name_1', 'column_name_2']
    foreign_keys: Optional[List[str]] = None # e.g. ['column_name_1', 'column_name_2']
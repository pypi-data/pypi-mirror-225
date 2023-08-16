from typing import Optional, Any, Dict, List, Tuple, Union

from pydantic import BaseModel, Extra


class InternalApiResponseErrorObj(BaseModel):
    error_type: str
    error_message: str
    error_location: Optional[Union[List[str], str, Tuple[str, ...]]] = None
    error_kind: Optional[str] = None
    other: Optional[Dict[str, Any]] = None

    class Config:
        extra = Extra.ignore
        allow_mutation = False

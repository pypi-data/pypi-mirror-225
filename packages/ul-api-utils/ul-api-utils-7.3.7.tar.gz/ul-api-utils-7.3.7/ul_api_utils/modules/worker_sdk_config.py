from pydantic import BaseModel, Extra


class WorkerSdkConfig(BaseModel):

    class Config:
        extra = Extra.forbid
        allow_mutation = False
        frozen = True
        arbitrary_types_allowed = True

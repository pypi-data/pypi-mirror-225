from immutabledict import immutabledict
from pydantic import BaseModel

from tdm.helper import freeze_dict


class AbstractMarkupModel(BaseModel):
    def immutabledict(self) -> immutabledict:
        return freeze_dict(self.dict(exclude_none=True, exclude_defaults=True))

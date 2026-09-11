from pydantic import BaseModel, Field, ConfigDict
from pydantic_core.core_schema import str_schema

class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=50) # these are like model.py in django where we actually create our schema

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True) # It tells python to read data from attributes not just dictionary

    id: int #we have to avoid using name "id" beacuse it is a builtin in python, but in API and Database it is naming convention standards
    date_posted: str

from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.typing import List, Optional, Annotated


class PromptUpdate(BaseModel):
    title: Optional[str] = Field(min_length=10, max_length=100, example="Sample Title", default=None)
    description: Optional[str] = Field(min_length=10, max_length=500, example="Sample Description",default=None)
    section: Optional[str] = Field(min_length=3, max_length=100, example="Section",default=None)
    tags: Optional[List[str]] = Field(max_length=15, default=None)
    topic: Optional[str] = Field(max_length=50, default=None)
    rating: Optional[int] = Field(ge=0, le=5, default=0)


class Prompt(BaseModel):
    title: str = Field(min_length=10, max_length=100, example="Sample Title")
    description: str = Field(min_length=10, max_length=500, example="Sample Description")
    section: str = Field(min_length=3, max_length=100, example="Section")
    tags: Optional[List[str]] = Field(max_length=15, default=[])
    topic: Optional[str] = Field(max_length=50, default="")
    rating: Optional[int] = Field(ge=0, le=5, default=0)


class PromptSearch(BaseModel):
    search: Annotated[str, None] = Field(default=None, example="")
    page_number: Annotated[int, None] = Field(gt=0, default=1)
    records_per_page: Annotated[int, None] = Field(gt=0, le=100, default=10)
    sort_order: Annotated[str, None] = Field(default="ASC")
    sort_by: Annotated[str, None] = Field(default=None, example="")

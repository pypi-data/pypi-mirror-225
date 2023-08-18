from pydantic import BaseModel, Field


class CreateDemoSchema(BaseModel):
    name: str = Field(..., description='名称')

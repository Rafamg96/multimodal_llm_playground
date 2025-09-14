
from pydantic import BaseModel, Field

class EmbedMarkdown_Request(BaseModel):
    ################################################################################################
    # TODO:
    # The objective of this class is to define the request fields, you can define validators
    ################################################################################################
    dir: str = Field(examples=["outputs/rag/my_collection"], description="Dir to process", min_length=1)
    collection_name: str = Field(examples=["my_collection"], description="Collection name", min_length=1)

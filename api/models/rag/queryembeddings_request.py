
from pydantic import BaseModel, Field

class QueryEmbeddings_Request(BaseModel):
    ################################################################################################
    # TODO:
    # The objective of this class is to define the request fields, you can define validators
    ################################################################################################
    query: str = Field(examples=["¿Cómo puedo optimizar mis videos de youtube? "], description="Query to process", min_length=1)
    collection_name: str = Field(examples=["my_collection"], description="Collection name", min_length=1)

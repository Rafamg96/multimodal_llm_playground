
from pydantic import BaseModel, Field

class ConvertMarkdown_Request(BaseModel):
    ################################################################################################
    # TODO:
    # The objective of this class is to define the predict request fields, you can define validators
    ################################################################################################
    url: str = Field(examples=["https://support.google.com/youtube/answer/9527654?hl=es"], description="URL to process", min_length=1)
    name: str = Field(examples=["Configurar la audiencia de un canal o un vídeo"], description="Name of document", min_length=1)
    collection_name: str = Field(examples=["my_collection"], description="Name of the collection to store embeddings", min_length=1)
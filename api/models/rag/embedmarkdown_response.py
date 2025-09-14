from pydantic import BaseModel, Field


class EmbedMarkdown_ResponseSuccess(BaseModel):
    ################################################################################################
    # TODO:
    # The objective of this class is to define the success response fields
    ################################################################################################

    message: str = Field(examples=["Embedding created successfully"], description="The success message")


class EmbedMarkdown_ResponseError(BaseModel):
    ################################################################################################
    # TODO:
    # The objective of this class is to define the error response fields
    ################################################################################################

    message: str = Field(examples=["Embedding was not created successfully"], description="The error message")


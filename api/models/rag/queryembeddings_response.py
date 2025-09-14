from pydantic import BaseModel, Field


class QueryEmbeddings_ResponseSuccess(BaseModel):
    ################################################################################################
    # TODO:
    # The objective of this class is to define the success response fields
    ################################################################################################

    message: str = Field(examples=["Response generated successfully"], description="The success message")


class QueryEmbeddings_ResponseError(BaseModel):
    ################################################################################################
    # TODO:
    # The objective of this class is to define the error response fields
    ################################################################################################

    message: str = Field(examples=["Response was not generated successfully"], description="The error message")


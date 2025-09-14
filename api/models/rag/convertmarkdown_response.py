from pydantic import BaseModel, Field


class ConvertMarkdown_ResponseSuccess(BaseModel):
    ################################################################################################
    # TODO:
    # The objective of this class is to define the success response fields
    ################################################################################################

    message: str = Field(examples=["Markdown file created successfully"], description="The success message")


class ConvertMarkdown_ResponseError(BaseModel):
    ################################################################################################
    # TODO:
    # The objective of this class is to define the error response fields
    ################################################################################################

    message: str = Field(examples=["Markdown file was not created successfully"], description="The error message")


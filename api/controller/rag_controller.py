from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import logging

from api.helpers.logger_builder import LoggerBuilder
from api.models.rag import (
    ConvertMarkdown_Request,
    ConvertMarkdown_ResponseSuccess,
    ConvertMarkdown_ResponseError,
    EmbedMarkdown_Request,
    EmbedMarkdown_ResponseSuccess,
    EmbedMarkdown_ResponseError,
    QueryEmbeddings_Request,
    QueryEmbeddings_ResponseSuccess,
    QueryEmbeddings_ResponseError
)
from api.service.rag import (
    CreateMarkdown_Service,
    Encode_Markdown_Service,
)

namespace = "RAG"
rag_router = APIRouter(prefix=f"/{namespace}")

logger = logging.getLogger(LoggerBuilder.name)


# Individual processing
@rag_router.post(
    "/create_markdown_url",
    response_model=ConvertMarkdown_ResponseSuccess,
    tags=[namespace],
    responses={
        201: {"model": ConvertMarkdown_ResponseError, "description": "RAG Error"}
    },
)
async def create_markdown_url(request: ConvertMarkdown_Request):
    try:
        create_markdown_service = CreateMarkdown_Service()
        create_markdown_service.create_markdown_from_url(dict(request))
        response = ConvertMarkdown_ResponseSuccess(
            message="Markdown created successfully"
        )
    except Exception as e:
        logger.error(f"Error creating markdown: {e}")
        response = ConvertMarkdown_ResponseError(message="Error creating markdown")

    return JSONResponse(content=jsonable_encoder(response))

# Multiple processing
@rag_router.get(
    "/create_markdown_urls",
    response_model=ConvertMarkdown_ResponseSuccess,
    tags=[namespace],
    responses={
        201: {"model": ConvertMarkdown_ResponseError, "description": "RAG Error"}
    },
)
async def create_markdown_urls():
    try:
        create_markdown_service = CreateMarkdown_Service()
        create_markdown_service.create_markdown_from_urls()
        response = ConvertMarkdown_ResponseSuccess(
            message="Markdowns created successfully"
        )
    except Exception as e:
        logger.error(f"Error creating markdowns: {e}")
        response = ConvertMarkdown_ResponseError(message="Error creating markdowns")

    return JSONResponse(content=jsonable_encoder(response))

@rag_router.post(
    "/embed_markdowns_url",
    response_model=EmbedMarkdown_ResponseSuccess,
    tags=[namespace],
    responses={
        201: {"model": EmbedMarkdown_ResponseError, "description": "Embedding Error"}
    },
)
async def embed_markdowns_url(request: EmbedMarkdown_Request):
    try:
        create_markdown_service = Encode_Markdown_Service()
        create_markdown_service.encode_markdowns_using_chunks(
            markdown_dir_path=request.dir, collection_name=request.collection_name
        )
        response = EmbedMarkdown_ResponseSuccess(
            message="Embedding created successfully"
        )
    except Exception as e:
        logger.error(f"Error creating markdown: {e}")
        response = EmbedMarkdown_ResponseError(message="Error creating embeddings")

    return JSONResponse(content=jsonable_encoder(response))

@rag_router.post(
    "/query_embeddings_and_generate_response",
    response_model=QueryEmbeddings_ResponseSuccess,
    tags=[namespace],
    responses={
        201: {"model": QueryEmbeddings_ResponseError, "description": "Embedding Error"}
    },
)
async def query_embeddings_and_generate_response(request: QueryEmbeddings_Request):
    try:
        create_markdown_service = Encode_Markdown_Service()
        response = create_markdown_service.user_query_using_embeddings(
            query=request.query, collection_name=request.collection_name
        )
        response = QueryEmbeddings_ResponseSuccess(
            message=response
        )
    except Exception as e:
        logger.error(f"Error creating markdown: {e}")
        response = QueryEmbeddings_ResponseError(message="Error creating embeddings")

    return JSONResponse(content=jsonable_encoder(response))
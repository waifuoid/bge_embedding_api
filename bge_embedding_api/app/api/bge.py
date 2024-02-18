from fastapi import APIRouter
from bge_embedding_api.app.models.request import EmbeddingRequest
from bge_embedding_api.library.config import config
from FlagEmbedding import BGEM3FlagModel


router = APIRouter()

model = None


def load_bge_model(model_name, device):
    global model
    model = BGEM3FlagModel(model_name, device=device, use_fp16=True)


@router.get("/v1/embeddings")
async def embeddings(request: EmbeddingRequest):
    if model is None:
        load_bge_model(config.BGE_MODEL_NAME, config.DEVICE)
    embedding_type = request.embedding_type
    input_data = [request.input] if isinstance(request.input, str) else request.input

    if embedding_type is None:
        embedding_type = config.DEFAULT_EMBEDDING_TYPE
    if embedding_type == "dense":
        embeddings = model.encode(input_data, batch_size=config.BATCH_SIZE, normalize_embeddings=True)['dense_vecs']
    elif embedding_type == "sparse":
        embeddings = model.encode(input_data, return_dense=True, return_sparse=True, return_colbert_vecs=False)['lexical_weights']
    elif embedding_type == "colbert":
        embeddings = model.encode(input_data, return_dense=True, return_sparse=True, return_colbert_vecs=True)['colbert_vecs']
    elif embedding_type == "all":
        embeddings = model.encode(input_data, return_dense=True, return_sparse=True, return_colbert_vecs=True)
    response = {
        "data": [
            {"embedding": embedding, "index": index, "object": "embedding"}
            for index, embedding in enumerate(embeddings)
        ],
        "model": config.BGE_MODEL_NAME,
    }

    return response

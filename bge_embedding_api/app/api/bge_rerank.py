from fastapi import APIRouter
from bge_embedding_api.app.models.request import RerankRequest
from bge_embedding_api.library.config import config
from FlagEmbedding import FlagReranker


router = APIRouter()

reranker = None


def load_rerank_model(model_name, device):
    global reranker
    reranker = FlagReranker(model_name, device=device, use_fp16=True)


@router.get("/v1/rerank")
async def rerank(request: RerankRequest):
    if reranker is None:
        load_rerank_model(config.RERANK_MODEL_NAME, config.DEVICE)
    query = request.query
    documents = request.documents
    pairs = [[query, doc] for doc in documents]
    scores = reranker.compute_score(pairs)

    response = {
        "data": [
            {"score": score, "index": index}
            for index, score in enumerate(scores)
        ],
        "model": config.RERANK_MODEL_NAME,
    }

    return response

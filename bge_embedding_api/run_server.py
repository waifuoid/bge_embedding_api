from bge_embedding_api.library.restapi import app as fastapi_app
from bge_embedding_api.library.restapi import load_router_callback
from bge_embedding_api.library.autoload import LoadFile
from bge_embedding_api.library.config import config
from bge_embedding_api.app.api.bge import load_bge_model
from bge_embedding_api.app.api.bge_rerank import load_rerank_model


import os
import uvicorn


def run_server():
    load_file = LoadFile(callback=load_router_callback)
    load_file.root_path = os.path.dirname(os.path.abspath(__file__))
    load_file.loop_up("app/api")
    if config.LOAD_BGE_MODEL:
        load_bge_model(config.BGE_MODEL_NAME, config.DEVICE)
    if config.LOAD_RERANK_MODEL:
        load_rerank_model(config.RERANK_MODEL_NAME, config.DEVICE)
    uvicorn.run(fastapi_app, host=config.SERVER_HOST, port=config.SERVER_PORT)

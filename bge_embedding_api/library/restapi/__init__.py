from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import importlib

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_router_callback(packet, suffix_to_remove="app.", prefix="bge_embedding_api"):
    module_path = ".".join(([prefix, packet]))
    module = importlib.import_module(module_path)
    if hasattr(module, 'router'):
        router = module.router
        prefix = packet.replace(suffix_to_remove, "/").replace(".", "/")
        tags = prefix.split("/")
        prefix = "/".join(tags[:-1])
        app.include_router(router, prefix=prefix, tags=tags)
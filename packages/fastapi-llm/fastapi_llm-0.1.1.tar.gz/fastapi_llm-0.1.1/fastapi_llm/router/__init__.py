from .functions import *
from .files import *
from .loaders import *
from fastapi import APIRouter

class Router(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = "/api"
        self.tags =  ["API"]
        self.include_router(FunctionsRouter())
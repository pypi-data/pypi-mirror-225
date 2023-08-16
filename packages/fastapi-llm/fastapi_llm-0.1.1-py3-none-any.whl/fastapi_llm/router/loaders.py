import functools
from celery import Celery
from fastapi.responses import StreamingResponse
from ..config import env
from fastapi import APIRouter, File, UploadFile
from fastapi_llm.service import function_call
from ..service import *
from ..schema import *
from ..tools.loaders import website_loader, pdf_loader

class LoadersRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.llm = LLMStack()
        self.prefix = "/loaders"
        self.tags =  ["Loaders"]
    
        @self.get("/loaders")
        async def loaders_consumer():
            """
            Suscribes to the loaders queue and returns the results as a stream.
            Updates the progress of the loaders being executed.
            """
            
            
            
            
    @property
    def worker(self):
        return Celery(self.__class__.__name__, backend=env.REDIS_URL, broker=env.REDIS_URL)

    def task(self,func):
        """Decorator to defer the execution of a function to a Celery Worker"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.worker.send_task(func.__name__, args=args, kwargs=kwargs)
            wrapper.__name__ = func.__name__
        return wrapper
    
    
from typing import List, Dict, Optional
from types import FunctionType
import httpx
import json 

class NstreamLLM(object):
    def __init__(self) -> None:
        pass
    @staticmethod
    def feret_v1():
        return "FERET_V1"
    @staticmethod
    def llama2_7b():
        return "LLAMA2_7B"
    @staticmethod
    def mistral_7b():
        return "MISTRAL_7B"


class NsNeuron(object):
    def __init__(self, llm:str) -> None:
        self.llm = llm
        pass
from pydantic import BaseModel
from typing import Optional

class Produto(BaseModel):
    nome:str
    preco:float
    descricao:Optional[str] = None
    quantidade: int


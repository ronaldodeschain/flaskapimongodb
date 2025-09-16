from pydantic import BaseModel
from typing import Optional

class Categoria(BaseModel):
    nome:str
    descricao:Optional[str] = None
    
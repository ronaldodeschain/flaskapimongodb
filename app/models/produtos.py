from pydantic import BaseModel,Field,ConfigDict
from typing import Optional
from bson import ObjectId

class Produto(BaseModel):
    id: Optional[ObjectId] = Field(alias='_id',default=None)
    nome:str
    preco:float
    descricao:Optional[str] = None
    quantidade: int
    criado_por: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

class UpdateProduto(BaseModel):
    nome:Optional[str] = None
    preco:Optional[float] = None
    descricao:Optional[str] = None
    quantidade: Optional[int] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )
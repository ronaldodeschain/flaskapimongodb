from pydantic import BaseModel, ConfigDict
from datetime import date

class Venda(BaseModel):
    data_venda:date
    id_produto:str
    quantidade:int
    valor_total:float

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
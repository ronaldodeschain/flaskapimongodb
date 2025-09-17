from pydantic import BaseModel,Field,ConfigDict
from typing import Any, Callable, Literal, Optional
from bson import ObjectId

class Produto(BaseModel):
    id: Optional[ObjectId] = Field(alias='_id',default=None)
    nome:str
    preco:float
    descricao:Optional[str] = None
    quantidade: int

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

class ProdutoDBMoldel(Produto):
    def model_dump(self, *, mode: str | Literal['json'] | Literal['python'] = 'python', include: set[int] | set[str] | Mapping[int, set[int] | set[str] | ... | Mapping[str, IncEx | bool] | bool] | Mapping[str, set[int] | set[str] | Mapping[int, IncEx | bool] | ... | bool] | None = None, exclude: set[int] | set[str] | Mapping[int, set[int] | set[str] | ... | Mapping[str, IncEx | bool] | bool] | Mapping[str, set[int] | set[str] | Mapping[int, IncEx | bool] | ... | bool] | None = None, context: Any | None = None, by_alias: bool | None = None, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False, round_trip: bool = False, warnings: bool | Literal['none'] | Literal['warn'] | Literal['error'] = True, fallback: Callable[[Any], Any] | None = None, serialize_as_any: bool = False) -> dict[str, Any]:
        data =  super().model_dump(mode=mode, include=include, exclude=exclude, context=context, by_alias=by_alias, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none, round_trip=round_trip, warnings=warnings, fallback=fallback, serialize_as_any=serialize_as_any)
        if self.id:
           data['_id'] = str(data['_id'])
        return data


from typing import List, Optional, Union

from pydantic import BaseModel, model_validator


class PackingBin(BaseModel):
    volume: float
    quantity: int
    binType: str
    length: float
    width: float
    height: float


class DispatchPlan(BaseModel):
    shapeType: str
    quantity: int
    length: float
    width: float
    height: float
    weight: float
    volume: float


class LoadingData(BaseModel):
    vehicle: List[PackingBin]
    dispatchPlan: List[DispatchPlan]


class ErrorResponseModel(BaseModel):
    success: bool
    message: str

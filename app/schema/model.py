from typing import List, Optional, Union

from pydantic import BaseModel, root_validator


class Vehicle(BaseModel):
    transporterName: str
    transporterId: str
    volume: float
    quantity: int
    vehicleType: str
    length: float
    width: float
    height: float
    transName: str


class DispatchPlan(BaseModel):
    shapeType: str
    quantity: Optional[Union[str, int]]
    length: Optional[Union[str, float]] = None
    width: Optional[Union[str, float]] = None
    height: Optional[Union[str, float]]
    radius: Optional[Union[str, float]] = None
    weight: Optional[Union[str, float]]
    volume: Optional[Union[str, float]]

    @root_validator(skip_on_failure=True)
    def check_shape_data(cls, values):
        for key, val in values.items():
            if values["shapeType"].lower() == "box":
                if key in ["quantity", "length", "width", "height", "weight", "volume"]:
                    try:
                        if not isinstance(val, float):
                            values[key] = float(val)
                        if key == "quantity":
                            values[key] = int(val)
                    except ValueError:
                        raise ValueError(f"{key} should be str/int/float")
            elif values["shapeType"].lower() == "cylinder":
                if key in ["quantity", "height", "radius", "weight", "volume"]:
                    try:
                        values["length"] = float(values["radius"]) * 2
                        values["width"] = float(values["radius"]) * 2
                        if not isinstance(val, float):
                            values[key] = float(val)
                    except ValueError as err:
                        raise ValueError(f"{key} should be str/int/float")

        return values


class LoadingData(BaseModel):
    # data: Optional[dict]
    vehicle: List[Vehicle]
    dispatchPlan: List[DispatchPlan]

    @root_validator(pre=True)
    def unwrap_data(cls, values):
        if "data" in values and isinstance(values["data"], dict):
            return values["data"]
        return values


class ErrorResponseModel(BaseModel):
    success: bool
    message: str

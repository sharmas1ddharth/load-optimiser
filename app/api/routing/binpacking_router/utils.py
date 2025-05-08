import polars as pl
from polars import DataFrame

from schema.model import LoadingData

def create_dataframe(input_data: LoadingData) -> tuple[DataFrame, DataFrame]:
    vehicle = pl.DataFrame(input_data.vehicle)
    dispatch = pl.DataFrame(input_data.dispatchPlan)
    return vehicle, dispatch

def is_volume_correct(vehicle, dispatch) -> bool:
    vehicle_volume = vehicle['volume'].sum()
    dispatch_volume = dispatch['volume'].sum()
    if vehicle_volume < dispatch_volume:
        return False
    return True



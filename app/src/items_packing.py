from dataclasses import dataclass
from src.load_optimiser_core.main import Packer, Item, Bin
from polars import DataFrame
import polars as pl
import numpy as np


@dataclass(slots=True)
class ItemsPacking:
    bin_combinations: list
    vehicle_dataframe: DataFrame
    dispatch_dataframe: DataFrame
    key_for_combinations: str = "binType"

    def add_bin_to_packer(self):
        packer = Packer()
        for binType in self.bin_combinations:
            bin_type = self.vehicle_dataframe.filter(pl.col(self.key_for_combinations) == binType)
            width = bin_type.select("width").item()
            length = bin_type.select("length").item()
            height = bin_type.select("height").item()
            volume = bin_type.select("volume").item()
            packer.addBin(Bin(binType, (length, width, height), max_weight=volume, put_type=0, corner=0)) #TODO: change volume to max_weight
            break
        first_bin = self.bin_combinations.pop(0)
        self.bin_combinations.append(first_bin)
        return packer

    def pack_unfit_items(self, unfit_item_bin):
        packer = self.add_bin_to_packer()
        for item in unfit_item_bin.unfitted_items:
            packer.addItem(
                Item(
                    str(item.partno),
                    str(item.partno),
                    str(item.typeof),
                    (float(item.length), float(item.width), float(item.height)),
                    float(item.weight),
                    int(item.level),
                    int(item.loadbear),
                    True,
                    str(item.color),
                )
            )
        packer.pack(
            bigger_first=True,
            distribute_items=True,
            fix_point=True,
            number_of_decimals=0,
        )

        return packer

    def pack_items_to_bin(self, unfit_item_bin=None, unfit=False):
        if unfit:
            packer = self.pack_unfit_items(unfit_item_bin)
            return packer

        packer = self.add_bin_to_packer()
        df_with_idx = self.dispatch_dataframe.with_row_index("idx")
        repeat_indices = np.repeat(
            np.arange(len(df_with_idx)),
            df_with_idx["quantity"].to_numpy()
        )
        expanded_df = df_with_idx[repeat_indices]
        for row in expanded_df.select(["idx", "shapeType", "length", "width", "height", "weight"]).rows():
            idx, shape_type, length, width, height, weight = row
            packer.addItem(
                Item(
                    shape_type + str(idx),
                    shape_type + str(idx),
                    shape_type,
                    (length, width, height),
                    weight,
                    0,
                    100,
                    True,
                    "red"
                )
            )
        packer.pack(bigger_first=True, distribute_items=False, fix_point=True, check_stable=True, support_surface_ratio=0.75, number_of_decimals=0)

        return packer

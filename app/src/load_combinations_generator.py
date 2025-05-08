from itertools import combinations
import polars as pl

class LoadCombinationMaker:
    def __init__(self, bin_df, dispatch_df):
        self.bin_df = bin_df
        self.dispatch_df = dispatch_df
        key_for_combinations = "binType"
        self.key_for_combinations: str = key_for_combinations

    def generate_combinations(self) -> set:
        unique_bins: list = list(self.bin_df[self.key_for_combinations].unique())
        all_combinations = [list(combinations(unique_bins, r)) for r in range(1, len(unique_bins) + 1)]
        list_combinations = set([item for sublist in all_combinations for item in sublist])
        return list_combinations

    def calculate_combination_capacities(self) -> dict:
        list_combinations: set = self.generate_combinations()


        comb_with_capacity = {}

        for comb in list_combinations:
            capacity = self.bin_df.filter(
                pl.col("binType").is_in(comb)
            ).select(
                pl.col("volume").sum()
            ).item()
            comb_with_capacity[comb] = capacity

        comb_with_capacity = dict(
            sorted(comb_with_capacity.items(), key=lambda x: x[1])
        )

        return comb_with_capacity

    def get_valid_combinations(self) -> list:
        comb_with_capacity = self.calculate_combination_capacities()
        total_dispatchplan_volume: float = (
                self.dispatch_df["volume"]
                * self.dispatch_df["quantity"]
        ).sum()

        filtered_combs = [
            comb
            for comb, capacity in comb_with_capacity.items()
            if total_dispatchplan_volume < capacity
        ]

        if not filtered_combs:
            filtered_combs = [list(comb_with_capacity.keys())[-1]]

        return filtered_combs

    def get_sorted_combinations(self) -> list:
        valid_combinations: list = self.get_valid_combinations()
        combs = {}
        for item in valid_combinations:
            volume = 0
            for bins in item:
                volume += self.bin_df.filter(
                    pl.col(self.key_for_combinations) == bins
                ).select("volume").item()
            combs[item] = volume
        sorted_combs: list = sorted(combs.keys(), key=lambda x: combs[x], reverse=True)
        return list(sorted_combs[0])

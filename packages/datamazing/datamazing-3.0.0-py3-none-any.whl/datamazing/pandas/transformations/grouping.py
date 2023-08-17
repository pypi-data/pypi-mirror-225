import typing

import pandas as pd

from datamazing._conform import _concat, _list


class GrouperResampler:
    def __init__(
        self,
        gb: "Grouper",
        on: str,
        resolution: pd.Timedelta,
        edge: str,
    ):
        self.gb = gb
        self.on = on
        self.resolution = resolution
        self.edge = edge

    def agg(self, method: str):
        start_time = self.gb.df[self.on].min()
        end_time = self.gb.df[self.on].max()

        if method == "interpolate":
            aggregate_options = {"limit_area": "inside"}
        else:
            aggregate_options = {}

        df = self.gb.df.set_index(self.on)

        df = (
            df.groupby(self.gb.by, dropna=False)
            .resample(rule=self.resolution, closed=self.edge, label=self.edge)
            .aggregate(method, **aggregate_options)
        )

        # depending on the resampling aggregation
        # method, pandas will include the group-by
        # columns in both the index and the columns
        df = df.drop(columns=self.gb.by, errors="ignore")

        df = df.reset_index()

        # after resampling, pandas might leave
        # timestamps outside of the original interval
        if not df.empty:
            df = df[df[self.on].between(start_time, end_time)]

        return df


class Grouper:
    def __init__(self, df: pd.DataFrame, by: list[str]):
        self.df = df
        self.by = by

    def agg(self, method: str):
        return (
            self.df.set_index(self.by)
            .groupby(self.by, dropna=False)
            .aggregate(method)
            .reset_index()
        )

    def resample(self, on: str, resolution: pd.Timedelta, edge: str = "left"):
        return GrouperResampler(self, on, resolution, edge)

    def pivot(self, on: list[str], values: typing.Optional[list[tuple[str]]] = None):
        """
        Pivot table. Non-existing combinations will be filled
        with NaNs.

        Args:
            on (list[str]): Columns which to pivot
            values (list[tuple[str]], optional): Enforce
                the existence of columns with these names
                after pivoting. Defaults to None, in which
                case the values will be inferred from the
                pivoting column.
        """

        df = self.df.set_index(_concat(self.by, on))

        if values:
            by_vals = df.index.to_frame(index=False)[_list(self.by)].drop_duplicates()
            on_vals = pd.DataFrame(values, columns=_list(on))
            cross_vals = by_vals.merge(on_vals, how="cross")
            df = df.reindex(pd.MultiIndex.from_frame(cross_vals))

        df = df.unstack(on)

        # concatenate multiindex columns to single index columns
        concat_cols = []
        suffix = len(df.columns.levels[0]) > 1
        for col in df.columns:
            concat_col = "_".join([str(item) for item in col[1:]])
            if suffix:
                # if more than one remaning columns, suffix with that
                concat_col = concat_col + "_" + str(col[0])
            concat_col = concat_col.strip("_")
            concat_cols.append(concat_col)
        df.columns = concat_cols

        return df.reset_index()

    def latest(self, on: str):
        return (
            self.df.set_index(_concat(self.by, on))
            .sort_index(level=on)
            .groupby(self.by, dropna=False)
            .tail(1)
            .reset_index()
        )


def group(df: pd.DataFrame, by: list[str]):
    return Grouper(df, by)

import inspect
from typing import Callable, Optional

import pandas as pd
from pyspark.sql import Column, DataFrame, SparkSession
from pyspark.sql.types import DataType

from hamilton import base, driver, htypes
from hamilton.ad_hoc_utils import create_temporary_module
from hamilton.experimental.h_spark import with_columns
from hamilton.function_modifiers.dependencies import source, value
from hamilton.function_modifiers.expanders import parameterize


class rename:
    def __init__(self, **columns: str):
        """Initializes a pass-through decorator.
        This just passes through the columns/renames them.
        Its passed a dictrionay of old names to new names

        :param columns: Dictionary of column names to rename
        """
        self.columns = columns

    def __call__(self, fn: Callable) -> Callable:
        if not len(inspect.signature(fn).parameters) == 1:
            raise ValueError("functions decorated with @copies must have a single parameter")
        param, = inspect.signature(fn).parameters.values()
        if not htypes.custom_subclass_check(param.annotation, DataFrame):
            raise ValueError(
                "Cannot decorate a function that does not take a DataFrame with @copies")
        parameterize_args = {
            key: dict(
                column_name=value(col_orig),
                df=source(col_orig)) for col_orig, key in self.columns.items()
        }

        @parameterize(**parameterize_args)
        def feature_copy(df: DataFrame, column_name: str,
                         cast: Optional[DataType] = None) -> Column:
            output = df[column_name].cast(cast)
            if cast is not None:
                output = output.cast(cast)
            return output

        return feature_copy


def spark_session() -> SparkSession:
    return (SparkSession.builder.master("local")
            .appName("spark session")
            .config("spark.sql.shuffle.partitions", "1")
            .getOrCreate())


def generate_df(spark_session: SparkSession) -> DataFrame:
    df = pd.DataFrame.from_records(
        [
            {"key": 1, "a_raw": 1, "b_raw": 2, "c_raw": 1},
            {"key": 2, "a_raw": 4, "b_raw": 5, "c_raw": 2},
            {"key": 3, "a_raw": 7, "b_raw": 8, "c_raw": 3},
            {"key": 4, "a_raw": 10, "b_raw": 11, "c_raw": 4},
            {"key": 5, "a_raw": 13, "b_raw": 14, "c_raw": 5},
        ]
    )
    return spark_session.createDataFrame(df)


def get_feature(df: DataFrame, column_name: str) -> Column:
    return df[column_name]


@rename(
    a_raw="a",
    b_raw="b",
    c_raw="c"
)
def raw_features(df: DataFrame) -> Column:
    """These are the raw features, renamed to end up as output features."""
    pass


@with_columns(
    raw_features,
)
def generate_features(generate_df: DataFrame) -> pd.DataFrame:
    return generate_df


test_module = create_temporary_module(generate_features, generate_df, spark_session)

config = dict()
driver = driver.Driver(
    config,
    test_module,
    adapter=base.DefaultAdapter()
)

out = driver.execute(final_vars=["generate_features"])["generate_features"]
print(out.toPandas())

from typing import Optional
from pyspark.sql.types import DataType
from hamilton.ad_hoc_utils import create_temporary_module
from hamilton.experimental.h_spark import with_columns
from pyspark.sql import Column, DataFrame, SparkSession, Window
from pyspark.sql.functions import col
from hamilton.function_modifiers import does
from hamilton.function_modifiers.expanders import parameterize
from hamilton.function_modifiers.dependencies import source, value
from hamilton import base, driver

import pandas as pd


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


# def get_feature(df: DataFrame, column_name: str) -> Column:
#     return df[column_name]

def get_column_from_df(
        df: DataFrame,
        column_name: str,
        cast: Optional[DataType] = None,
) -> DataFrame:
    column_name_replaced = column_name.replace("_raw", "")
    if cast is not None:
        return df.withColumn(column_name_replaced, col(column_name).cast(cast))
    return df.withColumn(column_name_replaced, col(column_name))


# @parameterize(
#     a=dict(column_name=value("a_raw"), df=source("a_raw")),
#     b=dict(column_name=value("b_raw"), df=source("b_raw")),
#     c=dict(column_name=value("c_raw"), df=source("c_raw")),
# )
# @does(get_column_from_df)
# def raw_feature(df: DataFrame, column_name: str) -> DataFrame:
#     pass

@parameterize(
    a=dict(column_name=value("a_raw"), df=source("a_raw")),
    b=dict(column_name=value("b_raw"), df=source("b_raw")),
    c_raw=dict(column_name=value("c_raw"), df=source("c_raw")),
)
@does(get_column_from_df)
def raw_feature(df: DataFrame, column_name: str) -> DataFrame:
    pass


@with_columns(
    raw_feature,
    mode="select",
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
driver.visualize_execution(
    final_vars=["generate_features"],
    output_file_path="test.png",
    render_kwargs={},
)
print(out.toPandas())

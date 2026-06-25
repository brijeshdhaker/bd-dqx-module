from databricks.labs.dqx.rule import register_rule
from databricks.labs.dqx.check_funcs import make_condition
from pyspark.sql import Column, DataFrame
from pyspark.sql import functions as F
from collections.abc import Callable
import uuid


@register_rule("dataset")
def max_orders_per_region(max_count: int) -> tuple[Column, Callable]:
    condition_col = f"__region_check_{uuid.uuid4().hex[:8]}"

    def apply(df: DataFrame) -> DataFrame:
        region_counts = df.groupBy("region").agg(
            F.count("*").alias("region_count")
        )
        return df.join(region_counts, on="region", how="left").withColumn(
            condition_col,
            F.col("region_count") <= max_count
        ).drop("region_count")

    return (
        make_condition(
            condition=F.col(condition_col),
            message=f"region has more than {max_count} orders",
            alias="region_order_count_check",
        ),
        apply,
    )

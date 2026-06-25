import pyspark.sql.functions as F
from pyspark.sql import Column
from databricks.labs.dqx.check_funcs import make_condition, get_normalized_column_and_expr
from databricks.labs.dqx.rule import register_rule

# Registering the rule as a "row" level check
@register_rule("row")
def must_exceed_minimum(column: str | Column, min_value: int) -> Column:
    """
    Custom row-level rule verifying that a column's numerical value 
    is strictly greater than a specified minimum value.
    """
    # Normalize the column input to handle both strings and Column objects safely
    col_str_norm, col_expr_str, col_expr = get_normalized_column_and_expr(column)
    
    # Define the core validation condition (True means the row passes)
    condition_expr = col_expr > min_value
    
    # Build and return the condition payload required by DQX
    return make_condition(
        condition=condition_expr,
        message=f"Column '{col_expr_str}' value must be greater than {min_value}.",
        name=f"{col_str_norm}_must_exceed_{min_value}"
    )

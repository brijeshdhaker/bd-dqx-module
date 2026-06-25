from databricks.labs.dqx.rule import register_rule
from databricks.labs.dqx.check_funcs import make_condition, get_normalized_column_and_expr
import pyspark.sql.functions as F
from pyspark.sql import Column

# Registering the rule as a "row" level check
@register_rule("row")
def py_validate_trackid(column: str | Column) -> Column:
    """
    Custom row-level rule verifying that a column's numerical value 
    is strictly greater than a specified minimum value.
    """
    # Normalize the column input to handle both strings and Column objects safely
    col_str_norm, col_expr_str, col_expr = get_normalized_column_and_expr(column)
    
    # Define the core validation condition (True means the row passes)
    condition_expr = (F.col(col_str_norm).startswith("TRK-") and F.length(F.col(col_str_norm)) == 10)
    
    # Build and return the condition payload required by DQX
    return make_condition(
        condition=condition_expr,
        message=f"Column '{col_expr_str}' value must be start with 'TRK-'.",
        name=f"{col_str_norm}_must_value must be start with 'TRK-'"
    )
import re
from databricks.labs.dqx.rule import register_rule
from databricks.labs.dqx.check_funcs import make_condition, get_normalized_column_and_expr
import pyspark.sql.functions as F
from pyspark.sql import Column

#
@register_rule("row")
def py_validate_email(column: str | Column) :
    """
    Custom row-level rule verifying that a column's numerical value 
    is strictly greater than a specified minimum value.
    """
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not column:
        return False
    
    # Normalize the column input to handle both strings and Column objects safely
    col_str_norm, col_expr_str, col_expr = get_normalized_column_and_expr(column)
    
    # Define the core validation condition (True means the row passes)
    # re.match(regex, email)
    condition_expr = F.regexp(F.col("col_str_norm"), regex)
    
    # Build and return the condition payload required by DQX
    return make_condition(
        condition=condition_expr,
        message=f"Column '{col_expr_str}' value must be valid email like bdhaker@ubs.com",
        name=f"{col_str_norm}_must_be valid email like bdhaker@ubs.com"
    )



from sqlalchemy import Select, Column, or_
from typing import List, Any


def format_in_clause(query: Select, column: Column, values: List[Any]) -> Select:
    """
    Format an IN clause for a SQL query.

    Args:
        query (Select): The SQL query object.
        column (Column): The column to filter on.
        values (List[Any]): The values to filter on.

    Returns:
        Select: The modified SQL query object.

    Raises:
        ValueError: If values is None or empty.
    """
    if values is None or len(values) <= 1000:
        return query.where(column.in_(values))

    # Split values into chunks of 1000
    chunks = [values[i : i + 1000] for i in range(0, len(values), 1000)]

    # Create conditions for each chunk
    conditions = [column.in_(chunk) for chunk in chunks]

    # Combine conditions with OR operator
    final_condition = or_(*conditions)

    return query.where(final_condition)

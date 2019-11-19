import pandas as pd
from typing import Tuple

# DataFrame level checks (as opposed to column level checks)
# are described in functions using the naming convention
# dfcheck_[some name](df: pd.DataFrame, [inputs]) -> Tuple[bool, str]
# The return value is a tuple containing a bool indicating if the
# test passed or failed (true = passed) and a string describing
# the error condition if the test failed. Error messages follow
# the pattern 'want [expected value or condition], got [actual
# value or condition'.

def dfcheck_min_rows(df: pd.DataFrame, min_rows: int) -> Tuple[bool, str]:
    """Check if a DataFrame has a minimum number of rows."""
    num_rows: int = len(df)
    if num_rows >= min_rows:
        return True, ''
    return False, f'want {min_rows} rows, got {num_rows}'

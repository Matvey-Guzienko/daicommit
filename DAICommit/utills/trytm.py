
from typing import Tuple, Any, Optional

def try_tm(func: Any, **kwargs) -> Tuple[Optional[Any], Optional[Exception]]:
    try:
        data = func(**kwargs)
        return data, None
    except Exception as throwable:
        return None, throwable

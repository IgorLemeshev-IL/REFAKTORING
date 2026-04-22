import time
from functools import wraps
from typing import Callable, TypeVar, Any

T = TypeVar("T")


def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """
    Декоратор для повторных попыток выполнения функции при ошибке.
    
    Args:
        max_attempts: максимальное количество попыток
        delay: задержка между попытками в секундах
        exceptions: кортеж исключений, при которых нужно повторять
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        time.sleep(delay)
                    else:
                        raise last_exception
            
            if last_exception:
                raise last_exception
                
        return wrapper
    return decorator
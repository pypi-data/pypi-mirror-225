import typing
import functools
from dataclasses import dataclass

T = typing.TypeVar('T')

@dataclass(frozen=True)
class Some(typing.Generic[T]):
    value: T

    def bind(self, f: typing.Callable[[T], 'Maybe[T]']) -> 'Maybe[T]':
        return f(self.value)
    
    def map(self, f: typing.Callable[[T], T]) -> 'Maybe[T]':
        return Some(f(self.value))

    def __repr__(self) -> str:
        return f'Some[{self.value.__class__.__name__}]({self.value})'

Maybe = typing.Union[Some[T], None]

def with_maybe(f: typing.Callable[..., T]) -> typing.Callable[..., Maybe[T]]:
    @functools.wraps(f)
    def wrapper(*args: typing.Any, **kwargs: typing.Any) -> Maybe[T]:
        try:
            return Some(f(*args, **kwargs))
        except Exception:
            return None
    return wrapper
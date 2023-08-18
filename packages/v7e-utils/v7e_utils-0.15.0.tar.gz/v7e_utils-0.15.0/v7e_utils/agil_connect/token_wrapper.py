from __future__ import annotations

from functools import wraps
from v7e_utils.agil_connect.token import Token


def insert_token(api_key:str | None=None, api_key_prefix:str='Api-Key'):
    """
    Set token of Authorization in request agil
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            authorization = args[0].headers.get('Authorization', None)
            token = Token()
            if api_key:
                token.set_token(f'{api_key_prefix} {api_key}')
            elif authorization:
                token.set_token(authorization)
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    return decorator


def with_token(
    function=None, api_key:str | None=None, api_key_prefix:str='Api-Key'
):
    """
    Decorator for views that checks that the token in requests consult agil
    """
    actual_decorator = insert_token(
        api_key=api_key,
        api_key_prefix=api_key_prefix,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

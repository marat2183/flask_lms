from flask import Response, request, render_template, jsonify, make_response, current_app
from functools import wraps
from typing import List, Dict, Union, Optional
import inspect


def required_json_arguments(view_func):
    @wraps(view_func)
    def decorator(*args, **kwargs):
        signature = inspect.signature(view_func)
        data = request.get_json()

        for arg in signature.parameters.values():
            if arg.name in kwargs:
                continue
            if data and data.get(arg.name) is not None:
                kwargs[arg.name] = data.get(arg.name)
            elif arg.default is not arg.empty:
                kwargs[arg.name] = arg.default

        missing = [arg for arg in signature.parameters.keys() if arg not in kwargs.keys()]

        if missing:
            return 'No data provided for required arguments: {}'.format(
                ', '.join(missing)
            ), 400
        return view_func(*args, **kwargs)
    return decorator


def required_query_params(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        signature = inspect.signature(view_func)

        params = request.args

        for arg in signature.parameters.values():
            if arg.name in kwargs:
                continue
            if params and params.get(arg.name) is not None:
                kwargs[arg.name] = params.get(arg.name)
            elif arg.default is not arg.empty:
                kwargs[arg.name] = arg.default

        missing = [arg for arg in signature.parameters.keys() if arg not in kwargs.keys()]

        if missing:
            return 'Missing required query parameters: {}'.format(
                ', '.join(missing)
            ), 400
        return view_func(*args, **kwargs)
    return decorated_view


ResponseData = Union[
    Dict[
        str,
        Union[
            List[Union[str, Dict]],
            Dict[str, str],
            str
        ]
    ],
    List[str]
]


def make_json_response(status: str, message: str, data: ResponseData = None, status_code: int = None, **kwargs) -> Response:
    """Helper function to create JSON API responses"""
    response: Response = jsonify({
        'status': status,
        'message': message,
        'data': data,
        **kwargs
    })
    if status_code is not None:
        response.status_code = status_code
    return response

def success(message: str, data: ResponseData):
    return make_json_response(
        status='success',
        message=message,
        data=data,
        status_code=200
    )


def error(message: str, data: Optional[ResponseData] = None, status_code: int = 500):
    return make_json_response(
        status='error',
        message=message,
        data=data,
        status_code=status_code
    )


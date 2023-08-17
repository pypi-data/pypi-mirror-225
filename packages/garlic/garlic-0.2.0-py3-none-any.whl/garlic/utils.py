import inspect
from typing import Callable, Any, ForwardRef


def get_typed_annotation(annotation: Any) -> Any:
    if isinstance(annotation, str):
        annotation = ForwardRef(annotation)
    return annotation


def get_typed_signature(call: Callable[..., Any]) -> inspect.Signature:
    signature = inspect.signature(call)
    typed_params = [
        inspect.Parameter(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=get_typed_annotation(param.annotation),
        )
        for param in signature.parameters.values()
    ]
    typed_signature = inspect.Signature(typed_params)
    return typed_signature

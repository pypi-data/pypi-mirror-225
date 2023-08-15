__all__ = ["InferenceModel", "Prediction"]
import typing

if typing.TYPE_CHECKING:
    from .inference_model import InferenceModel, Prediction
else:
    try:
        import fastapi
        import uvicorn

        from .inference_model import InferenceModel, Prediction
    except ImportError as e:
        if 'uvicorn' in str(e) or 'fastapi' in str(e):

            class InferenceModel:
                def __init__(self, *args, **kwargs):
                    raise ImportError(
                        "InferenceModel requires uvicorn and fastapi to be installed. Please install these dependencies and try again."
                    )

        else:
            # Handle other import errors if needed
            raise

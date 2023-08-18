from typing import Any


def _convert_input_data(data: Any) -> list:  # type: ignore
    # sourcery skip: merge-duplicate-blocks, remove-redundant-if, remove-unnecessary-else, swap-if-else-branches
    """
    Convert the input data to a list.

    Args:
        data (Union[list, ndarray, Tensor]): The data to convert.

    Returns:
        list: The converted data as a python list.
    """
    try:
        from torch import Tensor

        torch_installed = True
    except ImportError:
        torch_installed = False
    try:
        from numpy import ndarray

        numpy_installed = True
    except ImportError:
        numpy_installed = False

    if torch_installed:
        from torch import Tensor
        from numpy import ndarray

        if isinstance(data, Tensor):
            return data.tolist()
        elif isinstance(data, ndarray):
            return data.tolist()
    if numpy_installed:
        from numpy import ndarray

        return data.tolist() if isinstance(data, ndarray) else data
    else:
        return data

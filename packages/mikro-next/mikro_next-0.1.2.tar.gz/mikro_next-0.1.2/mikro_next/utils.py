from typing import Dict, Any
import math
from .errors import NotQueriedError


def rechunk(
    sizes: Dict[str, int], itemsize: int = 8, chunksize_in_bytes: int = 20_000_000
) -> Dict[str, int]:
    """Calculates Chunks for a given size

    Args:
        sizes (Dict): The sizes of the image

    Returns:
        The chunks(dict): The chunks
    """
    assert "c" in sizes, "c must be in sizes"
    assert "z" in sizes, "z must be in sizes"
    assert "y" in sizes, "y must be in sizes"
    assert "x" in sizes, "x must be in sizes"
    assert "t" in sizes, "t must be in sizes"

    all_size = sizes["c"] * sizes["z"] * sizes["y"] * sizes["x"] * sizes["t"]

    # We will not rechunk if the size is smaller than 1MB
    if all_size < 1 * 2048 * 2048:
        return sizes

    x = (
        sizes["x"] if not sizes["x"] > 2048 else 2048
    )  # Biggest X but not bigger than 1024
    y = (
        sizes["y"] if not sizes["y"] > 2048 else 2048
    )  # Biggest Y but not bigger than 1024

    best_z = math.ceil(chunksize_in_bytes / (x * y * itemsize))
    z = best_z if best_z < sizes["z"] else sizes["z"]

    best_t = math.ceil(chunksize_in_bytes / (x * y * z * itemsize))
    t = best_t if best_t < sizes["t"] else sizes["t"]

    chunk = {
        "c": 1,
        "z": z,
        "y": y,
        "x": x,
        "t": t,
    }

    return chunk


def get_nested_error(obj: Any, nested: list[str], above: []) -> Any:
    if hasattr(obj, nested[0]):
        obj = getattr(obj, nested[0])
        if len(nested) > 1:
            return get_nested_error(obj, nested[1:], above + [nested[0]])
        else:
            return obj
    else:
        raise NotQueriedError(f"{nested} not queried. {above} was queried")


def get_attributes_or_error(self, *args) -> Any:
    returns = []
    errors = []
    for i in args:
        if "." in i:
            try:
                returns.append(get_nested_error(self, i.split("."), []))
                continue
            except NotQueriedError:
                errors.append(i)
        else:
            if hasattr(self, i):
                returns.append(getattr(self, i))
            else:
                errors.append(i)

    if len(errors) > 0:
        raise NotQueriedError(
            f"Required fields {errors} not queried on {self.__class__.__name__}"
        )

    if len(args) == 1:
        return returns[0]
    else:
        return tuple(returns)

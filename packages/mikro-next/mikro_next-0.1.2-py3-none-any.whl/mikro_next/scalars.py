""" 
Custom scalars for mikro_next


"""


import os
from typing import Any, IO, Optional
import xarray as xr
import pandas as pd
import numpy as np
import io
from typing import TYPE_CHECKING
from .utils import rechunk
import uuid


if TYPE_CHECKING:
    from mikro_next.datalayer import DataLayer


class AssignationID(str):
    """A custom scalar to represent an affine matrix."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """Validate the input array and convert it to a xr.DataArray."""
        return cls(v)


class XArrayConversionException(Exception):
    """An exception that is raised when a conversion to xarray fails."""

    pass


MetricValue = Any
FeatureValue = Any


class Upload:
    """A custom scalar for ensuring an interface to files api supported by mikro_next It converts the graphql value
    (a string pointed to a zarr store) into a downloadable file. To access the file you need to call the download
    method. This is done to avoid unnecessary requests to the datalayer api.
    """

    __file__ = True

    def __init__(self, value) -> None:
        self.value = value

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.remove(self.local_file)

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def validate(cls, v):
        # you could also return a string here which would mean model.post_code
        # would be a string, pydantic won't care but you could end up with some
        # confusion since the value's type won't match the type annotation
        # exactly
        return cls(v)

    def __repr__(self):
        return f"Upload({self.value})"


class Micrometers(float):
    """A custom scalar to represent a micrometer."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """Validate the input array and convert it to a xr.DataArray."""
        return cls(v)


class Milliseconds(float):
    """A custom scalar to represent a micrometer."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """Validate the input array and convert it to a xr.DataArray."""
        return cls(v)


class TwoDVector(list):

    """A custom scalar to represent a vector."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """Validate the input array and convert it to a xr.DataArray."""
        if isinstance(v, np.ndarray):
            assert v.ndim == 1
            v = v.tolist()

        assert isinstance(v, list)
        assert len(v) == 3
        return cls(v)

    def as_vector(self):
        return np.array(self).reshape(-1)


class ThreeDVector(list):

    """A custom scalar to represent a vector."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """Validate the input array and convert it to a xr.DataArray."""
        if isinstance(v, np.ndarray):
            assert v.ndim == 1
            v = v.tolist()

        assert isinstance(v, list)
        assert len(v) == 3
        return cls(v)

    def as_vector(self):
        return np.array(self).reshape(-1)


class FourDVector(list):

    """A custom scalar to represent a vector."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """Validate the input array and convert it to a xr.DataArray."""
        if isinstance(v, np.ndarray):
            assert v.ndim == 1
            v = v.tolist()

        assert isinstance(v, list)
        assert len(v) == 4
        return cls(v)

    def as_vector(self):
        return np.array(self).reshape(-1)


class FiveDVector(list):

    """A custom scalar to represent a vector."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """Validate the input array and convert it to a xr.DataArray."""
        if isinstance(v, np.ndarray):
            assert v.ndim == 1
            v = v.tolist()

        assert isinstance(v, list)
        assert len(v) == 5
        return cls(v)

    def as_vector(self):
        return np.array(self).reshape(-1)


class Matrix(list):
    """A custom scalar to represent an affine matrix."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """Validate the input array and convert it to a xr.DataArray."""
        if isinstance(v, np.ndarray):
            assert v.ndim == 2
            assert v.shape[0] == v.shape[1]
            assert v.shape == (3, 3)
            v = v.tolist()

        assert isinstance(v, list)
        return cls(v)

    def as_matrix(self):
        return np.array(self).reshape(3, 3)


class FourByFourMatrix(list):
    """A custom scalar to represent a four by four matrix (e.g 3D affine matrix.)"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """Validate the input array and convert it to a xr.DataArray."""
        if isinstance(v, np.ndarray):
            assert v.ndim == 2
            assert v.shape[0] == v.shape[1]
            assert v.shape == (4, 4)
            v = v.tolist()

        assert isinstance(v, list)
        return cls(v)

    def as_matrix(self):
        return np.array(self).reshape(3, 3)


class ArrayLike:
    """A custom scalar for wrapping of every supported array like structure on
    the mikro platform. This scalar enables validation of various array formats
    into a mikro api compliant xr.DataArray.."""

    def __init__(self, value: xr.DataArray) -> None:
        self.value = value
        self.key = str(uuid.uuid4())

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: xr.DataArray):
        """Validate the input array and convert it to a xr.DataArray."""

        if isinstance(v, np.ndarray):
            dims = ["c", "t", "z", "y", "x"]
            v = xr.DataArray(v, dims=dims[5 - v.ndim :])

        if not isinstance(v, xr.DataArray):
            raise ValueError("This needs to be a instance of xarray.DataArray")

        if "x" not in v.dims:
            raise ValueError("Representations must always have a 'x' Dimension")

        if "y" not in v.dims:
            raise ValueError("Representations must always have a 'y' Dimension")

        if "t" not in v.dims:
            v = v.expand_dims("t")
        if "c" not in v.dims:
            v = v.expand_dims("c")
        if "z" not in v.dims:
            v = v.expand_dims("z")

        chunks = rechunk(
            v.sizes, itemsize=v.data.itemsize, chunksize_in_bytes=20_000_000
        )

        v = v.chunk(
            {key: chunksize for key, chunksize in chunks.items() if key in v.dims}
        )

        v = v.transpose(*"ctzyx")

        return cls(v)

    def __repr__(self):
        return f"InputArray({self.value})"


class BigFile:
    """A custom scalar for wrapping of every supported array like structure on
    the mikro platform. This scalar enables validation of various array formats
    into a mikro api compliant xr.DataArray.."""

    def __init__(self, value: IO) -> None:
        self.value = value
        self.key = str(value.name)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """Validate the input array and convert it to a xr.DataArray."""

        if isinstance(v, str):
            v = open(v, "rb")

        if not isinstance(v, io.IOBase):
            raise ValueError("This needs to be a instance of a file")

        return cls(v)

    def __repr__(self):
        return f"BigFile({self.value})"


class ParquetLike:
    """A custom scalar for ensuring a common format to support write to the
    parquet api supported by mikro_next It converts the passed value into
    a compliant format.."""

    def __init__(self, value: pd.DataFrame) -> None:
        self.value = value
        self.key = str(uuid.uuid4())

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, pd.DataFrame):
            raise ValueError("This needs to be a instance of pandas DataFrame")

        return cls(v)

    def __repr__(self):
        return f"ParquetInput({self.value})"


class FileLike:
    """A custom scalar for ensuring a common format to support write to the
    parquet api supported by mikro_next It converts the passed value into
    a compliant format.."""

    def __init__(self, value: IO, name="") -> None:
        self.value = value
        self.key = str(name)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """Validate the input array and convert it to a xr.DataArray."""

        if isinstance(v, str):
            file = open(v, "rb")
            name = v
        else:
            file = v
            name = v.name

        if not isinstance(file, io.IOBase):
            raise ValueError("This needs to be a instance of a file")

        return cls(file, name=name)

    def __repr__(self):
        return f"FileLikeInput({self.value})"



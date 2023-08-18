import asyncio

from mikro_next.scalars import ArrayLike, ParquetLike, FileLike
from rath.links.parsing import ParsingLink
from rath.operation import Operation, opify
from mikro_next.io.types import Uploader
from typing import Any, TYPE_CHECKING
from mikro_next.io.upload import aupload_bigfile, aupload_xarray, aupload_parquet
from pydantic import Field
from concurrent.futures import ThreadPoolExecutor
import uuid
from functools import partial
from mikro_next.datalayer import DataLayer


async def apply_recursive(func, obj, typeguard):
    if isinstance(obj, dict):  # if dict, apply to each key
        return {k: await apply_recursive(func, v, typeguard) for k, v in obj.items()}
    elif isinstance(obj, list):  # if list, apply to each element
        return await asyncio.gather(
            *[apply_recursive(func, elem, typeguard) for elem in obj]
        )
    elif isinstance(obj, tuple):  # if tuple, apply to each element
        return tuple(await apply_recursive(func, elem, typeguard) for elem in obj)
    if isinstance(obj, typeguard):
        return await func(obj)
    else:
        return obj


async def afake_upload(xarray: ArrayLike, *args, **kwargs) -> str:
    return str(uuid.uuid4())


class UploadLink(ParsingLink):
    """Data Layer Upload Link

    This link is used to upload  supported types to a DataLayer.
    It parses queries, mutatoin and subscription arguments and
    uploads the items to the DataLayer, and substitures the
    DataFrame with the S3 path.

    Args:
        ParsingLink (_type_): _description_


    """

    parquet_uploader: Uploader = aupload_parquet
    xarray_uploader: Uploader = aupload_xarray
    bigfile_uploader: Uploader = aupload_bigfile
    datalayer: DataLayer

    executor: ThreadPoolExecutor = Field(
        default_factory=lambda: ThreadPoolExecutor(max_workers=4), exclude=True
    )
    _executor_session: Any = None

    async def __aenter__(self):
        self._executor_session = self.executor.__enter__()

    async def aget_image_credentials(self, key, datalayer) -> Any:
        from mikro_next.api.schema import RequestUploadMutation

        operation = opify(
            RequestUploadMutation.Meta.document,
            variables={"key": key, "datalayer": datalayer},
        )

        async for result in self.next.aexecute(operation):
            return RequestUploadMutation(**result.data).request_upload

    async def aget_table_credentials(self, key, datalayer) -> Any:
        from mikro_next.api.schema import RequestTableUploadMutation

        operation = opify(
            RequestTableUploadMutation.Meta.document,
            variables={"key": key, "datalayer": datalayer},
        )

        async for result in self.next.aexecute(operation):
            return RequestTableUploadMutation(**result.data).request_table_upload

    async def aget_bigfile_credentials(self, key, datalayer) -> Any:
        from mikro_next.api.schema import RequestFileUploadMutation

        operation = opify(
            RequestFileUploadMutation.Meta.document,
            variables={"key": key, "datalayer": datalayer},
        )

        async for result in self.next.aexecute(operation):
            return RequestFileUploadMutation(**result.data).request_file_upload

    async def aupload_parquet(
        self, datalayer: "DataLayer", parquet_input: ParquetLike
    ) -> str:
        assert datalayer is not None, "Datalayer must be set"
        endpoint_url = await datalayer.get_endpoint_url()

        credentials = await self.aget_table_credentials(parquet_input.key, endpoint_url)
        return await self.parquet_uploader(
            parquet_input,
            credentials,
            datalayer,
            self._executor_session,
        )

    async def aupload_xarray(self, datalayer: "DataLayer", xarray: ArrayLike) -> str:
        assert datalayer is not None, "Datalayer must be set"
        endpoint_url = await datalayer.get_endpoint_url()

        credentials = await self.aget_image_credentials(xarray.key, endpoint_url)
        return await self.xarray_uploader(
            xarray,
            credentials,
            datalayer,
            self._executor_session,
        )

    async def aupload_bigfile(self, datalayer: "DataLayer", file: FileLike) -> str:
        assert datalayer is not None, "Datalayer must be set"
        endpoint_url = await datalayer.get_endpoint_url()

        credentials = await self.aget_bigfile_credentials(file.key, endpoint_url)
        return await self.bigfile_uploader(
            file,
            credentials,
            datalayer,
            self._executor_session,
        )

    async def aparse(self, operation: Operation) -> Operation:
        """Parse the operation (Async)

        Extracts the DataFrame from the operation and uploads it to the DataLayer.

        Args:
            operation (Operation): The operation to parse

        Returns:
            Operation: _description_
        """

        datalayer = operation.context.kwargs.get("datalayer", self.datalayer)

        operation.variables = await apply_recursive(
            partial(self.aupload_xarray, datalayer),
            operation.variables,
            ArrayLike,
        )
        operation.variables = await apply_recursive(
            partial(self.aupload_parquet, datalayer), operation.variables, ParquetLike
        )
        operation.variables = await apply_recursive(
            partial(self.aupload_bigfile, datalayer), operation.variables, FileLike
        )

        return operation

    async def adisconnect(self):
        self.executor.__exit__(None, None, None)

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True
        extra = "forbid"

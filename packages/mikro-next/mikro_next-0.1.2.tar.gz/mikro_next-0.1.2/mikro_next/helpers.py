from .api.schema import (
    PartialTransformationViewInput,
    PartialChannelViewInput,
    PartialTimepointViewInput,
    PartialOpticsViewInput,
    PartialLabelViewInput,
    TransformationKind,
    ViewInput,
    ChannelFragment,
    FluorophoreFragment,
    ObjectiveFragment,
    InstrumentFragment,
    CameraFragment,
    EraFragment,
    AntibodyFragment,
)
from .scalars import ThreeDVector, Milliseconds
from rath.scalars import ID
from typing import List
import numpy as np


def accesor_from_slices(slices: List[str] = None):
    """Creates an accesor from a list of slices

    Args:
        slices (List[str]): The slices

    Returns:
        str: The accesor
    """
    return {}


def view_from_pixel_size_and_position(
    scale: ThreeDVector,
    position: ThreeDVector,
    stage: ID = None,
    **kwargs,
) -> PartialTransformationViewInput:
    """Creates a view from the pixel size and position

    Args:
        x_scale (float): The x scale
        y_scale (float): The y scale
        z_scale (float): The z scale
        x_position (float): The x position
        y_position (float): The y position
        z_position (float): The z position

    Returns:
        View: The view
    """
    x_scale, y_scale, z_scale = scale
    x_position, y_position, z_position = position

    affine = np.array(
        [
            [x_scale, 0, 0, x_position],
            [0, y_scale, 0, y_position],
            [0, 0, z_scale, z_position],
            [0, 0, 0, 1],
        ]
    )

    return PartialTransformationViewInput(
        matrix=affine, kind=TransformationKind.AFFINE, stage=stage, **kwargs
    )


def view_from_channel(channel: ChannelFragment, c: int = None, **kwargs) -> ViewInput:
    """Creates a view from the channel name

    Args:
        channel_name (str): The channel name

    Returns:
        View: The view
    """
    if c is not None:
        return PartialChannelViewInput(channel=channel, cMax=c, cMin=c, **kwargs)

    return PartialChannelViewInput(channel=channel, **kwargs)


def opticsview_from_path(
    objective: ObjectiveFragment = None,
    camera: CameraFragment = None,
    instrument: InstrumentFragment = None,
    **kwargs,
) -> ViewInput:
    """Creates a view from the channel name

    Args:
        channel_name (str): The channel name

    Returns:
        View: The view
    """
    return PartialOpticsViewInput(
        objective=objective, camera=camera, instrument=instrument, **kwargs
    )


def timepoint_view_from_era(
    era: EraFragment,
    index_since_start: int = None,
    ms_since_start: Milliseconds = None,
    t: int = None,
) -> ViewInput:
    """Creates a view from the channel name

    Args:
        channel_name (str): The channel name

    Returns:
        View: The view
    """
    if t is not None:
        return PartialTimepointViewInput(
            era=era.id,
            index_since_start=index_since_start,
            ms_since_start=ms_since_start,
            tMax=t,
            tMin=t,
        )

    return PartialTimepointViewInput(
        era=era.id,
        index_since_start=index_since_start,
        ms_since_start=ms_since_start,
    )


def labelview_from_agents(
    fluorophore: FluorophoreFragment = None,
    primary_antibody: AntibodyFragment = None,
    secondary_antibody: AntibodyFragment = None,
    c: int = None,
    **kwargs,
) -> ViewInput:
    """Creates a view from the channel name

    Args:
        channel_name (str): The channel name

    Returns:
        View: The view
    """
    if c is not None:
        return PartialLabelViewInput(
            fluorophore=fluorophore.id,
            primary_antibody=primary_antibody.id,
            secondary_antibody=secondary_antibody.id,
            cMax=c,
            cMin=c,
            **kwargs,
        )

    return PartialLabelViewInput(
        fluorophore=fluorophore.id,
        primary_antibody=primary_antibody.id,
        secondary_antibody=secondary_antibody.id,
        **kwargs,
    )

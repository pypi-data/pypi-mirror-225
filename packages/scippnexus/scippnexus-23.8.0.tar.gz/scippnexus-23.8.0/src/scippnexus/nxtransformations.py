# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Scipp contributors (https://github.com/scipp)
# @author Simon Heybrock
from __future__ import annotations

from typing import List, Optional, Tuple, Union

import numpy as np
import scipp as sc
from scipp.scipy import interpolate

from .base import Group, NexusStructureError, NXobject, ScippIndex
from .field import Field, depends_on_to_relative_path


class TransformationError(NexusStructureError):
    pass


def make_transformation(obj, /, path) -> Optional[Transformation]:
    if path.startswith('/'):
        return obj.file[path]
    elif path != '.':
        return obj.parent[path]
    return None  # end of chain


class NXtransformations(NXobject):
    """Group of transformations."""


class Transformation:
    def __init__(self, obj: Union[Field, NXobject]):  # could be an NXlog
        self._obj = obj

    @property
    def sizes(self) -> dict:
        return self._obj.sizes

    @property
    def dims(self) -> Tuple[str, ...]:
        return self._obj.dims

    @property
    def shape(self) -> Tuple[int, ...]:
        return self._obj.shape

    @property
    def attrs(self):
        return self._obj.attrs

    @property
    def name(self):
        return self._obj.name

    @property
    def depends_on(self):
        if (path := self.attrs.get('depends_on')) is not None:
            return make_transformation(self._obj, path)
        return None

    @property
    def offset(self):
        if (offset := self.attrs.get('offset')) is None:
            return None
        if (offset_units := self.attrs.get('offset_units')) is None:
            raise TransformationError(
                f"Found {offset=} but no corresponding 'offset_units' "
                f"attribute at {self.name}"
            )
        return sc.spatial.translation(value=offset, unit=offset_units)

    @property
    def vector(self) -> sc.Variable:
        return sc.vector(value=self.attrs.get('vector'))

    def __getitem__(self, select: ScippIndex):
        transformation_type = self.attrs.get('transformation_type')
        # According to private communication with Tobias Richter, NeXus allows 0-D or
        # shape=[1] for single values. It is unclear how and if this could be
        # distinguished from a scan of length 1.
        value = self._obj[select]
        return self.make_transformation(value, transformation_type, select)

    def make_transformation(
        self,
        value: Union[sc.Variable, sc.DataArray],
        transformation_type: str,
        select: ScippIndex,
    ):
        try:
            if isinstance(value, sc.DataGroup):
                return value
            t = value * self.vector
            v = t if isinstance(t, sc.Variable) else t.data
            if transformation_type == 'translation':
                v = sc.spatial.translations(dims=v.dims, values=v.values, unit=v.unit)
            elif transformation_type == 'rotation':
                v = sc.spatial.rotations_from_rotvecs(v)
            else:
                raise TransformationError(
                    f"{transformation_type=} attribute at {self.name},"
                    " expected 'translation' or 'rotation'."
                )
            if isinstance(t, sc.Variable):
                t = v
            else:
                t.data = v
            if (offset := self.offset) is None:
                transform = t
            else:
                offset = sc.vector(value=offset.values, unit=offset.unit)
                offset = sc.spatial.translation(value=offset.value, unit=offset.unit)
                if transformation_type == 'translation':
                    offset = offset.to(unit=t.unit, copy=False)
                transform = t * offset
            if (depends_on := self.attrs.get('depends_on')) is not None:
                if not isinstance(transform, sc.DataArray):
                    transform = sc.DataArray(transform)
                transform.attrs['depends_on'] = sc.scalar(
                    depends_on_to_relative_path(depends_on, self._obj.parent.name)
                )
            return transform
        except (sc.DimensionError, sc.UnitError, TransformationError):
            # TODO We should probably try to return some other data structure and
            # also insert offset and other attributes.
            return value


def _interpolate_transform(transform, xnew):
    # scipy can't interpolate with a single value
    if transform.sizes["time"] == 1:
        transform = sc.concat([transform, transform], dim="time")
    return interpolate.interp1d(
        transform, "time", kind="previous", fill_value="extrapolate"
    )(xnew=xnew)


def _smaller_unit(a, b):
    if a.unit == b.unit:
        return a.unit
    ratio = sc.scalar(1.0, unit=a.unit).to(unit=b.unit)
    if ratio.value < 1.0:
        return a.unit
    else:
        return b.unit


def get_full_transformation(
    depends_on: Field,
) -> Union[None, sc.DataArray, sc.Variable]:
    """
    Get the 4x4 transformation matrix for a component, resulting
    from the full chain of transformations linked by "depends_on"
    attributes
    """
    if (t0 := make_transformation(depends_on, depends_on[()])) is None:
        return None
    return get_full_transformation_starting_at(t0)


def get_full_transformation_starting_at(
    t0: Transformation, *, index: ScippIndex = None
) -> Union[None, sc.DataArray, sc.Variable]:
    transformations = _get_transformations(t0, index=() if index is None else index)

    total_transform = None
    for transform in transformations:
        if total_transform is None:
            total_transform = transform
        elif isinstance(total_transform, sc.DataArray) and isinstance(
            transform, sc.DataArray
        ):
            unit = _smaller_unit(
                transform.coords['time'], total_transform.coords['time']
            )
            total_transform.coords['time'] = total_transform.coords['time'].to(
                unit=unit, copy=False
            )
            transform.coords['time'] = transform.coords['time'].to(
                unit=unit, copy=False
            )
            time = sc.concat(
                [total_transform.coords["time"], transform.coords["time"]], dim="time"
            )
            time = sc.datetimes(values=np.unique(time.values), dims=["time"], unit=unit)
            total_transform = _interpolate_transform(
                transform, time
            ) * _interpolate_transform(total_transform, time)
        else:
            total_transform = transform * total_transform
    if isinstance(total_transform, sc.DataArray):
        time_dependent = [t for t in transformations if isinstance(t, sc.DataArray)]
        times = [da.coords['time'][0] for da in time_dependent]
        latest_log_start = sc.reduce(times).max()
        return total_transform['time', latest_log_start:].copy()
    return total_transform


def _get_transformations(
    transform: Transformation, *, index: ScippIndex
) -> List[Union[sc.DataArray, sc.Variable]]:
    """Get all transformations in the depends_on chain."""
    transformations = []
    t = transform
    while t is not None:
        transformations.append(t[index])
        t = t.depends_on
    # TODO: this list of transformation should probably be cached in the future
    # to deal with changing beamline components (e.g. pixel positions) during a
    # live data stream (see https://github.com/scipp/scippneutron/issues/76).
    return transformations


def maybe_transformation(
    obj: Union[Field, Group],
    value: Union[sc.Variable, sc.DataArray, sc.DataGroup],
    sel: ScippIndex,
) -> Union[sc.Variable, sc.DataArray, sc.DataGroup]:
    """
    Return a loaded field, possibly modified if it is a transformation.

    Transformations are usually stored in NXtransformations groups. However, identifying
    transformation fields in this way requires inspecting the parent group, which
    is cumbersome to implement. Furthermore, according to the NXdetector documentation
    transformations are not necessarily placed inside NXtransformations.
    Instead we use the presence of the attribute 'transformation_type' to identify
    transformation fields.
    """
    if (transformation_type := obj.attrs.get('transformation_type')) is not None:
        from .nxtransformations import Transformation

        return Transformation(obj).make_transformation(value, transformation_type, sel)
    return value

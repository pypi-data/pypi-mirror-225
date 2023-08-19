"""
Functions for parsing a table of headers to extract information about the dataset
"""
from pathlib import Path
from typing import Any, Mapping
from itertools import product
from collections import defaultdict, OrderedDict
from functools import partial, cached_property

import numpy as np
from astropy.io import fits
from astropy.table import Table
from astropy.time import Time

from dkist_fits_specifications.utils.formatter import reformat_spec214_header


class HeaderParser:
    """
    A class for parsing and inspecting a table of Headers.
    """

    @staticmethod
    def _sort_headers(headers):
        dataset_axes = headers[0]["DNAXIS"]
        array_axes = headers[0]["DAAXES"]
        keys = [f"DINDEX{k}" for k in range(dataset_axes, array_axes, -1)]
        headers.sort(keys)
        return headers

    def __init__(self, headers: Table, *, validate=True):
        if not isinstance(headers, Table):
            raise TypeError("headers must be an astropy table.")

        self._headers = self._sort_headers(headers)
        if validate:
            self._validate_headers()

        # We must not access either .headers or .header here as otherwise they
        # will get cached before we have processed them fully
        header = self._get_headers_no_filename()[0]
        # Sort the header table into 214 order
        formatted_header = fits.Header(dict(header))
        if validate:
            formatted_header = reformat_spec214_header(formatted_header)

        ordered_keys = [key for key in formatted_header.keys() if key in header.keys()]
        # Make sure we put filenames (and anything else) back
        extra_keys = set(self._headers.colnames).difference(ordered_keys)
        ordered_keys += list(extra_keys)
        self._headers = self._headers[ordered_keys]

    @classmethod
    def from_headers(cls, headers: list[Mapping[str, Any]], *, filenames=None, **kwargs):
        header_table = Table(headers)
        if filenames is not None:
            header_table["filename"] = filenames
        return HeaderParser(header_table, **kwargs)

    @classmethod
    def from_filenames(cls, filenames: list[Path], *, hdu=0, include_filename=True, **kwargs):
        # Here we filter out empty cards and COMMENT cards
        filter_keys = ("", "COMMENT")
        headers = []
        for fname in filenames:
            header = dict(fits.getheader(fname, ext=hdu))
            if include_filename:
                header["filename"] = fname.as_posix()
            headers.append(header)
        headers = [dict(filter(lambda x: x[0] not in filter_keys, h.items())) for h in headers]
        return cls.from_headers(headers, **kwargs)

    def group_mosaic_tiles(self) -> "list[HeaderParser]":
        """
        Return a list of HeaderParser instances one per tile.
        """
        if "MINDEX1" not in self._headers.colnames:
            return [self]
        # Detect if we only have one tile and bail early.
        index1 = self._headers["MINDEX1"]
        index2 = self._headers["MINDEX2"]
        if (index1[0] == index1[1:]).all() and (index2[0] == index2[1:]).all():
            return [self]
        table_headers = self._headers.copy()
        # Otherwise return a list of Parser instances one per mosaic tile
        return list(map(partial(HeaderParser, validate=False), table_headers.group_by(("MINDEX1", "MINDEX2")).groups))

    def _validate_headers(self):
        """
        Validate the table of headers for internal consistency.

        Parameters
        ----------
        table_headers :  iterator
            An iterator of headers.
        """
        for hp in self.group_mosaic_tiles():
            t = hp._headers.copy()
            # Let's do roughly the minimal amount of verification here for construction
            # of the WCS. Validation for inventory records is done independently.

            # For some keys all the values must be the same
            same_keys = ["NAXIS", "DNAXIS", "BUNIT"]
            naxis_same_keys = ["NAXISn", "CTYPEn", "CUNITn"]
            dnaxis_same_keys = ["DNAXISn", "DTYPEn", "DPNAMEn", "DWNAMEn"]
            # Expand n in NAXIS keys
            for nsk in naxis_same_keys:
                for naxis in range(1, t["NAXIS"][0] + 1):
                    key = nsk.replace("n", str(naxis))
                    if key not in t.colnames:
                        raise ValueError(f"Expected key '{key}' not in table.")
                    same_keys.append(key)
            # Expand n in DNAXIS keys
            for dsk in dnaxis_same_keys:
                for dnaxis in range(1, t["DNAXIS"][0] + 1):
                    key = dsk.replace("n", str(dnaxis))
                    if key not in t.colnames:
                        raise ValueError(f"Expected key '{key}' not in table.")
                    same_keys.append(key)

            validate_t = t[same_keys]

            for col in validate_t.columns.values():
                if not all(col == col[0]):
                    raise ValueError(f"The {col.name} values did not all match:\n {set(col)}")

    @staticmethod
    def constant_columns(table, keys: list[str]):
        """
        Returns true if all columns given by keys have a constant value in table.
        """
        return all([np.allclose(table[0][k], table[k], rtol=1e-10) for k in keys])

    @staticmethod
    def compute_varying_axes_numbers(varying_axes):
        """
        Return the dataset pixel axes over which the spatial transform varies
        """
        if not varying_axes:
            return []
        if "pc" in varying_axes and "crval" in varying_axes:
            if varying_axes["pc"] != varying_axes["crval"]:
                # If both are in the dict but they don't match we make the
                # union of all of them, this makes the table bigger when it in
                # theory doesn't need to be, but it's also by far the easiest
                # solution.
                vaxes = list(sorted(set(varying_axes["pc"]).union(varying_axes["crval"])))
            vaxes = varying_axes["crval"]
        elif "crval" in varying_axes:
            vaxes = varying_axes["crval"]
        elif "pc" in varying_axes:
            vaxes = varying_axes["pc"]
        else:
            raise ValueError("What is this varying_axes dict you have given me?!")
        return vaxes

    def slice_for_file_axes(self, *axes):
        """
        Slice the header array given an index for the file dimensions.
        """
        tslice = [0] * len(self.files_shape)
        for i in axes:
            tslice[i] = slice(None)
        return tuple(tslice)

    def slice_for_dataset_array_axes(self, *axes, indexing="python"):
        """
        Slice the header array based on dataset indicies.

        Parameters
        ----------
        *axes
            Axes numbers for the dataset
        indexing : {"fits", "python"}
            If ``indexing=="python"`` then the input is assumed to be the
            number of the dataset axes counted from zero. If
            ``indexing=="fits"`` then it is assumed to count from one.
        """
        file_axes = np.array(axes).flatten() - self.header["DAAXES"]
        # If the input is fits then we have to subtract one.
        if indexing == "fits":
            file_axes -= 1
        if any(file_axes < 0) or any(file_axes > len(self.files_shape)):
            raise ValueError("Some or all of the axes are out of bounds for the files dimensions.")
        return self.slice_for_file_axes(*file_axes)

    def _get_headers_no_filename(self):
        h = self._headers.copy()
        if "filename" in h.colnames:
            h.remove_column("filename")
        return h

    @cached_property
    def header(self):
        return dict(self.headers[0])

    @cached_property
    def headers(self):
        return self._get_headers_no_filename()

    @cached_property
    def filenames(self):
        if "filename" not in self._headers.colnames:
            return None
        return np.array(list(map(Path, self._headers["filename"])))

    @cached_property
    def mosaic_grouped_headers(self):
        if "MINDEX1" not in self._headers.colnames:
            return self._headers.groups
        return self._headers.group_by(("MINDEX1", "MINDEX2")).groups

    @cached_property
    def files_shape(self):
        """
        The shape of the axes of the datasets not in the arrays.

        In FITS order.
        """
        DAAXES, DNAXIS = self.header["DAAXES"], self.header["DNAXIS"]
        return tuple(self.header[f"DNAXIS{d}"] for d in range(DAAXES + 1, DNAXIS + 1))

    @cached_property
    def dataset_shape(self):
        """
        The shape of the full reconstructed dataset

        In FITS order
        """
        DNAXIS = self.header["DNAXIS"]
        return tuple(self.header[f"DNAXIS{d}"] for d in range(1, DNAXIS + 1))

    @cached_property
    def array_shape(self):
        """
        The size of a singular array in a file.

        In FITS order
        """
        return tuple(self.header[f"NAXIS{n}"] for n in range(1, self.header["NAXIS"] + 1))

    @cached_property
    def axes_types(self):
        """
        The list of DTYPEn for the first header.

        In FITS order
        """
        return [self.header[f"DTYPE{n}"] for n in range(1, self.header["DNAXIS"] + 1)]

    @cached_property
    def header_array(self):
        """
        The header table as a numpy recarray with the shape of the dataset axes.

        In FITS order
        """
        return np.array(self.headers).reshape(self.files_shape, order="F")

    @cached_property
    def varying_spatial_daxes(self) -> dict[str, list[int]]:
        """
        The FITS pixel axes over which CRVAL or PC vary.
        """
        NAXIS, DAAXES = self.header["NAXIS"], self.header["DAAXES"]
        # Find which dataset axes the pointing varies along
        # If any of these keys vary along any of the dataset axes we want to know
        naxis_v = list(range(1, NAXIS + 1))
        crval_keys = [f"CRVAL{n}" for n in naxis_v]
        pc_keys = [f"PC{i}_{j}" for i, j in product(naxis_v, naxis_v)]
        varying_axes = defaultdict(list)
        for i in range(len(self.files_shape)):
            tslice = self.slice_for_file_axes(i)
            sliced_headers = self.header_array[tslice]
            if not self.constant_columns(sliced_headers, pc_keys):
                varying_axes["pc"].append(DAAXES + i + 1)
            if not self.constant_columns(sliced_headers, crval_keys):
                varying_axes["crval"].append(DAAXES + i + 1)

        return dict(varying_axes)

    @cached_property
    def varying_temporal_daxes(self) -> list[int]:
        """
        The FITS pixel axes over which time varies.
        """
        varying_daxes = []
        for i in range(len(self.files_shape)):
            tslice = self.slice_for_file_axes(i)
            sliced_headers = self.header_array[tslice]
            if not (sliced_headers[0]["DATE-AVG"] == sliced_headers["DATE-AVG"]).all():
                varying_daxes.append(self.header["DAAXES"] + i + 1)
        return varying_daxes

    @cached_property
    def pixel_axis_type_map(self) -> OrderedDict[str, list[int]]:
        """
        A dict which maps from DTYPE to the python array indices which contribute to that type.
        """
        axes_types = [self.header[f"DTYPE{n}"] for n in range(1, self.header["DNAXIS"] + 1)]
        axes_types = np.array(self.axes_types)
        type_map = defaultdict(list)
        if "STOKES" in self.axes_types:
            type_map["STOKES"] = np.argwhere(axes_types == "STOKES").flatten().tolist()
        if "SPECTRAL" in self.axes_types:
            type_map["SPECTRAL"] = np.argwhere(axes_types == "SPECTRAL").flatten().tolist()

        # Convert from FITS to Python
        vaxes = np.empty((0,), dtype=int)
        if self.varying_spatial_daxes:
            vaxes = np.array(self.compute_varying_axes_numbers(self.varying_spatial_daxes)) - 1
        type_map["SPATIAL"] = np.unique(
            np.concatenate((np.argwhere(axes_types == "SPATIAL").flatten(), vaxes))).tolist()
        ttypes = np.argwhere(axes_types == "TEMPORAL").flatten()
        taxes = np.array(self.varying_temporal_daxes, dtype=int) - 1
        type_map["TEMPORAL"] = np.unique(np.concatenate((ttypes, taxes))).tolist()

        # TODO: using max for sorting here is very fragile. It works for all the
        # current instruments with varying pointing because of the order we are
        # constructing the `type_map` above and because of the ordering of the
        # axes with cryo.
        # A time-varying pointing VTF dataset will cause this to fail.

        # Just being really explicit that the ordering in this dict matters
        # By ordering like this we can use the order of the keys to order the transforms
        return OrderedDict(sorted(type_map.items(), key=lambda item: max(item[1])))

    @cached_property
    def data_unit(self) -> str:
        return self.header["BUNIT"]

    @cached_property
    def midpoint_header(self):
        """
        The header from the frame closest to the midpoint of the observation.
        """
        times = Time(self.headers["DATE-AVG"])
        min_time = np.min(times)
        max_time = np.max(times)
        midtime = min_time + (max_time - min_time) / 2
        # Find a header at a time closest to that midtime
        # there might be more than one, but it doesn't matter
        midindex = np.argmin(np.abs(times - midtime))
        return self.headers[midindex]

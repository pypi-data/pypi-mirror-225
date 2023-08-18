import os
import pathlib
from importlib import resources
from typing import Iterable, Mapping, Union, Any

import asdf
import numpy as np
import astropy.units as u
from astropy.io.fits.hdu.base import BITPIX2DTYPE
from dkist.dataset import Dataset, TiledDataset
from dkist.io import FileManager
from dkist.io.loaders import AstropyFITSLoader

from dkist_inventory.inventory import extract_inventory
from dkist_inventory.header_parsing import HeaderParser
from dkist_inventory.transforms import TransformBuilder

__all__ = ["references_from_filenames", "dataset_from_fits", "asdf_tree_from_filenames"]


def references_from_filenames(header_parser: HeaderParser,
                              hdu_index: int = 0,
                              relative_to: os.PathLike = None) -> FileManager:
    """
    Given an array of paths to FITS files create a `dkist.io.FileManager`.

    Parameters
    ----------
    filenames
        An array of filenames, in numpy order for the output array (i.e. ``.flat``)

    headers
        A list of headers for files

    array_shape
        The desired output shape of the reference array. (i.e the shape of the
        data minus the HDU dimensions.)

    hdu_index
        The index of the HDU to reference. (Zero indexed)

    relative_to
        If set convert the filenames to be relative to this path.

    Returns
    -------
    `dkist.io.FileManager`
        A container that represents a set of FITS files, and can generate a
        `dask.array.Array` from them.
    """
    filenames = header_parser.filenames
    if filenames is None:
        raise ValueError("The HeaderParser provided does not contain the filenames.")
    if len(header_parser.mosaic_grouped_headers) != 1:
        raise ValueError("references_from_filenames must only be called for a singe mosaic tile.")

    # Note that the WCS (and therefore header_parser) works in cartesian (FITS)
    # order. When we build the reference array here we want the output to be in
    # C order so it acts like a numpy array.  That means slowest-varying first.
    # e.g. for a 5D VISP cube: stokes, map repeat, scan position, y, x.

    header_table = header_parser.headers
    # Transpose here to get the axes into C-order
    shaped_filepaths = filenames.reshape(header_parser.files_shape, order='F').T
    shaped_headers = header_parser.header_array.T

    dtypes = np.vectorize(lambda x: BITPIX2DTYPE[x])(shaped_headers["BITPIX"])
    shapes = shaped_headers[[f"NAXIS{a}" for a in range(header_table[0]["NAXIS"], 0, -1)]]

    filepath_fixer = np.vectorize(lambda p: str(p))
    if relative_to:
        filepath_fixer = np.vectorize(lambda p: os.path.relpath(p, str(relative_to)))

    shaped_filepaths = filepath_fixer(shaped_filepaths)

    # Validate all shapes and dtypes are consistent.
    dtype = np.unique(dtypes)
    if len(dtype) != 1:
        raise ValueError("Not all the dtypes of these files are the same.")
    dtype = list(dtype)[0]

    shape = np.unique(shapes)
    if len(shape) != 1:
        raise ValueError("Not all the shapes of these files are the same")
    shape = list(shape)[0]

    return FileManager.from_parts(
        shaped_filepaths.tolist(), hdu_index, dtype, shape, loader=AstropyFITSLoader
    )


def dataset_object_from_filenames(header_parser: HeaderParser,
                                  inventory: Mapping[str, Any],
                                  hdu: int,
                                  relative_to: os.PathLike = None) -> Dataset:
    """
    Generate a singular dataset object.

    Parameters
    ----------
    sorted_table
        The headers and filenames to process into a `dkist.Dataset`, in
        dataset index order.

    inventory
        Inventory record to use, if not specified will be generated.

    hdu
        The HDU to read the headers from and reference the data to.

    relative_to
        The path to reference the FITS files to inside the asdf. If not
        specified will be local to the asdf (i.e. ``./``).
    """
    ds_wcs = TransformBuilder(header_parser)

    # References from filenames
    array_container = references_from_filenames(header_parser,
                                                hdu_index=hdu,
                                                relative_to=relative_to)

    ds = Dataset(array_container._generate_array(),
                 ds_wcs.gwcs,
                 unit=u.Unit(header_parser.data_unit, format="fits"),
                 meta={'inventory': inventory, 'headers': header_parser.headers})

    ds._file_manager = array_container

    return ds


# This is the entry point from the asdf_maker service when asdf_maker calls this
# function it has used process_json_headers to make the headers kwarg
def asdf_tree_from_filenames(filenames: Iterable[os.PathLike],
                             headers: Iterable[Mapping[str, str]] = None,
                             inventory: Mapping[str, Any] = None,
                             hdu: int = 0,
                             relative_to: os.PathLike = None,
                             extra_inventory: Mapping[str, Any] = None) -> Mapping[str, Any]:
    """
    Build a DKIST asdf tree from a list of (unsorted) filenames.

    Parameters
    ----------
    filenames
        The filenames to process into a DKIST asdf dataset.

    headers
        The FITS headers if already known. If not specified will be read from
        filenames.

    inventory
        The frame inventory to put in the tree, if not specified a new one
        will be generated.

    hdu
        The HDU to read the headers from and reference the data to.

    relative_to
        The path to reference the FITS files to inside the asdf. If not
        specified will be local to the asdf (i.e. ``./``).

    extra_inventory
        An extra set of inventory to override the generated one.
    """
    if extra_inventory is None:
        extra_inventory = {}

    # In case filenames is a generator we cast to list.
    filenames = list(filenames)

    # headers is an iterator
    if not headers:
        header_parser = HeaderParser.from_filenames(filenames, hdu=hdu, include_filename=True)
    else:
        header_parser = HeaderParser.from_headers(headers, filenames=filenames)

    if not inventory:
        inventory = extract_inventory(header_parser, **extra_inventory)

    datasets = []
    for tile_header_parser in header_parser.group_mosaic_tiles():
        datasets.append(dataset_object_from_filenames(tile_header_parser,
                                                      inventory,
                                                      hdu,
                                                      relative_to))

    if len(datasets) == 1:
        tree = {"dataset": datasets[0]}
    else:
        # All tiled datasets should have exactly the same dict as their inventory record
        for ds in datasets:
            assert ds.meta["inventory"] == datasets[0].meta["inventory"]
            ds.meta["inventory"] = datasets[0].meta["inventory"]

        # Extract dataset shape
        mosaic_shape = tuple(header_parser.header[f"MAXIS{m}"] for m in range(header_parser.header["MAXIS"], 0, -1))
        datasets_arr = np.array(datasets, dtype=object).reshape(mosaic_shape)

        tree = {"dataset": TiledDataset(datasets_arr, inventory=datasets[0].meta["inventory"])}

    return tree


def dataset_from_fits(path: Union[str, os.PathLike],
                      asdf_filename: str,
                      inventory: Mapping[str, str] = None,
                      hdu: int = 0,
                      relative_to: os.PathLike = None,
                      **kwargs) -> pathlib.Path:
    """
    Given a path containing FITS files write an asdf file in the same path.

    Parameters
    ----------
    path
        The path to read the FITS files (with a `.fits` file extension) from
        and save the asdf file.

    asdf_filename
        The filename to save the asdf with in the path.

    inventory
        The dataset inventory for this collection of FITS. If `None` a random one will be generated.

    hdu
        The HDU to read from the FITS files.

    relative_to
        The base path to use in the asdf references. By default this is the
        parent of ``path=``, it's unlikely you should need to change this from
        the default.

    kwargs
        Additional kwargs are passed to `asdf.AsdfFile.write_to`.

    Returns
    -------
    asdf_filename
        The path of the ASDF file written.

    """
    path = pathlib.Path(path).expanduser()
    relative_to = pathlib.Path(relative_to or path).expanduser()

    files = path.glob("*fits")

    tree = asdf_tree_from_filenames(
        list(files), inventory=inventory, hdu=hdu, relative_to=relative_to
    )
    with resources.as_file(resources.files("dkist.io") / "level_1_dataset_schema.yaml") as schema_path:
        with asdf.AsdfFile(tree, custom_schema=schema_path) as afile:
            afile.write_to(path / asdf_filename, **kwargs)

    return path / asdf_filename

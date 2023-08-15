import pathlib

import asdf
import astropy.units as u
import pytest
from dkist.dataset import Dataset, TiledDataset
from dkist.io import FileManager
from dkist_data_simulator.spec214.vbi import SimpleVBIDataset
from dkist_inventory.asdf_generator import (asdf_tree_from_filenames,
                                            dataset_from_fits,
                                            references_from_filenames)
from dkist_inventory.header_parsing import HeaderParser


def test_array_container_shape(header_filenames):
    header_parser = HeaderParser.from_filenames(header_filenames, hdu=0)
    header_parser = header_parser.group_mosaic_tiles()[0]

    # References from filenames
    array_container = references_from_filenames(
        header_parser, hdu_index=0, relative_to="."
    )
    assert array_container.output_shape == array_container._generate_array().shape


def test_asdf_tree(header_filenames):
    tree = asdf_tree_from_filenames(header_filenames)
    assert isinstance(tree, dict)


def test_asdf_tree_with_headers_and_inventory_args():
    # given
    file_count = 5
    headers = []
    file_names = []
    for i, ds in enumerate(SimpleVBIDataset(
            n_time=file_count,
            time_delta=1,
            linewave=550 * u.nm,
            detector_shape=(10, 10),)):
        h = ds.header()
        h['BITPIX'] = 8
        headers.append(h)
        file_names.append(f"wibble_{i}.fits")
    tree = asdf_tree_from_filenames(file_names, headers)
    assert isinstance(tree, dict)


def test_validator(header_parser):
    header_parser._headers[3]["NAXIS"] = 5
    with pytest.raises(ValueError, match="NAXIS"):
        header_parser._validate_headers()


def test_references_from_filenames(header_parser):
    # references_from_filenames only works on a single tile
    header_parser = header_parser.group_mosaic_tiles()[0]
    base = header_parser.filenames[0].parent
    refs: FileManager = references_from_filenames(
        header_parser,
        relative_to=base,
    )

    for ref in refs.filenames:
        assert base.as_posix() not in ref


def test_dataset_from_fits(header_directory):
    asdf_filename = "test_asdf.asdf"
    asdf_file = pathlib.Path(header_directory) / asdf_filename
    try:
        dataset_from_fits(header_directory, asdf_filename)

        assert asdf_file.exists()

        with asdf.open(asdf_file) as adf:
            ds = adf["dataset"]
            assert isinstance(ds, (Dataset, TiledDataset))
            if isinstance(ds, Dataset):
                assert ds.unit is u.count
                # A simple test to see if the headers are 214 ordered
                assert ds.headers.colnames[0] == "SIMPLE"
                assert ds.headers.colnames[1] == "BITPIX"
            elif isinstance(ds, TiledDataset):
                assert ds[0, 0].unit is u.count
    finally:
        asdf_file.unlink()

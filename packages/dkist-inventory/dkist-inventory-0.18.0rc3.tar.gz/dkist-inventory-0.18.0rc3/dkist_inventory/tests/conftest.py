import astropy.units as u
import pytest
from dkist.conftest import *
from dkist_data_simulator.spec214.cryo import SimpleCryonirspSPDataset, SimpleCryonirspCIDataset, TimeDependentCryonirspSPDataset, \
    TimeDependentCryonirspCIDataset
from dkist_data_simulator.spec214.vbi import (MosaicedVBIBlueDataset,
                                              SimpleVBIDataset,
                                              TimeDependentVBIDataset)
from dkist_data_simulator.spec214.visp import (SimpleVISPDataset,
                                               TimeDependentVISPDataset)
from dkist_data_simulator.spec214.vtf import SimpleVTFDataset
from dkist_inventory.transforms import TransformBuilder
from dkist_inventory.header_parsing import HeaderParser


@pytest.fixture(scope="session")
def dataset():
    def _dataset(dataset_name):
        datasets = {
            "visp":
                SimpleVISPDataset(
                    2, 2, 4, 5, linewave=500 * u.nm, detector_shape=(32, 32)
                ),
            "vtf":
                SimpleVTFDataset(
                    2, 2, 4, 5, linewave=500 * u.nm, detector_shape=(32, 32)
                ),
            "vbi":
                SimpleVBIDataset(
                    n_time=5, time_delta=5, linewave=500 * u.nm, detector_shape=(32, 32)
                ),
            "cryonirsp-sp-single-meas-no-stokes":
                SimpleCryonirspSPDataset(
                    n_meas=1, n_steps=2, n_maps=2, n_stokes=1, time_delta=10, linewave=1083 * u.nm
                ),
            "cryonirsp-sp-multi-meas-no-stokes":
                SimpleCryonirspSPDataset(
                    n_meas=2, n_steps=2, n_maps=2, n_stokes=1, time_delta=10, linewave=1083 * u.nm
                ),
            "cryonirsp-ci-single-meas-no-stokes":
                SimpleCryonirspCIDataset(
                    n_meas=1, n_steps=2, n_maps=2, n_stokes=1, time_delta=10, linewave=1083 * u.nm
                ),
            "cryonirsp-ci-multi-meas-no-stokes":
                SimpleCryonirspCIDataset(
                    n_meas=2, n_steps=2, n_maps=2, n_stokes=1, time_delta=10, linewave=1083 * u.nm
                ),
            "cryonirsp-sp-single-meas-stokes":
                SimpleCryonirspSPDataset(
                    n_meas=1, n_steps=2, n_maps=2, n_stokes=4, time_delta=10, linewave=1083 * u.nm
                ),
            "cryonirsp-sp-multi-meas-stokes":
                SimpleCryonirspSPDataset(
                    n_meas=2, n_steps=2, n_maps=2, n_stokes=4, time_delta=10, linewave=1083 * u.nm
                ),
            "cryonirsp-ci-single-meas-stokes":
                SimpleCryonirspCIDataset(
                    n_meas=1, n_steps=2, n_maps=2, n_stokes=4, time_delta=10, linewave=1083 * u.nm
                ),
            "cryonirsp-ci-multi-meas-stokes":
                SimpleCryonirspCIDataset(
                    n_meas=2, n_steps=2, n_maps=2, n_stokes=4, time_delta=10, linewave=1083 * u.nm
                ),
            "cryonirsp-sp-time-varying-single-meas-no-stokes":
                TimeDependentCryonirspSPDataset(
                    n_meas=1, n_steps=2, n_maps=2, n_stokes=1, time_delta=10, linewave=1083 * u.nm
                ),
            "cryonirsp-sp-time-varying-multi-meas-no-stokes":
                TimeDependentCryonirspSPDataset(
                    n_meas=2, n_steps=2, n_maps=2, n_stokes=1, time_delta=10, linewave=1083 * u.nm
                ),
            "cryonirsp-ci-time-varying-single-meas-no-stokes":
                TimeDependentCryonirspCIDataset(
                    n_meas=1, n_steps=3, n_maps=2, n_stokes=1, time_delta=10, linewave=1083 * u.nm
                ),
            "cryonirsp-ci-time-varying-multi-meas-no-stokes":
                TimeDependentCryonirspCIDataset(
                    n_meas=2, n_steps=3, n_maps=4, n_stokes=1, time_delta=10, linewave=1083 * u.nm
                ),
            "cryonirsp-sp-time-varying-single-meas-stokes":
                TimeDependentCryonirspSPDataset(
                    n_meas=1, n_steps=2, n_maps=2, n_stokes=4, time_delta=10, linewave=1083 * u.nm
                ),
            "cryonirsp-sp-time-varying-multi-meas-stokes":
                TimeDependentCryonirspSPDataset(
                    n_meas=2, n_steps=2, n_maps=2, n_stokes=4, time_delta=10, linewave=1083 * u.nm
                ),
            "cryonirsp-ci-time-varying-single-meas-stokes":
                TimeDependentCryonirspCIDataset(
                    n_meas=1, n_steps=3, n_maps=2, n_stokes=4, time_delta=10, linewave=1083 * u.nm
                ),
            "cryonirsp-ci-time-varying-multi-meas-stokes":
                TimeDependentCryonirspCIDataset(
                    n_meas=2, n_steps=3, n_maps=4, n_stokes=4, time_delta=10, linewave=1083 * u.nm
                ),
            "vbi-mosaic":
                MosaicedVBIBlueDataset(
                    n_time=2, time_delta=10, linewave=400 * u.nm, detector_shape=(32, 32)
                ),
            "vbi-time-varying":
                TimeDependentVBIDataset(
                    n_time=4, time_delta=10, linewave=400 * u.nm, detector_shape=(32, 32)
                ),
            "visp-time-varying-single":
                TimeDependentVISPDataset(
                    n_maps=1, n_steps=4, n_stokes=1, time_delta=10, linewave=500 * u.nm, detector_shape=(16, 128)
                ),
            "visp-time-varying-multi":
                TimeDependentVISPDataset(
                    n_maps=2, n_steps=3,n_stokes=4, time_delta=10, linewave=500 * u.nm, detector_shape=(16, 128)
                ),
        }
        return datasets[dataset_name]
    return _dataset


@pytest.fixture(scope="session")
def simulated_dataset(cached_tmpdir, dataset):
    def _simulated_dataset(dataset_name):
        atmpdir = cached_tmpdir / dataset_name
        existed = atmpdir.exists()
        if not existed:
            ds = dataset(dataset_name)
            ds.generate_files(atmpdir, f"{dataset_name.upper()}_{{ds.index}}.fits")

        return atmpdir
    return _simulated_dataset


@pytest.fixture(scope="session", params=[
    "vtf",
    "vbi",
    "visp",
    "cryonirsp-sp-single-meas-no-stokes",
    "cryonirsp-sp-multi-meas-no-stokes",
    "cryonirsp-ci-single-meas-no-stokes",
    "cryonirsp-ci-multi-meas-no-stokes",
    "cryonirsp-sp-single-meas-stokes",
    "cryonirsp-sp-multi-meas-stokes",
    "cryonirsp-ci-single-meas-stokes",
    "cryonirsp-ci-multi-meas-stokes",
    "cryonirsp-sp-time-varying-single-meas-no-stokes",
    "cryonirsp-sp-time-varying-multi-meas-no-stokes",
    "cryonirsp-ci-time-varying-single-meas-no-stokes",
    "cryonirsp-ci-time-varying-multi-meas-no-stokes",
    "cryonirsp-sp-time-varying-single-meas-stokes",
    "cryonirsp-sp-time-varying-multi-meas-stokes",
    "cryonirsp-ci-time-varying-single-meas-stokes",
    "cryonirsp-ci-time-varying-multi-meas-stokes",
    "vbi-mosaic",
    "vbi-time-varying",
    "visp-time-varying-single",
    "visp-time-varying-multi",
])
def header_directory(request, simulated_dataset):
    return simulated_dataset(request.param)


@pytest.fixture
def vbi_time_varying_transform_builder(header_directory):
    if "vbi-time-varying" not in header_directory.as_posix():
        pytest.skip()

    header_parser = HeaderParser.from_filenames(header_directory.glob("*"))
    return TransformBuilder(header_parser)


@pytest.fixture
def header_filenames(header_directory):
    files = list(header_directory.glob("*"))
    files.sort()
    return files


@pytest.fixture
def header_parser(header_filenames):
    return HeaderParser.from_filenames(header_filenames)


@pytest.fixture
def transform_builder(header_filenames):
    # We can't build a single transform builder for a mosaic
    if "vbi-mosaic" in header_filenames[0].as_posix():
        pytest.skip()
    header_parser = HeaderParser.from_filenames(header_filenames)
    return TransformBuilder(header_parser)


@pytest.fixture
def non_varying_transform_builder(header_filenames):
    if ("varying" in header_filenames[0].as_posix() or "mosaic" in header_filenames[0].as_posix()):
        pytest.skip()
    header_parser = HeaderParser.from_filenames(header_filenames)
    return TransformBuilder(header_parser)

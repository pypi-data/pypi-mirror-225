"""Tests neuropil_correction_utils"""
import pytest

from aind_ophys_pipeline_utils import neuropil_correction_utils
from pipeline_util import get_plane


@pytest.mark.parametrize(
    "neuropil_trace_h5, roi_trace_h5, neuropil_trace_output_json",
    [
        ("300um_neuropil_trace.h5", "300um_roi_traces.h5",
         "300um_neuropil_trace_output.json"),
    ],
)
def test_create_input_json_capsule(
    neuropil_trace_h5,
    roi_trace_h5,
    neuropil_trace_output_json,
    ophys_files_capsule,
    helper_functions,
):
    """Test neuropil correction input json"""
    movie_fn, base_dir = ophys_files_capsule
    plane = get_plane(base_dir)
    output_dir = helper_functions.create_results_dir("results/")
    expected = {
        "neuropil_trace_file": str(movie_fn.parent / neuropil_trace_h5),
        "roi_trace_file": str(movie_fn.parent / roi_trace_h5),
        "storage_directory": str(output_dir / plane),
        "output_json": str(output_dir / plane / neuropil_trace_output_json),
    }

    actual = neuropil_correction_utils.create_input_json(
        base_dir, output_dir, plane)
    assert actual == expected

"""Tests dff_utils"""
import pytest

from aind_ophys_pipeline_utils import dff_utils
from pipeline_util import get_plane


@pytest.mark.parametrize(
    "neuropil_trace_h5, dff_h5, movie_frame_rate_hz",
    [
        ("300um_neuropil_trace.h5", "300um_dff.h5", 30.0),
    ],
)
def test_create_input_json_capsule(
    neuropil_trace_h5, dff_h5, movie_frame_rate_hz, ophys_files_capsule, helper_functions
):
    """Test dff input json"""
    movie_fn, base_dir = ophys_files_capsule
    plane = get_plane(base_dir)
    output_dir = helper_functions.create_results_dir("results/")
    expected = {
        "input_file": str(movie_fn.parent / neuropil_trace_h5),
        "movie_frame_rate_hz": movie_frame_rate_hz,
        "output_file": str(output_dir / plane / dff_h5),
    }

    actual = dff_utils.create_input_json(base_dir, output_dir, plane)
    assert actual == expected

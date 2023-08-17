"""Test suite2p motion correction"""
from aind_ophys_pipeline_utils import segmentation_utils
from pipeline_util import get_plane
import pytest


@pytest.mark.parametrize(
    "movie_frame_rate_hz, motion_corrected_output, segmentation_output",
    [
        (30.0, "300um_motion_corrected.h5", "300um_segmentation_output.json"),
    ],
)
def test_create_input_json_capsule(
    movie_frame_rate_hz,
    motion_corrected_output,
    segmentation_output,
    ophys_files_capsule,
    helper_functions,
):
    """Test segmentation input json"""
    movie_fn, base_dir = ophys_files_capsule
    output_dir = helper_functions.create_results_dir("results/")
    plane = get_plane(base_dir)
    motion_corrected_dir = movie_fn.parent
    expected = {
        "suite2p_args": {
            "h5py": str(motion_corrected_dir / motion_corrected_output),
            "tmp_dir": "/scratch",
            "movie_frame_rate_hz": movie_frame_rate_hz,
        },
        "postprocess_args": {
            "motion_corrected_video": str(motion_corrected_dir / motion_corrected_output),
            "output_json": str(output_dir / "300" / segmentation_output),
        },
    }
    actual = segmentation_utils.create_input_json(base_dir, output_dir, plane)
    assert actual == expected

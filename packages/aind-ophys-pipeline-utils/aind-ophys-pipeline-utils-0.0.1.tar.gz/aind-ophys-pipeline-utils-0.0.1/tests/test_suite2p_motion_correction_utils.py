"""Test suite2p motion correction"""
from aind_ophys_pipeline_utils import suite2p_motion_correction_utils
from pipeline_util import get_plane
import pytest


@pytest.mark.parametrize(
    "movie_frame_rate_hz, motion_corrected_output, motion_diagnostics_output, max_projection_output, avg_projection_output, registration_summary_output, motion_correction_preview_output, output_json",
    [
        (
            30.0,
            "300um_suite2p_motion_output.h5",
            "300um_suite2p_rigid_motion_transform.csv",
            "300um_suite2p_maximum_projection.png",
            "300um_suite2p_average_projection.png",
            "300um_suite2p_registration_summary.png",
            "300um_suite2p_motion_preview.webm",
            "300um_suite2p_motion_correction_output.json",
        ),
    ],
)
def test_create_input_json_capsule(
    movie_frame_rate_hz,
    motion_corrected_output,
    motion_diagnostics_output,
    max_projection_output,
    avg_projection_output,
    registration_summary_output,
    motion_correction_preview_output,
    output_json,
    ophys_files_capsule,
    helper_functions,
):
    """Test suite2p motion correction input json"""
    movie_fn, base_dir = ophys_files_capsule
    output_dir = helper_functions.create_results_dir("results/")
    plane = get_plane(base_dir)
    expected = {
        "h5py": str(movie_fn),
        "movie_frame_rate_hz": movie_frame_rate_hz,
        "motion_corrected_output": str(output_dir / plane / motion_corrected_output),
        "motion_diagnostics_output": str(output_dir / plane / motion_diagnostics_output),
        "max_projection_output": str(output_dir / plane / max_projection_output),
        "avg_projection_output": str(output_dir / plane / avg_projection_output),
        "registration_summary_output": str(output_dir / plane / registration_summary_output),
        "motion_correction_preview_output": str(
            output_dir / plane / motion_correction_preview_output
        ),
        "output_json": str(output_dir / plane / output_json),
    }
    actual = suite2p_motion_correction_utils.create_input_json(
        base_dir, output_dir, plane)
    assert actual == expected

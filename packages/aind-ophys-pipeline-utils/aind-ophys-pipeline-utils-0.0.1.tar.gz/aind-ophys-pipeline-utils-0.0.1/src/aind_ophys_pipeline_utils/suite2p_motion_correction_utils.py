"""suite2p motion utility"""
import glob
import os

from pipeline_util import (
    make_output_directory,
    get_frame_rate_platform_json,
)


def create_input_json(input_dir: str, output_dir: str, plane=None) -> dict:
    """Generates suite2p motion correction input json for a given plane

    Args:
        input_dir (str): path to data directory
        output_dir (str): path to results directory
        plane (int, optional): Plane to process if session directory is passed. Defaults to None.

    Returns:
        dict: suite2p motion correction input json
    """
    if plane is None:
        h5_file = glob.glob(f"{input_dir}/*.h5")[0]
    else:
        h5_file = glob.glob(f"{input_dir}/Other_[0-9]*/Other/ophys/planes/{plane}/*um.h5")[0]
    plane = str(plane)
    output_dir = make_output_directory(output_dir, plane)
    frame_rate_hz = get_frame_rate_platform_json(input_dir)
    return {
        "h5py": h5_file,
        "movie_frame_rate_hz": frame_rate_hz,
        "motion_corrected_output": os.path.join(output_dir, f"{plane}um_suite2p_motion_output.h5"),
        "motion_diagnostics_output": os.path.join(
            output_dir, f"{plane}um_suite2p_rigid_motion_transform.csv"
        ),
        "max_projection_output": os.path.join(
            output_dir, f"{plane}um_suite2p_maximum_projection.png"
        ),
        "avg_projection_output": os.path.join(
            output_dir, f"{plane}um_suite2p_average_projection.png"
        ),
        "registration_summary_output": os.path.join(
            output_dir, f"{plane}um_suite2p_registration_summary.png"
        ),
        "motion_correction_preview_output": os.path.join(
            output_dir, f"{plane}um_suite2p_motion_preview.webm"
        ),
        "output_json": os.path.join(output_dir, f"{plane}um_suite2p_motion_correction_output.json"),
    }

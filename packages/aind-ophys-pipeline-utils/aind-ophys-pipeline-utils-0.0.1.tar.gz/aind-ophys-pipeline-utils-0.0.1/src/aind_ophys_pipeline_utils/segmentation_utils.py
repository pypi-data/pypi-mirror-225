"""Segmentation Utility"""
import os
from pipeline_util import (
    get_motion_corrected_movie,
    make_output_directory,
    get_frame_rate_platform_json,
)


def create_input_json(input_dir: str, output_dir: str, plane: str) -> dict:
    """Generates input json for segment_postprocess module in ophys_etl

    Args:
        input_dir (str): path to data directory
        output_dir (str): path to results directory
        plane (str): plane depth

    Returns:
        dict: suite2p motion correction input json
    """
    motion_corrected_fn = get_motion_corrected_movie(input_dir, plane)
    output_dir = make_output_directory(output_dir, plane)
    return {
        "suite2p_args": {
            "h5py": motion_corrected_fn,
            "movie_frame_rate_hz": get_frame_rate_platform_json(input_dir),
            "tmp_dir": "/scratch",
        },
        "postprocess_args": {
            "motion_corrected_video": motion_corrected_fn,
            "output_json": os.path.join(output_dir, f"{plane}um_segmentation_output.json"),
        },
    }

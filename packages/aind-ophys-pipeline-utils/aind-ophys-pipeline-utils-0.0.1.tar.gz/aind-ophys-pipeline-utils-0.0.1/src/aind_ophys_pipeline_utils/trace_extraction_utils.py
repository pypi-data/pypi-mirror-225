"""Trace Extraction Utility"""
import glob
import os
import json

from pipeline_util import (
    get_motion_corrected_movie,
    add_motion_border,
    clean_roi_table,
    make_output_directory,
)


def create_input_json(input_dir: str, output_dir: str, plane: str) -> dict:
    """Creates input json for extract_traces

    Args:
        input_dir (str): input directory, data directory (co)
        output_dir (str): output directory, results directory (co)
        plane (str): plane depth

    Returns:
        dict: input json for extract_traces
    """
    h5_motion_corrected_movie = get_motion_corrected_movie(input_dir, plane)
    try:
        rigid_motion_transform = glob.glob(
            f"{input_dir}/Other_[0-9]*/Other/ophys/planes/{plane}/*um_suite2p_rigid_motion_transform.csv"
        )[0]
    except IndexError:
        rigid_motion_transform = glob.glob(
            f"{input_dir}/{plane}/*um_suite2p_rigid_motion_transform.csv"
        )[0]
    try:
        rois = glob.glob(
            f"{input_dir}/Other_[0-9]*/Other/ophys/planes/{plane}/*um_suite2p_segmentation_postprocess_rois.json"
        )[0]
    except IndexError:
        rois = glob.glob(f"{input_dir}/{plane}/*um_suite2p_segmentation_postprocess_rois.json")[0]
    with open(rois, "r") as f:
        rois = json.load(f)
    output_dir = make_output_directory(output_dir, plane)
    input_data = dict(
        storage_directory=output_dir,
        motion_corrected_stack=h5_motion_corrected_movie,
        output_json=os.path.join(output_dir, f"{plane}um_extract_traces.json"),
        log_0=rigid_motion_transform,
        rois=clean_roi_table(rois),
    )
    input_data = add_motion_border(rigid_motion_transform, input_data)

    return input_data

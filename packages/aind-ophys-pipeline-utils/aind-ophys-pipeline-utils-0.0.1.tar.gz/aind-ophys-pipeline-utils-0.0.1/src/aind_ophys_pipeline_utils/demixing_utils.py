"""demixing utility"""
import glob
import os

from pipeline_util import (
    read_json,
    remove_roi_nan,
    get_motion_corrected_movie,
    write_h5,
    read_h5,
    make_output_directory,
)


def create_input_json(input_dir: str, output_dir: str, plane: str) -> dict:
    """Creates input json for demixing

    Args:
        input_dir (str): input directory, data directory (co)
        output_dir (str): output directory, results directory (co)
        plane (str): plane depth

    Returns:
        dict: input json for demixing
    """
    h5_motion_corrected_movie = get_motion_corrected_movie(input_dir, plane)
    try:
        extract_traces = glob.glob(
            f"{input_dir}/Other_[0-9]*/Other/ophys/planes/{plane}/*extract_traces_v2.json"
        )[0]
    except KeyError:
        extract_traces = glob.glob(f"{input_dir}/{plane}/*extract_traces_v2.json")[0]
    try:
        roi_traces = glob.glob(
            f"{input_dir}/Other_[0-9]*/Other/ophys/planes/{plane}/*roi_traces.h5"
        )[0]
    except KeyError:
        roi_traces = glob.glob(f"{input_dir}/{plane}/*roi_traces.h5")[0]
    rois = read_h5(roi_traces, "data", "roi_names")
    roi_data = rois["data"]
    roi_names = rois["roi_names"]
    traces = read_json(extract_traces)
    mod_roi_data, _ = remove_roi_nan(traces, roi_names, roi_data)
    os.makedirs("./scratch", exist_ok=True)
    write_h5("./scratch/roi_traces.h5", roi_names=roi_names, data=mod_roi_data)
    output_dir = make_output_directory(output_dir, plane)
    input_data = dict(
        movie_h5=h5_motion_corrected_movie,
        traces_h5="./scratch/roi_traces.h5",
        output_file=os.path.join(output_dir, f"{plane}um_demixing_output.h5"),
        output_json=os.path.join(output_dir, f"{plane}um_demixing_output.json"),
        roi_masks=traces,
    )

    return input_data

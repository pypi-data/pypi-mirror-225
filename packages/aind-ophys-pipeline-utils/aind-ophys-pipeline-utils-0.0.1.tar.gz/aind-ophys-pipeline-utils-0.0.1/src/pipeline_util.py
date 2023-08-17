"""pipeline utility functions"""
import h5py as h5
import json
from datetime import datetime as dt
import pytz
import os
import glob
import subprocess
import numpy as np
from collections import namedtuple
import pandas as pd
from pathlib import Path
import platform

from aind_ophys_utils import motion_border_utils


def write_h5(fp: str, **kwargs: dict) -> bool:
    """Writes data to h5 file

    Args:
        fp (str): filepath to write data to
        kwargs (dict): data to write to h5 file

    Raises:
        Exception: Error writing h5 file
    Returns:
        bool: True if successful
    """
    try:
        with h5.File(fp, "w") as h:
            for k, v in kwargs.items():
                h.create_dataset(k, data=v)
        return True
    except Exception as e:
        raise Exception(f"Error writing h5 file: {e}")


def read_h5(fp: str, *args: list) -> dict:
    """Reads a list of keys from an h5 file

    Args:
        fp (str): filepath to read data from

    Returns:
        dict: data from h5 file in dictionary format
    """
    data = {}
    h5data = h5.File(fp, "r")
    for i in args:
        data[i] = h5data[i][()]
    h5data.close()
    return data


def write_json(fp: str, data: dict) -> bool:
    """Write data to json file
    Args:
        fp (str): filepath to write data to
        data (dict): data to write to json file

    Raises:
        Exception: Error writing json file
    Returns:
        bool: True if successful
    """
    try:
        with open(fp, "w") as j:
            json.dump(data, j, indent=2)
        return True
    except Exception as e:
        raise Exception(f"Error writing json file: {e}")


def read_json(fp: str) -> dict:
    """Read json file

    Args:
        fp (str): filepath to read data from

    Raises:
        Exception: Error reading json file
    Returns:
        dict: data from json file in dictionary format
    """
    try:
        with open(fp, "r") as j:
            return json.load(j)
    except Exception as e:
        raise Exception(f"Error reading json file: {e}")


def now() -> str:
    """Generates string with current date and time in PST

    Returns:
        str: YYYY-MM-DD_HH-MM-SS
    """
    current_dt = dt.now(tz=pytz.timezone("America/Los_Angeles"))
    return f"{current_dt.strftime('Y-m-d')}_{current_dt.strftime('H:M:S')}"


def create_results_folder(output_file_path: str, input_file_path: str) -> str:
    """Creates a results folder to store processed data

    Args:
        output_file_path (str): path to output folder
        input_file_path (str): path to input file

    Raises:
        OSError: Error creating results folder
    Returns:
        str: path to results folder
    """
    try:
        output_file_path = f"{output_file_path}_{get_file_name(input_file_path)}_processed_{now}"
        os.makedirs(output_file_path, exist_ok=True)
        return output_file_path
    except OSError as error:
        raise OSError(f"Error: {error}")


def get_basename(filename: str) -> str:
    """gets basename from filename for results data naming process

    Args:
        filename (str): filename to get basename from

    Raises:
        IndexError: could not get basename
    Returns:
        str: basename
    """
    try:
        return filename.split("/")[-1].split(".")[0]
    except IndexError:
        raise IndexError(f"Error: {filename} is not a valid file path")


def get_file_name(file_path: str) -> str:
    """gets basename of file path

    Args:
        file_path (str): file path to get file name from

    Raises:
        IndexError: could not get file name
    Returns:
        str: file name
    """
    try:
        return file_path.split("/")[-1].split(".")[0]
    except IndexError:
        raise IndexError(f"Error: {file_path} is not a valid file path")


def get_plane(input_dir: str) -> str:
    """Get the imaging plane from the session directory to know how to save the data

    Args:
        input_dir (str): directory where file is located

    Raises:
        Exception: if no plane depth is found
    Returns:
        plane (str): plane depth or None if no plane depth is found
    """

    try:
        try:
            filepath = glob.glob(f"{input_dir}/Other_[0-9]*/Other/ophys/planes/*")[0]

        except IndexError:
            filepath = glob.glob(f"{input_dir}/planes/*")[0]
        if platform.system() == "Windows":
            plane = filepath.split("\\")[-1]
        else:
            plane = filepath.split("/")[-1]
        assert int(plane)
        return plane
    except (IndexError, ValueError, AssertionError) as exc:
        raise Exception(f"Error: {exc}")


def get_motion_corrected_movie(input_dir: str, plane: str) -> str:
    """Retrieves the motion corrected, single plane movie from the /data directory

    Args:
        input_dir (str): directory where file is located
        plane (str): plane depth

    Raises:
        Exception: if no motion corrected movie is found
    Returns:
        h5_movie (str): motion corrected movie path
    """
    try:
        h5_movie = glob.glob(
            f"{input_dir}/Other_[0-9]*/Other/ophys/planes/{plane}/*motion_corrected.h5"
        )[0]
        return h5_movie
    except IndexError:
        try:
            h5_movie = glob.glob(f"{input_dir}/{plane}/*motion_corrected.h5")[0]
            return h5_movie
        except IndexError as exc:
            raise Exception(f"Error: {exc}")


def copy_data_to_results(src: str, dest: str) -> None:
    """Copies data from source to destination

    Args:
        src (str): source file path
        dest (str): destination file path

    Raises:
        subprocess.CalledProcessError: Error syncing the data to results folder
    """
    try:
        subprocess.run(["rsync", "-avz", src, dest])
    except subprocess.CalledProcessError as exc:
        raise subprocess.CalledProcessError(f"Error: {exc}")


def clean_roi_table(data: dict, remove_exclusion_labels=False) -> dict:
    """
    Removes unnecessary keys from the roi table

    Args:
        data (dict): roi table data
        remove_exclusion_labels (bool): remove exclusion labels from roi table data

    Returns:
        data (dict): cleaned roi table data
    """
    print(len(data))
    for roi in range(len(data)):
        data[roi].pop("max_correction_down", None)
        data[roi].pop("max_correction_up", None)
        data[roi].pop("max_correction_right", None)
        data[roi].pop("max_correction_left", None)
        if remove_exclusion_labels:
            data[roi].pop("exclusion_labels", None)
        data[roi].pop("mask_image_plane", None)
        data[roi]["mask"] = data[roi].get("mask_matrix", [])
    return data


def add_motion_border(input_csv, data):
    """Finds and adds max correction values assuming a max shift of 30.0 (default value in suite2p)

    Args:
        input_csv (str): rigid transform csv file output from suite2p motion correction
        data (dict): data for the input json file

    Raises:
        Exception: max shift could not be retrieved from csv file
    Returns:
        data (): input json data with max shift values added
    """
    csv_data = pd.read_csv(input_csv)
    max_shift = motion_border_utils.get_max_correction_from_df(csv_data)

    data["motion_border"] = {}

    # add max shift (left, right, up, down) to input json
    data["motion_border"]["x0"] = max_shift.left
    data["motion_border"]["x1"] = max_shift.right
    data["motion_border"]["y1"] = max_shift.up
    data["motion_border"]["y0"] = max_shift.down
    return data


def get_frame_rate_platform_json(input_dir: str) -> float:
    """Get the frame rate from the platform json file.
    Platform json will need to get copied to each data directory throughout the pipeline

    Args:
        input_dir (str): directory where file is located

    Raises:
        Exception: if no platform json file is found
    Returns:
        frame_rate (float): frame rate
    """
    try:
        try:
            platform_json = glob.glob(f"{input_dir}/Other_[0-9]*/Other/ophys/*platform.json")[0]
        except IndexError:
            platform_json = glob.glob(f"{input_dir}*platform.json")[0]
        with open(platform_json) as f:
            data = json.load(f)
        frame_rate = data["imaging_plane_groups"][0]["acquisition_framerate_Hz"]
        return frame_rate
    except IndexError as exc:
        raise Exception(f"Error: {exc}")


def remove_roi_nan(trace_exclusions: dict, roi_names: np.array, roi_data: np.array):
    """Removes ROIs that are NaNs from the ROI table

    Args:
        trace_exclusions (dict): trace exclusions file
        roi_names (np.array): roi names
        roi_data (dict): roi data

    Returns:
        roi_data (dict): roi data with NaNs removed
        roi_names (np.array): roi names with NaNs removed
    Raises:
        Exception: if roi_data is empty"""
    try:
        for i in range(len(trace_exclusions["exclusion_labels"])):
            # value = trace_exclusions['exclusion_labels'][i]['roi_id']
            # index = np.where(roi_names == value.encode())[0][0]
            find_nans = np.isnan(roi_data)
            roi_data[find_nans] = 0
            # roi_data = np.delete(roi_data, index, 0)
            # roi_names = np.delete(roi_names, index, 0)
    except Exception as exc:
        raise Exception(f"Error: {exc}")
    return roi_data, roi_names


def make_output_directory(output_dir: str, plane: str):
    """Creates the output directory if it does not exist

    Args:
        output_dir (str): output directory
        plane (str): plane depth

    Returns:
        output_dir (str): output directory
    """
    output_dir = os.path.join(output_dir, plane)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


# see comment in motion_border_from_max_frame_shift for an explanation
# of the difference between these two structures

MaxFrameShift = namedtuple("MaxFrameShift", ["left", "right", "up", "down"])

MotionBorder = namedtuple("MotionBorder", ["top", "bottom", "left_side", "right_side"])


def get_max_correction_values(
    x_series: pd.Series, y_series: pd.Series, max_shift: float = 30.0
) -> MaxFrameShift:
    """
    Gets the max correction values in the cardinal directions from a series
    of correction values in the x and y directions
    Parameters
    ----------
    x_series: pd.Series:
        A series of movements in the x direction
    y_series: pd.Series:
        A series of movements in the y direction
    max_shift: float
        Maximum shift to allow when considering motion correction. Any
        larger shifts are considered outliers (only absolute value matters).

    For deprecated implementation see:
    allensdk.internal.brain_observatory.roi_filter_utils.calculate_max_border

    Returns
    -------
    MaxFrameShift
        A named tuple containing the maximum correction values found during
        motion correction workflow step. Saved with the following direction
        order [left, right, up, down].

    """
    # take abs of max shift as we are considering both positive and negative
    # directions
    max_shift = abs(max_shift)

    # filter based out analomies based on maximum_shift
    x_no_outliers = x_series[(x_series >= -max_shift) & (x_series <= max_shift)]
    y_no_outliers = y_series[(y_series >= -max_shift) & (y_series <= max_shift)]
    # calculate max border shifts
    right_shift = -1 * x_no_outliers.min()
    left_shift = x_no_outliers.max()
    down_shift = -1 * y_no_outliers.min()
    up_shift = y_no_outliers.max()

    max_shift = MaxFrameShift(left=left_shift, right=right_shift, up=up_shift, down=down_shift)

    # check if all exist
    if np.any(np.isnan(np.array(max_shift))):
        raise ValueError(
            "One or more motion correction shifts "
            "was found to be Nan, max shift found: "
            f"{max_shift}, with max_shift {max_shift}"
        )

    return max_shift


def get_max_correction_from_file(input_csv: Path, max_shift: float = 30.0) -> MaxFrameShift:
    """

    Parameters
    ----------
    input_csv: Path
        Path to motion correction values for each frame stored in .csv format.
        This .csv file is expected to have a header row of either:
        ['framenumber','x','y','correlation','kalman_x', 'kalman_y'] or
        ['framenumber','x','y','correlation','input_x','input_y','kalman_x',
         'kalman_y','algorithm','type']
    max_shift: float
        Maximum shift to allow when considering motion correction. Any
        larger shifts are considered outliers.

    Returns
    -------
    max_shift
        A named tuple containing the maximum correction values found during
        motion correction workflow step. Saved with the following direction
        order [left, right, up, down].

    """
    motion_correction_df = pd.read_csv(input_csv)
    max_shift = get_max_correction_values(
        x_series=motion_correction_df["x"].astype("float"),
        y_series=motion_correction_df["y"].astype("float"),
        max_shift=max_shift,
    )
    return max_shift


def motion_border_from_max_shift(max_shift: MaxFrameShift) -> MotionBorder:
    """
    Find the MotionBorder that corresponds to a given
    MaxFrameShift
    """

    # The difference between MaxFrameShift and MotionBorder is that
    # MaxFrame shift records the maximum shift that was applied to
    # a movie in a given direction during motion correction. This could,
    # in principle, be negative (if a movie was only ever shifted up, it's
    # maximum down shift will be negative). MotionBorder is the positive
    # (or zero) number of pixels to ignore at the edge of a field of view.
    # In addition to the fact that MotionBorder can only be positive, there
    # is a transposition. If a movie is only ever shifted up, there should
    # be a non-zero motion border at the bottom, since those pixels were
    # either wrapped or padded by motion correction, but there should be
    # no motion border at the top (assuming you trust your motion correction
    # algorithm).

    result = MotionBorder(
        bottom=max(max_shift.up, 0),
        top=max(max_shift.down, 0),
        left_side=max(max_shift.right, 0),
        right_side=max(max_shift.left, 0),
    )

    return result

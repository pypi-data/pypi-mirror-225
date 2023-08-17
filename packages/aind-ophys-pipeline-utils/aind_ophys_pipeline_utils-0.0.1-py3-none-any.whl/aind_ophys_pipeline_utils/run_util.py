"""Pars command line args"""
import argparse

from pipeline_util import get_plane, write_json, copy_data_to_results
from aind_ophys_pipeline_utils import (
    demixing_utils,
    dff_utils,
    neuropil_correction_utils,
    segmentation_utils,
    suite2p_motion_correction_utils,
    trace_extraction_utils,
)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_dir", type=str, help="Input directory")
parser.add_argument("-o", "--output_dir", type=str, help="Output directory")
parser.add_argument("-p", "--plane", type=int, help="Plane depth", default=None)
parser.add_argument(
    "-a", "--action", type=str, help="Action to perform", default="create-input-json"
)
parser.add_argument("-c", "--capsule", type=str, help="Capsule to be run")


args = parser.parse_args()
input_dir = args.input_dir
output_dir = args.output_dir
capsule = args.capsule
action = args.action

if not args.plane:
    plane = get_plane(input_dir)
else:
    plane = args.plane

capsules = dict(
    demixing=demixing_utils,
    dff=dff_utils,
    neuropil_correction=neuropil_correction_utils,
    segmentation=segmentation_utils,
    suite2p_motion_correction=suite2p_motion_correction_utils,
    trace_extraction=trace_extraction_utils,
)
if action == "create-input-json":
    data = capsules[capsule].create_input_json(input_dir, output_dir, plane)
    write_json(input_dir + "input.json", data)
elif action == "copy-data-to-results":
    copy_data_to_results(input_dir, output_dir)

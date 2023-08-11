import pyxdf
import glob
import re

# streams, header = pyxdf.load_xdf('./data/p22.xdf')
#
# timestamps = []
# for i, entry in enumerate(streams[1]['time_series']):
#     if entry[0] != 'Stickfigure detected!' and entry[0] != 'No Stickfigure was detected!':
#         print(entry[0])



datafiles = []
for file in glob.glob("./data/*.xdf"):
    datafiles.append(file)

for datafile in datafiles:
    streams, header = pyxdf.load_xdf(datafile)
    p_id = datafile
    #TODO: extract id

    #get the progress stream -> can be any id in streams
    for stream in streams:
        if stream['info']['name'][0] == 'Progress':
            marker_stream = stream
            break

    # extract the timestamp of start_test and stop_test, total of four (two conditions)
    #works for all participants, cause they are ordered: 1. 'Starting the test.', 2. 'Completed the test of the first condition.', 3. 'Starting the test.', 4. 'Completed the test of the second condition.'
    timestamps = []
    for i, entry in enumerate(marker_stream['time_series']):
        if entry[0] == 'Starting the test.' or entry[0] == 'Completed the test of the first condition.' or entry[
            0] == 'Completed the test of the second condition.':
            timestamps.append((marker_stream['time_stamps'][i], entry[0]))
    print((p_id, timestamps))










import matplotlib.pyplot as plt

import numpy as np
# #this print basic info on all stream in the xdf file
# print("Found {} streams:".format(len(streams)))
# for ix, stream in enumerate(streams):
#     msg = "Stream {}: {} - type {} - source_id {} - shape {} at {} (effective {}) Hz"
#     print(msg.format(
#         ix + 1, stream['info']['name'][0],
#         stream['info']['type'][0],
#         stream['info']['source_id'][0],
#         (int(stream['info']['channel_count'][0]), len(stream['time_stamps'])),
#         stream['info']['nominal_srate'][0],
#         stream['info']['effective_srate'])
#     )
#     if any(stream['time_stamps']):
#         duration = stream['time_stamps'][-1] - stream['time_stamps'][0]
#         print("\tDuration: {} s".format(duration))
# print("Done.")

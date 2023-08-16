import pyxdf
import glob
import numpy as np
import re

# streams, header = pyxdf.load_xdf('./data/p22.xdf')
#
# timestamps = []
# for i, entry in enumerate(streams[1]['time_series']):
#     if entry[0] != 'Stickfigure detected!' and entry[0] != 'No Stickfigure was detected!':
#         print(entry[0])

printInfo = False
extractMarker = True
extractCsv = True

datafiles = []
for file in glob.glob("./data/*.xdf"):
    datafiles.append(file)

#datafiles = ["./data/p3.xdf"]

for datafile in datafiles:

    streams, header = pyxdf.load_xdf(datafile)
    # TODO: works only if saved in /data
    p_id = datafile[8:-4]

    if printInfo:
        print("Found {} streams:".format(len(streams)))
        for ix, stream in enumerate(streams):
            msg = "Stream {}: {} - type {} - source_id {} - shape {} at {} (effective {}) Hz"
            print(msg.format(
                ix + 1, stream['info']['name'][0],
                stream['info']['type'][0],
                stream['info']['source_id'][0],
                (int(stream['info']['channel_count'][0]), len(stream['time_stamps'])),
                stream['info']['nominal_srate'][0],
                stream['info']['effective_srate'])
            )
            if any(stream['time_stamps']):
                duration = stream['time_stamps'][-1] - stream['time_stamps'][0]
                print("\tDuration: {} s".format(duration))

    if extractMarker:
        #get the progress stream -> can be any id in streams
        for stream in streams:
            if stream['info']['name'][0] == 'Progress':
                marker_stream = stream
                break

        # extract the timestamp of start_test and stop_test, total of four (two conditions)
        #works for all participants, cause they are ordered: 1. 'Starting the test.', 2. 'Completed the test of the first condition.', 3. 'Starting the test.', 4. 'Completed the test of the second condition.'
        rawMarkers = []
        for i, entry in enumerate(marker_stream['time_series']):
            if entry[0] == 'Starting the test.' or entry[0] == 'Completed the test of the first condition.' or entry[
                0] == 'Completed the test of the second condition.':
                rawMarkers.append((marker_stream['time_stamps'][i], entry[0]))
        markers = [(rawMarkers[0][0], rawMarkers[1][0]), (rawMarkers[2][0], rawMarkers[3][0])]

    if extractCsv:
        for i, marker in enumerate(markers):
            for stream in streams:
                if stream['info']['name'][0] != 'Progress':
                    filename = "./data_extracted/p" + str(p_id)  + "_" + str(i+1) + "_" + stream['info']['source_id'][0] + ".csv"
                    data = stream['time_series']
                    timestamps = stream['time_stamps']
                    #add timestamps to the data
                    data = np.vstack([timestamps, data.T])
                    data = data.T
                    mask = np.logical_and(timestamps >= marker[0], timestamps <= marker[1])
                    data = data[mask]
                    if "XSensDot" in stream['info']['name'][0]:
                        #drop the local timestamp (last column)
                        data = data[:,:-1]
                    np.savetxt(filename, data, delimiter=",")


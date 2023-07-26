import pyxdf
import matplotlib.pyplot as plt
import numpy as np

streams, header = pyxdf.load_xdf('./data/P1.xdf')

#this print basic info on all stream in the xdf file
print("Found {} streams:".format(len(streams)))
for ix, stream in enumerate(streams):
    msg = "Stream {}: {} - type {} - uid {} - shape {} at {} (effective {}) Hz"
    print(msg.format(
        ix + 1, stream['info']['name'][0],
        stream['info']['type'][0],
        stream['info']['uid'][0],
        (int(stream['info']['channel_count'][0]), len(stream['time_stamps'])),
        stream['info']['nominal_srate'][0],
        stream['info']['effective_srate'])
    )
    if any(stream['time_stamps']):
        duration = stream['time_stamps'][-1] - stream['time_stamps'][0]
        print("\tDuration: {} s".format(duration))
print("Done.")

print(streams[0]['time_series'])